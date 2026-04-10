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


def run_pipeline():
    """
    Main pipeline for the AI Business Report Generator.

    The pipeline performs:
    - data loading
    - data cleaning
    - KPI calculation
    - category and regional analysis
    - weekly and monthly trend analysis
    - business insight generation
    - AI report generation via Ollama
    """

    # Load raw sales data
    df = load_sales_data("data/superstore_sales.csv")

    # Clean and prepare the dataset
    df = clean_sales_data(df)

    # Calculate core KPIs
    kpis = calculate_kpis(df)

    # Perform category and regional analysis
    category_df = revenue_by_category(df)
    region_df = revenue_by_region(df)

    # Perform time-based trend analysis
    weekly_df = weekly_revenue(df)
    monthly_df = monthly_revenue(df)

    # Generate structured business insights
    insights = generate_business_insights(
        kpis=kpis,
        category_df=category_df,
        region_df=region_df,
        weekly_df=weekly_df,
        monthly_df=monthly_df,
    )

    print("\n==============================")
    print("STRUCTURED BUSINESS INSIGHTS")
    print("==============================")
    print(insights)

    # Generate AI-written business report using local Ollama model
    report = generate_business_report(insights)

    print("\n==============================")
    print("AI BUSINESS REPORT")
    print("==============================")
    print(report)

    # Save generated report
    with open("outputs/business_report.txt", "w", encoding="utf-8") as file:
        file.write(report)


if __name__ == "__main__":
    run_pipeline()