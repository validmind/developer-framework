# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import os

import numpy as np
import pandas as pd
import scorecardpy as sc
import statsmodels.api as sm
from sklearn.model_selection import train_test_split

current_path = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_path, "datasets")

# URLs or file paths for online and offline data
online_data_file = "https://vmai.s3.us-west-1.amazonaws.com/datasets/lending_club_loan_data_2007_2014.csv"
offline_data_file = os.path.join(
    dataset_path, "lending_club_loan_data_2007_2014_clean.csv.gz"
)

target_column = "loan_status"

drop_columns = [
    "Unnamed: 0",
    "id",
    "member_id",
    "funded_amnt",
    "emp_title",
    "url",
    "desc",
    "application_type",
    "title",
    "zip_code",
    "delinq_2yrs",
    "mths_since_last_delinq",
    "mths_since_last_record",
    "mths_since_last_major_derog",
    "revol_bal",
    "total_rec_prncp",
    "total_rec_late_fee",
    "recoveries",
    "out_prncp_inv",
    "out_prncp",
    "collection_recovery_fee",
    "next_pymnt_d",
    "initial_list_status",
    "pub_rec",
    "collections_12_mths_ex_med",
    "policy_code",
    "acc_now_delinq",
    "pymnt_plan",
    "tot_coll_amt",
    "tot_cur_bal",
    "total_rev_hi_lim",
    "last_pymnt_d",
    "last_credit_pull_d",
    "earliest_cr_line",
    "issue_d",
    "addr_state",
    "dti",
    "revol_util",
    "total_pymnt_inv",
    "inq_last_6mths",
    "total_rec_int",
    "last_pymnt_amnt",
]

drop_features = [
    "loan_amnt",
    "funded_amnt_inv",
    "total_pymnt",
]

categorical_variables = [
    "term",
    "grade",
    "sub_grade",
    "emp_length",
    "home_ownership",
    "verification_status",
    "purpose",
]

breaks_adj = {
    "loan_amnt": [5000, 10000, 15000, 20000, 25000],
    "int_rate": [10, 15, 20],
    "annual_inc": [50000, 100000, 150000],
}

score_params = {
    "target_score": 600,
    "target_odds": 50,
    "pdo": 20,
}


def load_data(source="online"):
    """
    Load data from either an online source or offline files, automatically dropping specified columns for offline data.

    :param source: 'online' for online data, 'offline' for offline files. Defaults to 'online'.
    :return: DataFrame containing the loaded data.
    """

    if source == "online":
        print(f"Loading data from an online source: {online_data_file}")
        df = pd.read_csv(online_data_file)
        df = _clean_data(df)

    elif source == "offline":
        print(f"Loading data from an offline .gz file: {offline_data_file}")
        # Since we know the offline_data_file path ends with '.zip', we replace it with '.csv.gz'
        gzip_file_path = offline_data_file.replace(".zip", ".csv.gz")
        print(f"Attempting to read from .gz file: {gzip_file_path}")
        # Read the CSV file directly from the .gz archive
        df = pd.read_csv(gzip_file_path, compression="gzip")
        print("Data loaded successfully.")
    else:
        raise ValueError("Invalid source specified. Choose 'online' or 'offline'.")

    print(
        f"Rows: {df.shape[0]}, Columns: {df.shape[1]}, Missing values: {df.isnull().sum().sum()}"
    )
    return df


def _clean_data(df):
    df = df.copy()

    # Drop columns not relevant for application scorecards
    df = df.drop(columns=drop_columns)

    # Drop rows with missing target values
    df.dropna(subset=[target_column], inplace=True)
    print("Dropping rows with missing target values:")
    print(
        f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nMissing values: {df.isnull().sum().sum()}\n"
    )

    # Drop columns with more than N percent missing values
    missing_values = df.isnull().mean()
    df = df.loc[:, missing_values < 0.7]
    print("Dropping columns with more than 70% missing values:")
    print(
        f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nMissing values: {df.isnull().sum().sum()}\n"
    )

    # Drop columns with only one unique value
    unique_values = df.nunique()
    df = df.loc[:, unique_values > 1]
    print("Dropping columns with only one unique value:")
    print(
        f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nMissing values: {df.isnull().sum().sum()}\n"
    )

    # Define the target variable for the model, representing loan default status.
    df[target_column] = df[target_column].map({"Fully Paid": 0, "Charged Off": 1})

    # Drop rows with NaN in target_column after mapping
    df.dropna(subset=[target_column], inplace=True)
    print("Dropping rows with missing target values:")
    print(
        f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nMissing values: {df.isnull().sum().sum()}\n"
    )

    return df


