# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.express as px

from validmind import tags, tasks


@tags("data_validation", "visualization")
@tasks("regression", "time_series_forecasting")
def TimeSeriesHistogram(dataset, nbins=30):
    """
    Visualizes distribution of time-series data using histograms and Kernel Density Estimation (KDE) lines.

    **Purpose**: The purpose of this metric is to perform a histogram analysis on time-series data. It primarily
    assesses the distribution of values within a dataset over a period of time, typically used for regression tasks.
    The types of data that this metric can be applicable to are diverse, ranging from internet traffic and stock prices
    to weather data. This analysis provides valuable insights into the probability distribution, skewness, and peakness
    (kurtosis) underlying the data.

    **Test Mechanism**: This test operates on a specific column within the dataset that is required to have a datetime
    type index. It goes through each column in the given dataset, creating a histogram with Plotly's histplot
    function. In cases where the dataset includes more than one time-series (i.e., more than one column with a datetime
    type index), a distinct histogram is plotted for each series. Additionally, a kernel density estimate (KDE) line is
    drawn for each histogram, providing a visualization of the data's underlying probability distribution. The x and
    y-axis labels are purposely hidden to concentrate solely on the data distribution.

    **Signs of High Risk**:
    - The dataset lacks a column with a datetime type index.
    - The specified columns do not exist within the dataset.
    - The data distribution within the histogram demonstrates high degrees of skewness or kurtosis, which could bias
    the model.
    - Outliers that differ significantly from the primary data distribution are present.

    **Strengths**:
    - It serves as a visual diagnostic tool, offering an ideal starting point for understanding the overall behavior
    and distribution trends within the dataset.
    - It is effective for both single and multiple time-series data analysis.
    - The Kernel Density Estimation (KDE) line provides a smooth estimate of the overall trend in data distribution.

    **Limitations**:
    - The metric only presents a high-level view of data distribution and does not offer specific numeric measures such
    as skewness or kurtosis.
    - The histogram does not display precise data values; due to the data grouping into bins, some detail is inevitably
    lost, marking a trade-off between precision and general overview.
    - The histogram cannot handle non-numeric data columns.
    - The histogram's shape may be sensitive to the number of bins used.
    """

    df = dataset.df

    columns = list(dataset.df.columns)

    if not set(columns).issubset(set(df.columns)):
        raise ValueError("Provided 'columns' must exist in the dataset")

    figures = []
    for col in columns:
        fig = px.histogram(
            df, x=col, marginal="violin", nbins=nbins, title=f"Histogram for {col}"
        )
        fig.update_layout(
            title={
                "text": f"Histogram for {col}",
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            xaxis_title="",
            yaxis_title="",
            font=dict(size=18),
        )
        figures.append(fig)

    return tuple(figures)
