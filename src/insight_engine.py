import pandas as pd


def generate_business_insights(
    kpis: dict,
    category_df: pd.DataFrame,
    region_df: pd.DataFrame,
    weekly_df: pd.DataFrame,
    monthly_df: pd.DataFrame,
) -> str:
    """
    Generate human-readable business insights from analytical results.

    This function converts numerical results into textual insights that
    can later be passed to a language model to generate an executive report.
    """

    # best and worst category
    best_category = category_df.iloc[0]["category"]
    worst_category = category_df.iloc[-1]["category"]

    # best region
    best_region = region_df.iloc[0]["region"]

    # latest weekly growth
    latest_week = weekly_df.iloc[-1]
    weekly_growth = latest_week["growth_rate"]

    # latest monthly growth
    latest_month = monthly_df.iloc[-1]
    monthly_growth = latest_month["growth_rate"]

    # interpret weekly trend
    if weekly_growth > 0:
        weekly_trend = f"Weekly revenue increased by {weekly_growth*100:.2f}%."
    else:
        weekly_trend = f"Weekly revenue declined by {abs(weekly_growth*100):.2f}%."

    # interpret monthly trend
    if monthly_growth > 0:
        monthly_trend = f"Monthly revenue increased by {monthly_growth*100:.2f}%."
    else:
        monthly_trend = f"Monthly revenue declined by {abs(monthly_growth*100):.2f}%."

    insights = f"""
Business Insights

Total Revenue: {kpis['total_revenue']:.2f}
Total Profit: {kpis['total_profit']:.2f}
Average Order Value: {kpis['avg_order_value']:.2f}

Top Performing Category: {best_category}
Lowest Performing Category: {worst_category}

Top Performing Region: {best_region}

Trend Analysis
{weekly_trend}
{monthly_trend}
"""

    return insights