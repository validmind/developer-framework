import pandas as pd
import numpy as np
import re
import scorecardpy as sc
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

from notebooks.probability_of_default.helpers.model_development import *


def import_data(params):
    source = params["source"]
    # print("Importing raw data from: %s", source)

    df_out = pd.read_csv(source)
    log_df_info(df_out, "Import Data")

    return df_out


def data_preparation(df, params):
    for key, value in params.items():
        print(f"{key}: {value}")

    features_to_drop = params["features_to_drop"]
    default_column = params["default_column"]
    min_missing_percentage = params["min_missing_percentage"]
    iqr_threshold = params["iqr_threshold"]

    # Initial DataFrame details
    print("\nInitial DataFrame:")
    print(f"Number of columns: {df.shape[1]}")
    print(f"Columns: {', '.join(df.columns)}")

    # Drop specified features and display the result
    drop_features(df, features_to_drop)
    print(f"\nAfter dropping specified features:")
    print(f"Number of columns: {df.shape[1]}")
    print(f"Columns: {', '.join(df.columns)}")

    # Add default definition and display results
    add_default_definition(df, default_column)
    print(f"\nAfter adding default definition for column '{default_column}':")
    print(f"Number of columns: {df.shape[1]}")

    # Remove features based on missing values and display results
    remove_features_missing_values(df, min_missing_percentage)
    print(
        f"\nAfter removing features based on missing values (threshold: {min_missing_percentage * 100}%):"
    )
    print(f"Number of columns: {df.shape[1]}")
    print(f"Columns: {', '.join(df.columns)}")

    # Convert term column and display results
    convert_term_column(df)
    print("\nAfter converting 'term' column:")

    # Convert employment length column and display results
    convert_emp_length_column(df)
    print("\nAfter converting 'emp_length' column:")

    # Convert inq_last_6mths column and display results
    convert_inq_last_6mths_column(df)
    print("\nAfter modifying 'inq_last_6mths' column values:")

    # Remove outliers based on IQR for a certain column and display results
    remove_iqr_outliers(df, default_column, iqr_threshold)
    print(
        f"\nAfter removing outliers based on IQR for column '{default_column}' (threshold: {iqr_threshold}):"
    )
    print(f"Remaining rows: {len(df)}")

    print("\nData Preparation Complete:")
    print(f"Final number of columns: {df.shape[1]}")
    print(f"Columns: {', '.join(df.columns)}")

    return df


def data_split(df, params):
    df_out = df.copy()

    target_column = params["target_column"]
    test_size = params["test_size"]

    # Split data into train and test
    X = df_out.drop(target_column, axis=1)
    y = df_out[target_column]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )

    print(f"Training data has {X_train.shape[0]} rows and {X_train.shape[1]} columns.")
    print(f"Test data has {X_test.shape[0]} rows and {X_test.shape[1]} columns.")

    # Concatenate X_train with y_train to form df_train
    df_train = pd.concat([X_train, y_train], axis=1)

    # Concatenate X_test with y_test to form df_test
    df_test = pd.concat([X_test, y_test], axis=1)

    # Logging
    log_df_info(df_train, "Training Data")
    log_df_info(df_test, "Test Data")

    return df_train, df_test


def feature_selection(df, params):
    df_out = df.copy()
    features_to_drop = params["features_to_drop"]

    drop_categories(df_out)

    # Drop the specified features
    if set(features_to_drop).issubset(df_out.columns):
        df_out.drop(features_to_drop, axis=1, inplace=True)

    else:
        missing_features = set(features_to_drop) - set(df_out.columns)
        print(
            f"The following features are not in the dataframe and cannot be dropped: {missing_features}"
        )

    # Logging
    log_df_info(df_out, "Feature Selection")

    return df_out


def feature_engineering(df, params):
    df_out = df.copy()

    target_column = params["target_column"]
    woe_breaks_adj = params["woe_breaks_adj"]

    df_out = convert_to_woe(df_out, target_column, woe_breaks_adj)

    # Logging
    log_df_info(df, "Feature Engineering")

    return df_out


# -------
def add_default_definition(df, default_column):
    # Direct modifications
    if "loan_status" not in df.columns:
        raise ValueError("'loan_status' column not found in the DataFrame.")

    df[default_column] = df["loan_status"].apply(
        lambda x: 0 if x == "Fully Paid" else 1 if x == "Charged Off" else np.nan
    )
    df.dropna(subset=[default_column], inplace=True)
    df[default_column] = df[default_column].astype(int)
    df.drop(columns=["loan_status"], inplace=True)


