# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import pandas as pd

from validmind.vm_models import Figure, Metric


class RollingStatsPlot(Metric):
    """
    **Purpose**: The `RollingStatsPlot` metric is used to assess the stationarity of time series data in a given
    dataset. More specifically, the metric evaluates the rolling mean and rolling standard deviation of the dataset
    over a defined window size. The rolling mean is a measure of the average trend in the data, while the rolling
    standard deviation assesses the data's volatility within the window. These measures are critical for preparing time
    series data for modeling as they provide insights into the behavior of the data over time.

    **Test Mechanism**: The testing mechanism is divided into two steps. Firstly, the rolling mean and standard
    deviation for each column of the dataset are calculated over a window size, specified by the user or defaulted to
    12 data points. Secondly, the rolling mean and standard deviation are plotted separately, thus visualizing the
    trends and volatility in the dataset. A basic check is performed to ensure that the columns exist in the dataset
    and that the provided dataset is indexed by date and time, which is a requirement for time series analysis.

    **Signs of High Risk**: Signs that could indicate high risk include:
    1. A non-stationary pattern in either the rolling mean or the rolling standard deviation plot. This might mean that
    the data has trends or seasonality, which could affect the performance of time series models.
    2. Missing columns in the dataset, which would prevent the metric from running successfully.
    3. The presence of NaN values in the dataset. These might need to be handled before the metric can proceed.

    **Strengths**: The strengths of this metric include:
    1. Providing visualizations of the data's trending behaviour and volatility, which can aid in understanding the
    overall characteristics of the data.
    2. Checking the integrity of the dataset (whether all designated columns exist, and that the index is of datetime
    type).
    3. Adapting to various window sizes, which allows for flexibility in analysing data with different temporal
    granularities.
    4. Accommodating multi-feature datasets by considering each column of the data individually.

    **Limitations**: Some limitations of the `RollingStatsPlot` metric include:
    1. A fixed window size is used for all columns, which may not accurately capture the patterns in datasets where
    different features have different optimal window sizes.
    2. The metric requires the dataset to be indexed by date and time, hence may not be applicable to datasets without
    a timestamp index.
    3. The metrics primarily serve for data visualization. It does not provide any quantitative measures for
    stationarity, such as statistical tests. Thus, interpretation is subjective and depends on the discretion of the
    modeler.
    """

    name = "rolling_stats_plot"
    required_inputs = ["dataset"]
    default_params = {"window_size": 12}
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "visualization", "stationarity"],
    }

    def plot_rolling_statistics(self, col, window_size=12):
        """
        Plot rolling mean and rolling standard deviation in different subplots for a given series.
        :param series: Pandas Series with time-series data
        :param window_size: Window size for the rolling calculations
        :param ax1: Axis object for the rolling mean plot
        :param ax2: Axis object for the rolling standard deviation plot
        """
        rolling_mean = self.dataset.df[col].rolling(window=int(window_size)).mean()
        rolling_std = self.dataset.df[col].rolling(window=int(window_size)).std()

        # Create a new figure and axis objects
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.plot(rolling_mean)

        ax1.set_title(
            f"Rolling Mean for {col}",
            fontsize=20,
            weight="bold",
        )
        ax1.set_ylabel("")
        ax1.tick_params(axis="both", labelsize=18)
        ax1.legend()

        ax2.plot(rolling_std, label="Rolling Standard Deviation", color="orange")
        ax2.set_title(
            f"Rolling STD for {col}",
            fontsize=20,
            weight="bold",
        )
        ax2.set_xlabel("")
        ax2.set_ylabel("")
        ax2.tick_params(axis="both", labelsize=18)
        ax2.legend()

        return fig

    def run(self):
        if "window_size" not in self.params:
            raise ValueError("Window size must be provided in params")

        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        window_size = self.params["window_size"]
        df = self.dataset.df.dropna()

        if not set(df.columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        figures = []

        for col in df.columns:
            fig = self.plot_rolling_statistics(col, window_size=window_size)

            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{col}",
                    figure=fig,
                )
            )

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

        return self.cache_results(figures=figures)
