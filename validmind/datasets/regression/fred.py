import os
import pickle
import pandas as pd

current_path = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(
    current_path, "..", "..", "..", "notebooks", "datasets", "time_series"
)

models_path = os.path.join(
    current_path, "..", "..", "..", "notebooks", "models", "time_series"
)


file = "../datasets/time_series/fred_loan_rates_test_1.csv"


target_column = "MORTGAGE30US"
feature_columns = ["FEDFUNDS", "GS10", "UNRATE"]
frequency = "MS"
split_option = "train_test"
transform_func = "diff"


def load_data():
    data_file = os.path.join(dataset_path, "fred_loan_rates.csv")
    df = pd.read_csv(data_file, parse_dates=["DATE"], index_col="DATE")
    df = df[[target_column] + feature_columns]
    return df


def preprocess(df, split_option="train_test_val", train_size=0.6, test_size=0.2):
    """
    Split a time series DataFrame into train, validation, and test sets.

    Parameters:
        df (pandas.DataFrame): The time series DataFrame to be split.
        split_option (str): The split option to choose from: 'train_test_val' (default) or 'train_test'.
        train_size (float): The proportion of the dataset to include in the training set. Default is 0.6.
        test_size (float): The proportion of the dataset to include in the test set. Default is 0.2.

    Returns:
        train_df (pandas.DataFrame): The training set.
        validation_df (pandas.DataFrame): The validation set (only returned if split_option is 'train_test_val').
        test_df (pandas.DataFrame): The test set.

    """
    # Sort the DataFrame by the time column (assuming the time column is the index)
    df = df.sort_index()

    if split_option == "train_test_val":
        # Split the DataFrame into train, validation, and test sets
        train_size = int(len(df) * train_size)
        val_size = int(len(df) * test_size)

        train_df = df.iloc[:train_size]
        validation_df = df.iloc[train_size : train_size + val_size]
        test_df = df.iloc[train_size + val_size :]

        return train_df, validation_df, test_df

    elif split_option == "train_test":
        # Split the DataFrame into train and test sets
        train_size = int(len(df) * train_size)

        train_df = df.iloc[:train_size]
        test_df = df.iloc[train_size:]

        return train_df, test_df

    else:
        raise ValueError(
            "Invalid split_option. Must be 'train_test_val' or 'train_test'."
        )


def transform(df, transform_func="diff"):
    if transform_func == "diff":
        df = df.diff().dropna()
    return df


def load_models():
    model_files = os.listdir(models_path)

    models = {}

    for model_file in model_files:
        if model_file.endswith(".pkl"):
            model_name = os.path.splitext(model_file)[0]
            with open(os.path.join(models_path, model_file), "rb") as f:
                models[model_name] = pickle.load(f)
    return models


def load_test_dataset():
    data_file = os.path.join(dataset_path, "fred_loan_rates_test_1.csv")
    df = pd.read_csv(data_file, parse_dates=["DATE"], index_col="DATE")
    df = df.diff().dropna()
    return df


def load_train_dataset():
    model_file = os.path.join(models_path, "fred_loan_rates_model_5.pkl")

    with open(os.path.join(models_path, model_file), "rb") as f:
        model_fit = pickle.load(f)

    # Extract the endogenous (target) variable from the model
    train_df = pd.Series(model_fit.model.endog, index=model_fit.model.data.row_labels)
    train_df = train_df.to_frame()
    target_var_name = model_fit.model.endog_names
    train_df.columns = [target_var_name]

    # Extract the exogenous (explanatory) variables from the model
    exog_df = pd.DataFrame(
        model_fit.model.exog,
        index=model_fit.model.data.row_labels,
        columns=model_fit.model.exog_names,
    )

    # Concatenate the endogenous (target) and exogenous (explanatory) variables
    train_df = pd.concat([train_df, exog_df], axis=1)

    return train_df
