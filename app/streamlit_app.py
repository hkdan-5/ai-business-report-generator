import sys
import os

# Add project root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import io
from datetime import date

import pandas as pd
import streamlit as st

# Import internal project modules
from src.data_loader import load_sales_data
from src.data_cleaning import clean_sales_data
from src.analysis import (
    calculate_kpis,
    revenue_by_category,
    revenue_by_region,
    weekly_revenue,
    monthly_revenue,
)
from src.insight_engine import generate_business_insights
from src.llm_report import generate_business_report


# Configure the Streamlit page
# A wide layout creates a more professional dashboard experience
st.set_page_config(
    page_title="AI Business Report Generator",
    page_icon="📈",
    layout="wide",
)


@st.cache_data
def load_default_data(filepath: str) -> pd.DataFrame:
    """
    Load the default dataset from disk and apply data cleaning.

    The result is cached to avoid unnecessary repeated file access
    during dashboard interactions.
    """

    df = load_sales_data(filepath)
    df = clean_sales_data(df)

    return df


@st.cache_data
def load_uploaded_data(file_bytes: bytes, file_name: str) -> pd.DataFrame:
    """
    Load an uploaded CSV file and apply data cleaning.

    Parameters
    ----------
    file_bytes : bytes
        Raw bytes of the uploaded file.
    file_name : str
        Original filename, used only for caching purposes.

    Returns
    -------
    pd.DataFrame
        Cleaned uploaded dataset.
    """

    buffer = io.BytesIO(file_bytes)

    try:
        df = pd.read_csv(buffer, encoding="utf-8")
    except UnicodeDecodeError:
        buffer.seek(0)
        df = pd.read_csv(buffer, encoding="latin1")

    df = clean_sales_data(df)

    return df


def format_currency(value: float) -> str:
    """
    Format a numeric value as a currency string.
    """

    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """
    Format a decimal value as a percentage string.
    """

    return f"{value * 100:.2f}%"


def safe_growth_value(df: pd.DataFrame) -> float | None:
    """
    Safely return the latest growth rate from a time-based DataFrame.

    Returns None if the growth value is unavailable.
    """

    if df.empty or "growth_rate" not in df.columns:
        return None

    value = df["growth_rate"].iloc[-1]

    if pd.isna(value):
        return None

    return float(value)


def convert_df_to_csv(df: pd.DataFrame) -> bytes:
    """
    Convert a DataFrame to CSV bytes for download.
    """

    return df.to_csv(index=False).encode("utf-8")


# Sidebar content
# This section makes the dashboard more interactive and closer to a real analytics product
st.sidebar.title("Dashboard Controls")
st.sidebar.write(
    "Customize the analysis by uploading your own dataset and applying business filters."
)

uploaded_file = st.sidebar.file_uploader(
    "Upload a sales CSV file",
    type=["csv"],
)

# Load either uploaded data or the default local dataset
if uploaded_file is not None:
    df = load_uploaded_data(uploaded_file.getvalue(), uploaded_file.name)
    data_source_label = f"Uploaded file: {uploaded_file.name}"
else:
    df = load_default_data("data/superstore_sales.csv")
    data_source_label = "Default local dataset"

st.sidebar.caption(f"Data source: {data_source_label}")

# Stop early if dataset could not be loaded correctly
if df.empty:
    st.error("The dataset is empty after loading and cleaning.")
    st.stop()

# Validate expected columns before continuing
required_columns = {"order_date", "sales", "profit", "region", "category"}

missing_columns = required_columns - set(df.columns)

