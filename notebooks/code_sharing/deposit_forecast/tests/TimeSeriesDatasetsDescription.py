# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd
import numpy as np


def TimeSeriesDatasetsDescription(datasets):
    """
    Time Series Datasets Description
    """

    description = []

    for dataset in datasets:
        df = dataset.df
        target_column = dataset.target_column
        dataset_name = dataset.input_id

        metrics = _extract_dataset_metrics(df, dataset_name, target_column)
        description.append(metrics)

    description_df = pd.DataFrame(description)
    return description_df


def _extract_dataset_metrics(df, dataset_name, target_column):
    # Infer frequency for each column
    inferred_frequencies = [pd.infer_freq(df.index)] * df.shape[1]

    metrics = {
        "Dataset": dataset_name,
        "Target Column": target_column,
        "Total Missing Values": df.isnull().sum().sum(),
        "Total Rows": df.shape[0],
        "Total Columns": df.shape[1],
        "Number of Unique Dates": df.index.nunique(),
        "Date Range Start": df.index.min().strftime("%Y-%m-%d"),
        "Date Range End": df.index.max().strftime("%Y-%m-%d"),
        "Frequencies": inferred_frequencies,
    }

    return metrics