def preprocess(df):
    df = df.copy()

    # Convert the target variable to integer type for modeling.
    df[target_column] = df[target_column].astype(int)

    # Keep rows where purpose is 'debt_consolidation' or 'credit_card'
    df = df[df["purpose"].isin(["debt_consolidation", "credit_card"])]
    print("Filtering 'purpose' to 'debt_consolidation' and 'credit_card':")
    print(
        f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nMissing values: {df.isnull().sum().sum()}\n"
    )

    # Remove rows where grade is 'F' or 'G'
    df = df[~df["grade"].isin(["F", "G"])]
    print("Filtering out 'grade' F and G:")
    print(
        f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nMissing values: {df.isnull().sum().sum()}\n"
    )

    # Remove rows where sub_grade starts with 'F' or 'G'
    df = df[~df["sub_grade"].str.startswith(("F", "G"))]
    print("Filtering out 'sub_grade' F and G:")
    print(
        f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nMissing values: {df.isnull().sum().sum()}\n"
    )

    # Remove rows where home_ownership is 'OTHER', 'NONE', or 'ANY'
    df = df[~df["home_ownership"].isin(["OTHER", "NONE", "ANY"])]
    print("Filtering out 'home_ownership' OTHER, NONE, ANY:")
    print(
        f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nMissing values: {df.isnull().sum().sum()}\n"
    )

    # Drop features that are not useful for modeling
    df.drop(drop_features, axis=1, inplace=True)
    print("Dropping specified features:")
    print(
        f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nMissing values: {df.isnull().sum().sum()}\n"
    )

    # Drop rows with missing values
    df.dropna(inplace=True)
    print("Dropping rows with any missing values:")
    print(
        f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nMissing values: {df.isnull().sum().sum()}\n"
    )

    # Preprocess emp_length column
    df = _preprocess_emp_length(df)

    # Preprocess term column
    df = _preprocess_term(df)

    return df


def _preprocess_term(df):
    df = df.copy()

    # Remove ' months' and convert to integer
    df["term"] = df["term"].str.replace(" months", "").astype(object)

    return df


def _preprocess_emp_length(df):
    df = df.copy()

    # Mapping string values to numbers
    emp_length_map = {
        "10+ years": 10,
        "< 1 year": 0,
        "1 year": 1,
        "2 years": 2,
        "3 years": 3,
        "4 years": 4,
        "5 years": 5,
        "6 years": 6,
        "7 years": 7,
        "8 years": 8,
        "9 years": 9,
    }

    # Apply the mapping to the emp_length column
    df["emp_length"] = df["emp_length"].map(emp_length_map).astype(object)

    # Drop rows where emp_length is NaN after mapping
    # df.dropna(subset=["emp_length"], inplace=True)

    return df


def feature_engineering(df):
    df = df.copy()

    # WoE encoding of numerical and categorical features
    df = woe_encoding(df)

    print(
        f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nMissing values: {df.isnull().sum().sum()}\n"
    )

    return df


def woe_encoding(df):
    df = df.copy()

    woe = _woebin(df)
    bins = _woe_to_bins(woe)

    # Make sure we don't transform the target column
    if target_column in bins:
        del bins[target_column]
        print(f"Excluded {target_column} from WoE transformation.")

    # Apply the WoE transformation
    df = sc.woebin_ply(df, bins=bins)

    print("Successfully converted features to WoE values.")

    return df


def _woe_to_bins(woe):
    # Select and rename columns
    transformed_df = woe[
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


def _woebin(df):
    """
    This function performs automatic binning using WoE.
    df: A pandas dataframe
    target_column: The target variable in quotes, e.g. 'loan_status'
    """

    non_numeric_cols = df.select_dtypes(exclude=["int64", "float64"]).columns
    df[non_numeric_cols] = df[non_numeric_cols].astype(str)

    try:
        print(
            f"Performing binning with breaks_adj: {breaks_adj}"
        )  # print the breaks_adj being used
        bins = sc.woebin(df, target_column, breaks_list=breaks_adj)
    except Exception as e:
        print("Error during binning: ")
        print(e)
    else:
        bins_df = pd.concat(bins.values(), keys=bins.keys())
        bins_df.reset_index(inplace=True)
        bins_df.drop(columns=["variable"], inplace=True)
        bins_df.rename(columns={"level_0": "variable"}, inplace=True)

        bins_df["bin_number"] = bins_df.groupby("variable").cumcount()

        return bins_df


def split(df, add_constant=False):
    df = df.copy()

    # Splitting the dataset into training and test sets
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    if add_constant:
        # Add a constant to the model for both training and testing datasets
        train_df = sm.add_constant(train_df)
        test_df = sm.add_constant(test_df)

    # Calculate and print details for the training dataset
    print("After splitting the dataset into training and test sets:")
    print(
        f"Training Dataset:\nRows: {train_df.shape[0]}\nColumns: {train_df.shape[1]}\nMissing values: {train_df.isnull().sum().sum()}\n"
    )

    # Calculate and print details for the test dataset
    print(
        f"Test Dataset:\nRows: {test_df.shape[0]}\nColumns: {test_df.shape[1]}\nMissing values: {test_df.isnull().sum().sum()}\n"
    )

    return train_df, test_df


def compute_scores(probabilities):

    target_score = score_params["target_score"]
    target_odds = score_params["target_odds"]
    pdo = score_params["pdo"]

    factor = pdo / np.log(2)
    offset = target_score - (factor * np.log(target_odds))

    scores = offset + factor * np.log(probabilities / (1 - probabilities))

    return scores