if missing_columns:
    st.error(
        "The dataset is missing required columns: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

# Date range filter
# This is especially useful for weekly and monthly trend analysis
min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

selected_date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
    start_date, end_date = selected_date_range
else:
    start_date, end_date = min_date, max_date

# Region and category filters
available_regions = sorted(df["region"].dropna().unique().tolist())
available_categories = sorted(df["category"].dropna().unique().tolist())

selected_regions = st.sidebar.multiselect(
    "Select region",
    options=available_regions,
    default=available_regions,
)

selected_categories = st.sidebar.multiselect(
    "Select category",
    options=available_categories,
    default=available_categories,
)

# Apply all dashboard filters
filtered_df = df.copy()

filtered_df = filtered_df[
    (filtered_df["order_date"].dt.date >= start_date)
    & (filtered_df["order_date"].dt.date <= end_date)
]

if selected_regions:
    filtered_df = filtered_df[filtered_df["region"].isin(selected_regions)]

if selected_categories:
    filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

# Stop early if no records remain after filtering
if filtered_df.empty:
    st.warning("No data is available for the selected filters.")
    st.stop()

# Run the analytics pipeline on the filtered dataset
kpis = calculate_kpis(filtered_df)
category_df = revenue_by_category(filtered_df)
region_df = revenue_by_region(filtered_df)
weekly_df = weekly_revenue(filtered_df)
monthly_df = monthly_revenue(filtered_df)

insights = generate_business_insights(
    kpis=kpis,
    category_df=category_df,
    region_df=region_df,
    weekly_df=weekly_df,
    monthly_df=monthly_df,
)

# Extract summary values for dashboard cards
top_category = category_df.iloc[0]["category"] if not category_df.empty else "N/A"
lowest_category = category_df.iloc[-1]["category"] if not category_df.empty else "N/A"
top_region = region_df.iloc[0]["region"] if not region_df.empty else "N/A"

latest_weekly_growth = safe_growth_value(weekly_df)
latest_monthly_growth = safe_growth_value(monthly_df)

weekly_growth_display = (
    format_percentage(latest_weekly_growth)
    if latest_weekly_growth is not None
    else "N/A"
)

monthly_growth_display = (
    format_percentage(latest_monthly_growth)
    if latest_monthly_growth is not None
    else "N/A"
)

# Main page header
st.title("AI Business Report Generator")
st.caption(
    "Executive-style analytics dashboard for automated KPI monitoring, business insight generation, "
    "and AI-written reporting."
)

header_left, header_right = st.columns([3, 1])

with header_left:
    st.markdown(
        """
This dashboard demonstrates a complete analytics workflow:
data loading, preprocessing, business KPI generation, weekly and monthly trend analysis,
structured insight generation, and AI-based executive reporting.
"""
    )

with header_right:
    st.info(
        f"""
**Date Range**  
{start_date} to {end_date}

**Rows Analyzed**  
{len(filtered_df):,}
"""
    )

# KPI section
st.markdown("---")
st.subheader("Executive KPI Overview")

kpi_col_1, kpi_col_2, kpi_col_3, kpi_col_4 = st.columns(4)

with kpi_col_1:
    st.metric(
        label="Total Revenue",
        value=format_currency(kpis["total_revenue"]),
        delta=weekly_growth_display if latest_weekly_growth is not None else None,
    )

with kpi_col_2:
    st.metric(
        label="Total Profit",
        value=format_currency(kpis["total_profit"]),
    )

with kpi_col_3:
    st.metric(
        label="Total Orders",
        value=f"{kpis['total_orders']:,}",
    )

with kpi_col_4:
    st.metric(
        label="Average Order Value",
        value=format_currency(kpis["avg_order_value"]),
        delta=monthly_growth_display if latest_monthly_growth is not None else None,
    )

# Business summary cards
st.markdown("---")
st.subheader("Business Performance Summary")

summary_col_1, summary_col_2, summary_col_3 = st.columns(3)

with summary_col_1:
    st.success(f"Top Performing Category: **{top_category}**")

with summary_col_2:
    st.success(f"Top Performing Region: **{top_region}**")

with summary_col_3:
    st.warning(f"Lowest Performing Category: **{lowest_category}**")

# Revenue composition charts
st.markdown("---")
st.subheader("Revenue Composition Analysis")

composition_col_1, composition_col_2 = st.columns(2)

with composition_col_1:
    st.write("Revenue by Category")
    st.bar_chart(category_df.set_index("category")["sales"])

with composition_col_2:
    st.write("Revenue by Region")
    st.bar_chart(region_df.set_index("region")["sales"])

# Time trend charts
st.markdown("---")
st.subheader("Revenue Trend Analysis")

trend_col_1, trend_col_2 = st.columns(2)

with trend_col_1:
    st.write("Weekly Revenue Trend")

    weekly_chart_df = weekly_df.copy().set_index("order_date")
    st.line_chart(weekly_chart_df["sales"])

with trend_col_2:
    st.write("Monthly Revenue Trend")

    monthly_chart_df = monthly_df.copy().set_index("order_date")
    st.line_chart(monthly_chart_df["sales"])

# Structured insights section
st.markdown("---")
st.subheader("Structured Business Insights")

st.code(insights, language="text")

# AI report section
# This section turns structured insights into an executive-facing report
st.markdown("---")
st.subheader("AI Executive Report")

st.write(
    "Generate a professional business report based on the analytical insights shown above."
)

if "ai_report" not in st.session_state:
    st.session_state.ai_report = ""

report_col_1, report_col_2 = st.columns([1, 1])

with report_col_1:
    generate_clicked = st.button("Generate AI Report", use_container_width=True)

with report_col_2:
    if st.session_state.ai_report:
        st.download_button(
            label="Download AI Report",
            data=st.session_state.ai_report,
            file_name="business_report.txt",
            mime="text/plain",
            use_container_width=True,
        )

if generate_clicked:
    try:
        report = generate_business_report(insights)
        st.session_state.ai_report = report

        with open("outputs/business_report.txt", "w", encoding="utf-8") as file:
            file.write(report)

        st.success("AI report generated successfully.")

    except Exception as error:
        st.error(
            "The AI report could not be generated. "
            "Please make sure Ollama is running and the selected model is available."
        )
        st.exception(error)

if st.session_state.ai_report:
    st.markdown("### Generated Executive Report")
    st.write(st.session_state.ai_report)

# Detailed source data section
st.markdown("---")
st.subheader("Filtered Source Data")

table_col_1, table_col_2 = st.columns([1, 1])

with table_col_1:
    st.download_button(
        label="Download Filtered Data",
        data=convert_df_to_csv(filtered_df),
        file_name="filtered_sales_data.csv",
        mime="text/csv",
        use_container_width=True,
    )

with table_col_2:
    st.download_button(
        label="Download Category Analysis",
        data=convert_df_to_csv(category_df),
        file_name="category_analysis.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.dataframe(filtered_df.head(50), use_container_width=True)

# Detailed analysis tables inside an expander
# This keeps the main interface clean while preserving analytical depth
with st.expander("Show Detailed Analysis Tables"):
    st.write("Category Performance")
    st.dataframe(category_df, use_container_width=True)

    st.write("Regional Performance")
    st.dataframe(region_df, use_container_width=True)

    st.write("Weekly Revenue Analysis")
    st.dataframe(weekly_df, use_container_width=True)

    st.write("Monthly Revenue Analysis")
    st.dataframe(monthly_df, use_container_width=True)