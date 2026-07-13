import pandas as pd


def successful_logins_per_user(df) -> dict:
    """
    Counts the number of successful logins for each user in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing log data.

    Returns:
        dict: A dictionary with users as keys and their successful login counts as values.
    """
    successful_logins = df[(df["action"] == "LOGIN") & (df["level"] == "INFO")]
    return successful_logins["user"].value_counts().to_dict()


def ips_per_user(df) -> dict:
    """
    Retrieves the unique IP addresses associated with each user in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing log data.

    Returns:
        dict: A dictionary with users as keys and a list of their unique IP addresses as values.
    """
    return df.groupby("user")["ip"].unique().apply(list).to_dict()


def filter_entries(df, **kwargs) -> pd.DataFrame:
    """
    Filters the DataFrame based on provided keyword arguments.

    Args:
        df (pd.DataFrame): The DataFrame containing log data.
        **kwargs: Column-value pairs to filter the DataFrame.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    for key, value in kwargs.items():
        df = df[df[key] == value]
    return df