def convert_term_column(df):
    column = "term"
    if column not in df.columns:
        raise ValueError(f"The column '{column}' does not exist in the dataframe.")
    df[column] = df[column].str.replace(" months", "").astype("object")


def convert_emp_length_column(df):
    column = "emp_length"
    if column not in df.columns:
        raise ValueError(f"The column '{column}' does not exist in the dataframe.")
    df[column] = (
        df[column]
        .replace("n/a", np.nan)
        .str.replace("< 1 year", str(0))
        .apply(lambda x: re.sub("\D", "", str(x)))
        .astype("object")
    )


def convert_inq_last_6mths_column(df):
    column = "inq_last_6mths"
    if column not in df.columns:
        raise ValueError(f"The column '{column}' does not exist in the dataframe.")
    df[column] = df[column].astype("category")


def convert_to_woe(df, target_column, breaks_adj):
    df_out = df.copy()

    woe_df = woe_binning(df_out, target_column, breaks_adj)

    # Placeholder for the transformation function - you'll need to define or import it
    bins = transform_woe_df(woe_df)

    # Print how many features are getting transformed
    print(f"Converting {len(bins)} features to WoE values.")

    # Make sure we don't transform the target column
    if target_column in bins:
        del bins[target_column]
        print(f"Excluded {target_column} from WoE transformation.")

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


def apply_credit_scores(model, X, target_score, target_odds, pdo):
    X_copy = X.copy()
    beta = model.params.values
    alpha = model.params[0]
    factor = pdo / np.log(2)
    offset = target_score - (factor * np.log(target_odds))

    for _, row in X_copy.iterrows():
        score_i = 0
        for i in range(1, len(beta)):
            WoE_i = row[i]
            score_i += (beta[i] * WoE_i) * factor

        score_i += alpha * factor
        score_i += offset
        X_copy.loc[row.name, "score"] = score_i

    return X_copy


def drop_categories(df):
    df_out = df.copy()

    # Initial count
    initial_count = df_out.shape[0]

    # Select rows where purpose is 'debt_consolidation' or 'credit_card'
    df_out = df_out[df_out["purpose"].isin(["debt_consolidation", "credit_card"])]
    print(
        f"Rows retained with purpose 'debt_consolidation' or 'credit_card': {df_out.shape[0]}"
    )

    # Remove rows where grade is 'F' or 'G'
    df_out = df_out[~df_out["grade"].isin(["F", "G"])]
    print(f"Rows after removing grades 'F' or 'G': {df_out.shape[0]}")

    # Remove rows where sub_grade starts with 'F' or 'G'
    df_out = df_out[~df_out["sub_grade"].str.startswith(("F", "G"))]
    print(f"Rows after removing sub_grades starting with 'F' or 'G': {df_out.shape[0]}")

    # Remove rows where home_ownership is 'OTHER', 'NONE', or 'ANY'
    df_out = df_out[~df_out["home_ownership"].isin(["OTHER", "NONE", "ANY"])]
    print(
        f"Rows after removing home_ownership values 'OTHER', 'NONE', or 'ANY': {df_out.shape[0]}"
    )

    print(f"Total rows dropped: {initial_count - df_out.shape[0]}")

    return df_out


import statsmodels.api as sm


def model_training(df, params):
    target_column = params["target_column"]
    add_constant = params.get("add_constant", False)  # Default to False if not provided

    # Ensure that the target column is in the DataFrame
    if target_column not in df.columns:
        raise ValueError(f"'{target_column}' not found in DataFrame.")

    # Get X (features) and y (target) from df
    X = df.drop(target_column, axis=1)  # Drop the target column to get features

    # Add a constant to the model if required
    if add_constant:
        X = sm.add_constant(X)

    y = df[target_column]

    # Define the model
    model = sm.GLM(y, X, family=sm.families.Binomial())

    print(
        f"Training the model with {X.shape[1]} features and {X.shape[0]} data points."
    )

    # Fit the model
    model_fit = model.fit()

    print("GLM Logisitic Regression Model trained successfully.")

    return model_fit


def woe_binning(df, target_column, breaks_adj):
    """
    This function performs automatic binning using WoE.
    df: A pandas dataframe
    target_column: The target variable in quotes, e.g. 'target'
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
