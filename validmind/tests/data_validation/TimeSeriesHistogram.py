# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from validmind.vm_models import Figure, Metric


class TimeSeriesHistogram(Metric):
    """
    Visualizes distribution of time-series data using histograms and Kernel Density Estimation (KDE) lines.

    **Purpose**: The purpose of this metric is to perform a histogram analysis on time-series data. It primarily
    assesses the distribution of values within a dataset over a period of time, typically used for regression tasks.
    The types of data that this metric can be applicable to are diverse, ranging from internet traffic and stock prices
    to weather data. This analysis provides valuable insights into the probability distribution, skewness, and peakness
    (kurtosis) underlying the data.

    **Test Mechanism**: This test operates on a specific column within the dataset that is required to have a datetime
    type index. It goes through each column in the given dataset, creating a histogram with Seaborn's histplot
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

    name = "time_series_histogram"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "visualization"],
    }

    def run(self):
        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        columns = list(self.dataset.df.columns)

        df = self.dataset.df

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        figures = []
        for col in columns:
            plt.figure()
            fig, _ = plt.subplots()
            ax = sns.histplot(data=df, x=col, kde=True)
            plt.title(f"Histogram for {col}", weight="bold", fontsize=20)

            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)
            ax.set_xlabel("")
            ax.set_ylabel("")
            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{col}",
                    figure=fig,
                )
            )

        plt.close("all")

        return self.cache_results(
            figures=figures,
        )
