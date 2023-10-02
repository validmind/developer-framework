# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from validmind.vm_models import Figure, Metric


class TimeSeriesHistogram(Metric):
    """
    **Purpose**: This test conducts a histogram analysis on time series data. The goal is to evaluate the distribution
    of values in the dataset over a given time period, typically for regression tasks. Internet traffic, stock prices,
    weather data etc. could be time series data. Histograms provide insights into the data’s underlying probability
    distribution, skewness, peakness(kurtosis) etc.

    **Test Mechanism**: The test requires a dataset column that must have a datetime type index. It iterates over each
    column in the provided dataset and generates a histogram using Seaborn's histplot function. If the dataset contains
    more than one time-series (i.e., more than one column with datetime type index), a separate histogram will be
    plotted for each. Additionally, a kernel density estimate (KDE) line is drawn for each histogram to indicate the
    data's underlying probability distribution. The x and y-axis labels are hidden to only focus on the data
    distribution.

    **Signs of High Risk**:
    - The dataset does not contain a column with a datetime type index.
    - The specified columns do not exist in the dataset.
    - The distribution of data in the histogram exhibits high skewness or kurtosis, which might induce biases in the
    model.
    - Presence of outliers that are far from the main data distribution.

    **Strengths**:
    - Provides a visual diagnostic tool, which is a good starting point to understand the overall behavior and
    distribution trends of the dataset.
    - Works well for both single and multiple time series data analysis.
    - The Kernel Density Estimation (KDE) line offers a smooth estimate of the overall trend in data distribution.

    **Limitations**:
    - It only provides a high-level overview of data distribution and does not provide specific numeric measures of
    skewness, kurtosis, etc.
    - It doesn’t show the precise data values and the actual data is grouped into bins, hence some detail is inherently
    lost (precision vs. general overview trade-off).
    - Can't handle non-numeric data columns.
    - The shape of the histogram can be sensitive to the number of bins used.
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
