# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd


def TimeSeriesTargetVariableDescription(datasets):
    """
    Target Variable Description
    """

    description = []

    for dataset in datasets:
        df = dataset.df
        target_column = dataset.target_column
        dataset_name = dataset.input_id

        metrics = _extract_target_variable_metrics(df, dataset_name, target_column)
        description.append(metrics)

    description_df = pd.DataFrame(description)
    return description_df


def _extract_target_variable_metrics(df, dataset_name, target_column):
    metrics = {
        "Dataset": dataset_name,
        "Target Variable": target_column,
        "Start Date": df.index.min().strftime("%Y-%m-%d"),
        "End Date": df.index.max().strftime("%Y-%m-%d"),
        "Max": df[target_column].max(),
        "Min": df[target_column].min(),
        "Number of Missing Values": df[target_column].isnull().sum(),
        "Count": df[target_column].notnull().sum(),
        "Mean": df[target_column].mean(),
        "Median": df[target_column].median(),
        "Standard Deviation": df[target_column].std(),
    }

    return metrics
