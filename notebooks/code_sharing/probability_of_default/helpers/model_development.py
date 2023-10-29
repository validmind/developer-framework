import pandas as pd
import numpy as np
import datetime
import pickle
import statsmodels.api as sm
import logging


def save_model(model, df, base_filename):
    """Save a model and a dataframe with a timestamp in the filename"""
    # Get current date and time
    now = datetime.datetime.now()

    # Convert the current date and time to string
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")

    filename = f"{base_filename}_{timestamp_str}.pkl"

    # Save the model and dataframe
    with open(filename, "wb") as file:
        pickle.dump((model, df), file)

    print(f"Model and dataframe saved as {filename}")


def get_numerical_columns(df):
    numerical_columns = df.select_dtypes(
        include=["int", "float", "uint"]
    ).columns.tolist()
    return numerical_columns


def get_categorical_columns(df):
    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    return categorical_columns


def get_features_with_min_missing(df, min_missing_fraction):
    """Calculate columns where the fraction of missing values exceeds the given threshold."""
    # Calculate the fraction of missing values in each column
    missing_fractions = df.isnull().mean()

    # Get the variables where the fraction of missing values is greater than the specified minimum
    variables_to_drop = missing_fractions[
        missing_fractions > min_missing_fraction
    ].index.tolist()

    # Also add any columns where all values are missing
    variables_to_drop.extend(df.columns[df.isnull().all()].tolist())

    # Remove duplicates (if any)
    variables_to_drop = list(set(variables_to_drop))

    return variables_to_drop


def remove_features_missing_values(df, min_missing_fraction):
    """Drop columns with missing values exceeding a certain fraction."""

    print("Analyzing missing values in the dataset...")

    vars_to_drop = get_features_with_min_missing(df, min_missing_fraction)

    if vars_to_drop:
        print(
            f"Found {len(vars_to_drop)} features with more than {min_missing_fraction * 100}% missing values."
        )
        print("Dropping the following columns:", ", ".join(vars_to_drop))
        df.drop(columns=vars_to_drop, inplace=True)
    else:
        print(
            f"No features found with more than {min_missing_fraction * 100}% missing values."
        )


def add_constant(df):
    df_out = df.copy()

    # Before adding constant
    initial_cols = df_out.shape[1]

    # Add constant
    df_out = sm.add_constant(df_out)

    # After adding constant
    after_add_cols = df_out.shape[1]

    print(
        f"Added constant to dataframe. Number of columns went from {initial_cols} to {after_add_cols}."
    )

    return df_out


def remove_iqr_outliers(df, target_column, threshold=1.5):
    df_out = df.copy()

    if target_column not in df.columns:
        raise ValueError(f"{target_column} is not a column in the DataFrame.")
    if not np.issubdtype(df[target_column].dtype, np.number):
        raise ValueError(f"{target_column} is not a numerical column.")

    num_cols = df_out.select_dtypes(include=[np.number]).columns.tolist()
    num_cols.remove(target_column)  # Exclude target_column from numerical columns
    for col in num_cols:
        outliers = compute_outliers(df_out[col], threshold)
        df_out = df_out[~df_out[col].isin(outliers)]
    return df_out


def compute_outliers(series, threshold=1.5):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    return series[(series < lower_bound) | (series > upper_bound)]


def drop_features(df, to_drop):
    df.drop(columns=to_drop, axis=1, inplace=True)


# Setup logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_df_info(df, df_name):
    """
    Log details about a DataFrame including column names, number of rows,
    number of columns, data types of each column, and number of missing values.

    Args:
    - df (pd.DataFrame): The DataFrame to log details about.
    - df_name (str): A name or description of the DataFrame to include in the log.
    """

    logging.info(f"Details of {df_name}:")
    logging.info(f"Columns: {df.columns.tolist()}")
    logging.info(f"Number of Rows: {df.shape[0]}")
    logging.info(f"Number of Columns: {df.shape[1]}")
    logging.info(f"Data Types: {df.dtypes.to_dict()}")
    logging.info(f"Total Missing Values: {df.isnull().sum().sum()}")
