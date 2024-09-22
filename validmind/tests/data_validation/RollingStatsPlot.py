# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import matplotlib.pyplot as plt
import pandas as pd

from validmind.vm_models import Figure, Metric


class RollingStatsPlot(Metric):
    """
    Evaluates the stationarity of time series data by plotting its rolling mean and standard deviation over a specified
    window.

    ### Purpose

    The `RollingStatsPlot` metric is employed to gauge the stationarity of time series data in a given dataset. This
    metric specifically evaluates the rolling mean and rolling standard deviation of the dataset over a pre-specified
    window size. The rolling mean provides an understanding of the average trend in the data, while the rolling
    standard deviation gauges the volatility of the data within the window. It is critical in preparing time series
    data for modeling as it reveals key insights into data behavior across time.

    ### Test Mechanism

    This mechanism is comprised of two steps. Initially, the rolling mean and standard deviation for each of the
    dataset's columns are calculated over a window size, which can be user-specified or by default set to 12 data
    points. Then, the calculated rolling mean and standard deviation are visualized via separate plots, illustrating
    the trends and volatility in the dataset. A straightforward check is conducted to ensure the existence of columns
    in the dataset, and to verify that the given dataset has been indexed by its date and time—a necessary prerequisite
    for time series analysis.

    ### Signs of High Risk

    - The presence of non-stationary patterns in either the rolling mean or the rolling standard deviation plots, which
    could indicate trends or seasonality in the data that may affect the performance of time series models.
    - Missing columns in the dataset, which would prevent the execution of this metric correctly.
    - The detection of NaN values in the dataset, which may need to be addressed before the metric can proceed
    successfully.

    ### Strengths

    - Offers visualizations of trending behavior and volatility within the data, facilitating a broader understanding
    of the dataset's inherent characteristics.
    - Checks of the dataset's integrity, such as the existence of all required columns and the availability of a
    datetime index.
    - Adjusts to accommodate various window sizes, thus allowing accurate analysis of data with differing temporal
    granularities.
    - Considers each column of the data individually, thereby accommodating multi-feature datasets.

    ### Limitations

    - For all columns, a fixed-size window is utilized. This may not accurately capture patterns in datasets where
    different features may require different optimal window sizes.
    - Requires the dataset to be indexed by date and time, hence it may not be usable for datasets without a timestamp
    index.
    - Primarily serves for data visualization as it does not facilitate any quantitative measures for stationarity,
    such as through statistical tests. Therefore, the interpretation is subjective and depends heavily on modeler
    discretion.
    """

    name = "rolling_stats_plot"
    required_inputs = ["dataset"]
    default_params = {"window_size": 12}
    tasks = ["regression"]
    tags = ["time_series_data", "visualization", "stationarity"]

    def plot_rolling_statistics(self, col, window_size=12):
        """
        Plot rolling mean and rolling standard deviation in different subplots for a given series.
        :param series: Pandas Series with time-series data
        :param window_size: Window size for the rolling calculations
        :param ax1: Axis object for the rolling mean plot
        :param ax2: Axis object for the rolling standard deviation plot
        """
        rolling_mean = (
            self.inputs.dataset.df[col].rolling(window=int(window_size)).mean()
        )
        rolling_std = self.inputs.dataset.df[col].rolling(window=int(window_size)).std()

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
        if not pd.api.types.is_datetime64_any_dtype(self.inputs.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        window_size = self.params["window_size"]
        df = self.inputs.dataset.df.dropna()

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
