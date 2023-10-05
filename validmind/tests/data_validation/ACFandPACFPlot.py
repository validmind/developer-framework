# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from validmind.vm_models import Figure, Metric


class ACFandPACFPlot(Metric):
    """
    **Purpose**: The ACF (Autocorrelation Function) and PACF (Partial Autocorrelation Function) plot test is employed
    for analyzing time series data in machine learning models. These plots provide valuable insights about the data
    correlation over a period of time. The ACF plots the correlation of the series with its own lags, while the PACF
    plots correlations after removing the effects already explained by earlier lags. This helps in identifying the
    nature of the trend (for example, seasonality), degree of autocorrelation, and selecting order parameters for
    AutoRegressive Integrated Moving Average (ARIMA) models.

    **Test Mechanism**: The python class `ACFandPACFPlot` receives a dataset with a time-based index. After checking
    that the index is of datetime type and dealing with any NaN values, it generates ACF and PACF plots for each column
    in the dataset, creating a subplot for each. In case the dataset does not include key columns, an error is thrown.

    **Signs of High Risk**: An indication of model risk in relation to the ACF and PACF plot test includes sudden drops
    in the correlation at a specific lag or consistent high correlation across multiple lags. Both could indicate
    non-stationarity in the data, which might suggest that the model estimated on this data might not generalize well
    to future data.

    **Strengths**: The ACF and PACF plots provide clear graphical representations of the correlation in time series
    data. This is particularly useful for identifying important characteristics such as seasonality, trends, and
    correlation patterns within the data. This allows for better model configuration, more specifically in the
    selection of parameters for ARIMA models.

    **Limitations**: ACF and PACF plots can only be used with time series data, and are thus not applicable to every ML
    model. Additionally, they require a large and consistent dataset, as gaps can lead to misleading results. These
    plots only show linear correlation, ignoring potential nonlinear relationships. Lastly, they may not be intuitive
    for non-experts to interpret and are not a substitute for more advanced analyses.
    """

    name = "acf_pacf_plot"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["regression"],
        "tags": [
            "time_series_data",
            "forecasting",
            "statistical_test",
            "visualization",
        ],
    }

    def run(self):
        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        columns = list(self.dataset.df.columns)

        df = self.dataset.df.dropna()

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        figures = []

        for col in df.columns:
            series = df[col]

            # Create subplots
            fig, (ax1, ax2) = plt.subplots(1, 2)
            width, _ = fig.get_size_inches()
            fig.set_size_inches(width, 5)

            plot_acf(series, ax=ax1)
            plot_pacf(series, ax=ax2)

            # Get the current y-axis limits
            ymin, ymax = ax1.get_ylim()
            # Set new limits - adding a bit of space
            ax1.set_ylim([ymin, ymax + 0.05 * (ymax - ymin)])

            ymin, ymax = ax2.get_ylim()
            ax2.set_ylim([ymin, ymax + 0.05 * (ymax - ymin)])

            ax1.tick_params(axis="both", labelsize=18)
            ax2.tick_params(axis="both", labelsize=18)
            ax1.set_title(f"ACF for {col}", weight="bold", fontsize=20)
            ax2.set_title(f"PACF for {col}", weight="bold", fontsize=20)
            ax1.set_xlabel("Lag", fontsize=18)
            ax2.set_xlabel("Lag", fontsize=18)
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
