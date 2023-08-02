# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import pandas as pd

from validmind.vm_models import Figure, Metric


class RollingStatsPlot(Metric):
    """
    This class provides a metric to visualize the stationarity of a given time series dataset by plotting the rolling mean and rolling standard deviation. The rolling mean represents the average of the time series data over a fixed-size sliding window, which helps in identifying trends in the data. The rolling standard deviation measures the variability of the data within the sliding window, showing any changes in volatility over time. By analyzing these plots, users can gain insights into the stationarity of the time series data and determine if any transformations or differencing operations are required before applying time series models.
    """

    name = "rolling_stats_plot"
    required_context = ["dataset"]
    default_params = {"window_size": 12}

    def plot_rolling_statistics(self, col, window_size=12):
        """
        Plot rolling mean and rolling standard deviation in different subplots for a given series.
        :param series: Pandas Series with time-series data
        :param window_size: Window size for the rolling calculations
        :param ax1: Axis object for the rolling mean plot
        :param ax2: Axis object for the rolling standard deviation plot
        """
        rolling_mean = self.dataset.df[col].rolling(window=window_size).mean()
        rolling_std = self.dataset.df[col].rolling(window=window_size).std()

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
