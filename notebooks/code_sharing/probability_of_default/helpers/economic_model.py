from validmind.datasets.regression import fred as fred
import statsmodels.api as sm


def import_data():
    df = fred.load_all_data()

    # Combining the target column with feature columns
    selected_columns = [
        "DRSFRMACBS",
        "GS3",
        "GS5",
        "GS10",
        "GDPC1",
        "UNRATE",
        "CPIAUCSL",
        "FEDFUNDS",
        "CSUSHPISA",
    ]

    # Filtering the dataframe to only have the desired columns
    df = df[selected_columns]

    return df


def data_preparation(df, params):
    """
    Prepare the time series data by filtering, resampling, removing missing values, and taking first differences.

    Args:
    - df: Raw time series dataframe.
    - params (dict): Dictionary containing preparation parameters such as 'end_date' and 'resample_freq'.

    Returns:
    - df_prepared: Processed dataframe.
    """

    # Copy the raw dataframe
    df_out = df.copy()

    # Remove data beyond specified end_date (e.g., to avoid COVID years)
    df_out = df_out[df_out.index <= params["end_date"]]

    # Resample frequencies (e.g., to Monthly)
    df_out = df_out.resample(params["resample_freq"]).last()

    # Remove all missing values
    df_out = df_out.dropna()

    # Take the first difference across all variables
    df_out = df_out.diff().dropna()

    return df_out


def data_split(df, params):
    """
    Split the time series dataframe into training and test sets based on the given percentage for the test set.

    Args:
    - df: Time series dataframe.
    - test_pct: Percentage of data to use for testing. E.g., 0.2 for 20%.

    Returns:
    - df_train: Training dataframe.
    - df_test: Test dataframe.
    """

    # Ensure the data frame is sorted by date
    df = df.sort_index()

    # Retrieve the test_pct from params
    test_pct = params["test_pct"]

    # Calculate the index to split on based on the given percentage
    split_idx = int(len(df) * (1 - test_pct))
    split_date = df.iloc[split_idx].name

    # Split the data frame
    df_train = df[df.index < split_date]
    df_test = df[df.index >= split_date]

    return df_train, df_test


def model_training(df, params):
    # Convert the target column to a list if it's a string
    target_column = params["target_column"]
    if isinstance(target_column, str):
        target_column = [target_column]

    # Check if the target column(s) is(are) in the DataFrame
    if not set(target_column).issubset(df.columns):
        missing_columns = set(target_column) - set(df.columns)
        raise ValueError(f"Columns {missing_columns} not found in DataFrame.")

    # Get X (features) and y (target) from df
    X = df.drop(target_column, axis=1)  # Drop the target column to get features
    y = df[target_column]

    # Define the model
    model = sm.OLS(y, X)

    print(
        f"Training the model with {X.shape[1]} features and {X.shape[0]} data points."
    )

    # Fit the model
    model_fit = model.fit()

    print("OLS Regression Model trained successfully.")

    return model_fit
