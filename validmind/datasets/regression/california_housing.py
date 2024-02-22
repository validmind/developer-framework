# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import os

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

current_path = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_path, "datasets")

feature_columns = ["HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup"]
target_column = "MedHouseVal"


def load_data(full_dataset=False):
    california_housing = fetch_california_housing(as_frame=True)
    df = california_housing.data[feature_columns]
    df = df.copy()
    df[target_column] = california_housing.target.values

    return df


def preprocess(df):
    df = df.copy()

    train_val_df, test_df = train_test_split(df, test_size=0.20)

    # This guarantees a 60/20/20 split
    train_df, validation_df = train_test_split(train_val_df, test_size=0.25)

    return train_df, validation_df, test_df
