import pandas as pd
import numpy as np
import datetime
import pickle
from sklearn.model_selection import train_test_split
import statsmodels.api as sm


def import_raw_data(source):
    print("Importing raw data from:", source)
    df_out = pd.read_csv(source)
    print(
        f"Data imported successfully with {df_out.shape[0]} rows and {df_out.shape[1]} columns."
    )
    return df_out


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


def remove_features_missing_values(df, min_missing_percentage):
    """Drop columns with missing values exceeding a certain percentage."""

    def get_features_with_min_missing(data, threshold_percentage):
        """Get features with missing values above the given threshold."""
        missing_percent = data.isnull().mean() * 100
        return missing_percent[missing_percent > threshold_percentage].index.tolist()

    print("Analyzing missing values in the dataset...")
    vars_to_drop = get_features_with_min_missing(df, min_missing_percentage)

    if vars_to_drop:
        print(
            f"Found {len(vars_to_drop)} features with more than {min_missing_percentage}% missing values."
        )
        print("Dropping the following columns:", ", ".join(vars_to_drop))
        return df.drop(columns=vars_to_drop)
    else:
        print(
            f"No features found with more than {min_missing_percentage}% missing values."
        )
        return df


def get_features_with_min_missing(df, min_missing_percentage):
    # Calculate the percentage of missing values in each column
    missing_percentages = df.isnull().mean() * 100

    # Get the variables where the percentage of missing values is greater than the specified minimum
    variables_to_drop = missing_percentages[
        missing_percentages > min_missing_percentage
    ].index.tolist()

    # Also add any columns where all values are missing
    variables_to_drop.extend(df.columns[df.isnull().all()].tolist())

    # Remove duplicates (if any)
    variables_to_drop = list(set(variables_to_drop))

    return variables_to_drop


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
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    num_cols.remove(target_column)  # Exclude target_column from numerical columns
    for col in num_cols:
        outliers = compute_outliers(df[col], threshold)
        df = df[~df[col].isin(outliers)]
    return df


def compute_outliers(series, threshold=1.5):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    return series[(series < lower_bound) | (series > upper_bound)]


def train_model(df, target_column):
    # Ensure that the target column is in the DataFrame
    if target_column not in df.columns:
        raise ValueError(f"'{target_column}' not found in DataFrame.")

    # Get X (features) and y (target) from df
    X = df.drop(target_column, axis=1)  # Drop the target column to get features
    y = df[target_column]

    # Define the model
    model = sm.GLM(y, X, family=sm.families.Binomial())

    print(
        f"Training the model with {X.shape[1]} features and {X.shape[0]} data points."
    )

    # Fit the model
    model_fit = model.fit()

    print("Model trained successfully.")

    return model_fit


def drop_features(df, to_drop):
    df_out = df.copy()

    # Before dropping
    initial_cols = df_out.shape[1]

    df_out.drop(columns=to_drop, axis=1, inplace=True)

    # After dropping
    after_drop_cols = df_out.shape[1]

    print(f"Dropped {initial_cols - after_drop_cols} columns.")
    print(f"Columns remaining after dropping: {after_drop_cols}")

    return df_out


def data_split(df, target_column):
    df_out = df.copy()

    # Split data into train and test
    X = df_out.drop(target_column, axis=1)
    y = df_out[target_column]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training data has {X_train.shape[0]} rows and {X_train.shape[1]} columns.")
    print(f"Test data has {X_test.shape[0]} rows and {X_test.shape[1]} columns.")

    # Concatenate X_train with y_train to form df_train
    df_train = pd.concat([X_train, y_train], axis=1)

    # Concatenate X_test with y_test to form df_test
    df_test = pd.concat([X_test, y_test], axis=1)

    return df_train, df_test
