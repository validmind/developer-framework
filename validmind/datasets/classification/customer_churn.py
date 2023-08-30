# Copyright © 2023 ValidMind Inc. All rights reserved.
import os

import pandas as pd
from sklearn.model_selection import train_test_split

from . import (
    simple_preprocess_booleans,
    simple_preprocess_categoricals,
    simple_preprocess_numericals,
)

current_path = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_path, "datasets")

drop_columns = ["RowNumber", "CustomerId", "Surname"]
boolean_columns = ["Gender"]
categorical_columns = ["Geography"]

target_column = "Exited"
class_labels = {
    "0": "Did not exit",
    "1": "Exited",
}


def load_data(full_dataset=False):
    data_file = os.path.join(dataset_path, "bank_customer_churn.csv")
    df = pd.read_csv(data_file)

    # Drop these unnecessary columns when loading since they won't be
    # helpful for showing data quality issues
    if full_dataset is False:
        df.drop(drop_columns, axis=1, inplace=True)

    return df


def preprocess(df):
    df = df.copy()
    df = simple_preprocess_booleans(df, boolean_columns)
    df = simple_preprocess_categoricals(df, categorical_columns)
    numerical_columns = [
        col
        for col in df.columns
        if col not in boolean_columns + categorical_columns + [target_column]
    ]
    df = simple_preprocess_numericals(df, numerical_columns)

    train_val_df, test_df = train_test_split(df, test_size=0.20)

    # This guarantees a 60/20/20 split
    train_df, validation_df = train_test_split(train_val_df, test_size=0.25)

    return train_df, validation_df, test_df
