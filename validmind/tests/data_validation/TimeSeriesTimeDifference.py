# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd
import plotly.graph_objects as go

from validmind import tags, tasks


@tags("time_series_data", "visualization")
@tasks("regression")
def TimeSeriesTimeDifference(datasets):
    """
    Evaluates the time differences between consecutive entries in each time series dataset and generates histograms.

    **Purpose**: The purpose of the TimeSeriesTimeDifference function is to evaluate the consistency of time
    intervals in multiple time series datasets by generating histograms of time differences between consecutive data
    points. This helps in identifying patterns or irregularities in data frequency, which is crucial for time-series
    analysis.

    **Test Mechanism**: The function iterates through each dataset, calculates the time differences between consecutive
    entries, and generates histograms using Plotly. Each dataset is expected to have a datetime index. The function
    checks this and raises an error if the index is not in datetime format. For each dataset, the time differences are
    computed and plotted in a histogram.

    **Signs of High Risk**:
    - If the index of the dataset is not in datetime format, it could lead to errors in time-series analysis and hinder
      the generation of accurate plots.
    - Irregular time differences between data points might affect the reliability of time-series models and analyses.

    **Strengths**:
    - This function provides a clear visualization of the time intervals between consecutive data points, making it
      easier to identify patterns and irregularities.
    - The histograms help in quickly assessing the distribution and consistency of time intervals in the data.
    - The function provides a comprehensive summary of key statistics for each variable, helping to identify data quality
      issues such as missing values.

    **Limitations**:
    - This function assumes that the datasets are provided as DataFrameDataset objects with a .df attribute to access
      the pandas DataFrame.
    - It only generates histograms for datasets with a datetime index, and will raise an error for other types of indices.
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

        for column in df.columns:
            # Calculate the time differences between consecutive entries for each variable
            time_diff = df[column].dropna().index.to_series().diff().dropna()

            if not time_diff.empty:
                # Convert the time differences to a suitable unit (e.g., days)
                time_diff_days = time_diff.dt.total_seconds() / (60 * 60 * 24)

                # Create a Plotly histogram for each variable
                fig = go.Figure(data=[go.Histogram(x=time_diff_days, nbinsx=50)])
                fig.update_layout(
                    title=f"{column} in {dataset.input_id} (Days)",
                    xaxis_title="Days",
                    yaxis_title="Frequency",
                    font=dict(size=16),
                    showlegend=False,  # Removing the legend
                )

                figures.append(fig)

                # Calculate additional statistics
                min_diff = time_diff_days.min()
                max_diff = time_diff_days.max()
                total_span = (df.index.max() - df.index.min()).days
                frequency = pd.infer_freq(df.index)

                summary.append(
                    {
                        "Dataset": dataset.input_id,
                        "Variable": column,
                        "Frequency": frequency,
                        "Min Time Difference (days)": min_diff,
                        "Max Time Difference (days)": max_diff,
                        "Total Time Span (days)": total_span,
                    }
                )

    result_df = pd.DataFrame(summary)

    return (result_df, *figures)
