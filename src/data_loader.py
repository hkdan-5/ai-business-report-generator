import pandas as pd


def load_sales_data(filepath: str) -> pd.DataFrame:
    """
    Load the sales dataset from a CSV file.

    As this is a public datasets downloaded from Kaggle its not encoded in UTF-8.
    Therefore we explicitly define the encoding to avoid
    UnicodeDecodeError during loading.
    """

    df = pd.read_csv(filepath, encoding="latin1")

    return df