# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd
import plotly.graph_objects as go

from validmind import tags, tasks


@tags("time_series_data", "visualization")
@tasks("regression")
def TimeSeriesDatasetAnalysis(datasets):
    """
    Generates a detailed analysis and line plots for each individual time series in the provided datasets.

    **Purpose**: The purpose of the TimeSeriesDatasetAnalysis function is to visualize and analyze multiple individual time series
    by generating line plots for each dataset and providing a summary of key statistics. This helps in understanding trends, patterns,
    and data quality issues within each time series independently.

    **Test Mechanism**: The function iterates through each dataset, extracts the time series data, and generates a line
    plot using Plotly. Each dataset is expected to have a datetime index. The function checks this and raises an error if
    the index is not in datetime format. For each dataset, all its variables (columns) are plotted in the same figure with
    appropriate legends indicating the variables. Additionally, the function calculates and records the start date, end date,
    frequency, number of missing values, and count of data points for each variable in the datasets.

    **Signs of High Risk**:
    - If the index of the dataset is not in datetime format, it could lead to errors in time-series analysis and hinder
      the generation of accurate plots.
    - Inconsistent or missing data within the datasets might affect the visual representation of trends and patterns.

    **Strengths**:
    - This function provides a clear and intuitive visualization of each individual time series, making it easier to
      analyze trends and patterns.
    - Including legends in each plot helps in identifying the variables being plotted, enhancing the interpretability of
      the plots.
    - The function provides a comprehensive summary of key statistics for each variable, helping to identify data quality
      issues such as missing values.
    - The function caters to visual learners by providing an immediate visual representation of the data.

    **Limitations**:
    - This function assumes that the datasets are provided as DataFrameDataset objects with a .df attribute to access
      the pandas DataFrame.
    - It only generates line plots for datasets with a datetime index, and will raise an error for other types of indices.
    - The function does not handle large datasets efficiently, and performance may degrade with very large datasets.
    """

    figures = []
    summary = []

    for dataset in datasets:
        df = (
            dataset.df
        )  # Assuming DataFrameDataset objects have a .df attribute to get the pandas DataFrame

        if not pd.api.types.is_datetime64_any_dtype(df.index):
            raise ValueError(f"Dataset {dataset.input_id} must have a datetime index")

        fig = go.Figure()

        for column in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df[column], mode="lines", name=column)
            )

            start_date = df.index.min().strftime("%Y-%m-%d")
            end_date = df.index.max().strftime("%Y-%m-%d")
            frequency = pd.infer_freq(df.index)
            num_missing_values = df[column].isna().sum()
            count = df[column].count()

            summary.append(
                {
                    "Dataset": dataset.input_id,
                    "Variable": column,
                    "Start Date": start_date,
                    "End Date": end_date,
                    "Frequency": frequency,
                    "Num of Missing Values": num_missing_values,
                    "Count": count,
                }
            )

        fig.update_layout(
            title=f"Dataset {dataset.input_id}",
            xaxis_title="Date",
            yaxis_title="Value",
            legend_title="Variables",
            font=dict(size=16),
            showlegend=True,
        )

        figures.append(fig)

    result_df = pd.DataFrame(summary)

    return (result_df, *figures)
