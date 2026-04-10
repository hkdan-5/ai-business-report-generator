import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate core business KPIs from the dataset.
    """

    total_revenue = df["sales"].sum()
    total_profit = df["profit"].sum()
    total_orders = len(df)
    avg_order_value = df["sales"].mean()

    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
    }


def revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate total revenue by product category.
    """

    category_sales = (
        df.groupby("category")["sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    return category_sales


def revenue_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate total revenue by region.
    """

    region_sales = (
        df.groupby("region")["sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    return region_sales


def weekly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate weekly revenue trends using order_date.
    """

    weekly = (
        df.set_index("order_date")
        .resample("W")["sales"]
        .sum()
        .reset_index()
    )

    weekly["growth_rate"] = weekly["sales"].pct_change()

    return weekly


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate monthly revenue trends.
    Pandas >=2.2 requires 'ME' instead of 'M'.
    """

    monthly = (
        df.set_index("order_date")
        .resample("ME")["sales"]
        .sum()
        .reset_index()
    )

    monthly["growth_rate"] = monthly["sales"].pct_change()

    return monthly