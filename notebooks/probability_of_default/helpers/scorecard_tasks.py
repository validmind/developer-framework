import pandas as pd
import numpy as np
import re
import scorecardpy as sc


def add_default_definition(df, default_column):
    # Check if 'loan_status' is in the DataFrame
    if "loan_status" not in df.columns:
        raise ValueError("'loan_status' column not found in the DataFrame.")

    print("Converting 'loan_status' to target column...")
    # Assuming the column name is 'loan_status'
    df[default_column] = df["loan_status"].apply(
        lambda x: 0 if x == "Fully Paid" else 1 if x == "Charged Off" else np.nan
    )

    initial_row_count = df.shape[0]
    # Remove rows where the target column is NaN
    df = df.dropna(subset=[default_column])
    removed_rows = initial_row_count - df.shape[0]
    print(f"Removed {removed_rows} rows with undefined 'loan_status' values.")

    # Convert target column to integer
    df[default_column] = df[default_column].astype(int)
    print(
        f"Converted 'loan_status' to '{default_column}' and set its data type to integer."
    )

    # Remove the 'loan_status' column from the DataFrame
    df.drop(columns=["loan_status"], inplace=True)
    print("'loan_status' column has been removed from the DataFrame.")

    return df


def convert_term_column(df):
    """
    Function to remove 'months' string from the 'term' column and convert it to categorical
    """

    column = "term"

    # Ensure the column exists in the dataframe
    if column not in df.columns:
        raise ValueError(f"The column '{column}' does not exist in the dataframe.")

    df[column] = df[column].str.replace(" months", "")

    # Convert to categorical
    df[column] = df[column].astype("object")

    return df


def convert_emp_length_column(df):
    """
    Function to clean 'emp_length' column and convert it to categorical.
    """

    column = "emp_length"

    # Ensure the column exists in the dataframe
    if column not in df.columns:
        raise ValueError(f"The column '{column}' does not exist in the dataframe.")

    df[column] = df[column].replace("n/a", np.nan)
    df[column] = df[column].str.replace("< 1 year", str(0))
    df[column] = df[column].apply(lambda x: re.sub("\D", "", str(x)))
    df[column].fillna(value=0, inplace=True)

    # Convert to categorical
    df[column] = df[column].astype("object")

    return df


def convert_inq_last_6mths_column(df):
    """
    Function to convert 'inq_last_6mths' column into categorical.
    """
    column = "inq_last_6mths"

    # Ensure the column exists in the dataframe
    if column not in df.columns:
        raise ValueError(f"The column '{column}' does not exist in the dataframe.")

    # Convert to categorical
    df[column] = df[column].astype("category")

    return df


def convert_to_woe(df, woe_df, target_col):
    df_out = df.copy()

    # Placeholder for the transformation function - you'll need to define or import it
    bins = transform_woe_df(woe_df)

    # Print how many features are getting transformed
    print(f"Converting {len(bins)} features to WoE values.")

    # Make sure we don't transform the target column
    if target_col in bins:
        del bins[target_col]
        print(f"Excluded {target_col} from WoE transformation.")

    # Apply the WoE transformation
    df_out = sc.woebin_ply(df_out, bins=bins)

    print(f"Successfully converted features to WoE values.")

    return df_out


def transform_woe_df(woe_df):
    # Select and rename columns
    transformed_df = woe_df[
        [
            "variable",
            "bin",
            "count",
            "count_distr",
            "good",
            "bad",
            "badprob",
            "woe",
            "bin_iv",
            "total_iv",
        ]
    ].copy()
    transformed_df.rename(columns={"bin_iv": "total_iv"}, inplace=True)

    # Create 'is_special_values' column (assuming there are no special values)
    transformed_df["is_special_values"] = False

    # Transform 'bin' column into interval format and store it in 'breaks' column
    transformed_df["breaks"] = transformed_df["bin"].apply(
        lambda x: "[-inf, %s)" % x if isinstance(x, float) else "[%s, inf)" % x
    )

    # Group by 'variable' to create bins dictionary
    bins = {}
    for variable, group in transformed_df.groupby("variable"):
        bins[variable] = group

    return bins
