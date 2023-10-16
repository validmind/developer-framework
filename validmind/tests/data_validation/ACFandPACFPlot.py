# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from validmind.vm_models import Figure, Metric


class ACFandPACFPlot(Metric):
    """
    Analyzes time series data using Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF) plots to
    reveal trends and correlations.

    **Purpose**: The ACF (Autocorrelation Function) and PACF (Partial Autocorrelation Function) plot test is employed
    to analyze time series data in machine learning models. It illuminates the correlation of the data over time by
    plotting the correlation of the series with its own lags (ACF), and the correlations after removing effects already
    accounted for by earlier lags (PACF). This information can identify trends, such as seasonality, degrees of
    autocorrelation, and inform the selection of order parameters for AutoRegressive Integrated Moving Average (ARIMA)
    models.

    **Test Mechanism**: The `ACFandPACFPlot` test accepts a dataset with a time-based index. It first confirms the
    index is of a datetime type, then handles any NaN values. The test subsequently generates ACF and PACF plots for
    each column in the dataset, producing a subplot for each. If the dataset doesn't include key columns, an error is
    returned.

    **Signs of High Risk**:

    - Sudden drops in the correlation at a specific lag might signal a model at high risk.
    - Consistent high correlation across multiple lags could also indicate non-stationarity in the data, which may
    suggest that a model estimated on this data won't generalize well to future, unknown data.

    **Strengths**:

    - ACF and PACF plots offer clear graphical representations of the correlations in time series data.
    - These plots are effective at revealing important data characteristics such as seasonality, trends, and
    correlation patterns.
    - The insights from these plots aid in better model configuration, particularly in the selection of ARIMA model
    parameters.

    **Limitations**:

    - ACF and PACF plots are exclusively for time series data and hence, can't be applied to all ML models.
    - These plots require large, consistent datasets as gaps could lead to misleading results.
    - The plots can only represent linear correlations and fail to capture any non-linear relationships within the data.
    - The plots might be difficult for non-experts to interpret and should not replace more advanced analyses.
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
