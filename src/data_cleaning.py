import pandas as pd


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic cleaning on the sales dataset.

    Operations
    ----------
    - Standardize column names
    - Convert order date to datetime
    - Remove rows with missing sales values
    """

    # normalize column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # convert date column
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"])

    # remove rows with missing sales
    if "sales" in df.columns:
        df = df.dropna(subset=["sales"])

    return df