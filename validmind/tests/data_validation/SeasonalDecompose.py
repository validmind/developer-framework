# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import warnings

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose

from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric

logger = get_logger(__name__)


class SeasonalDecompose(Metric):
    """
    Assesses patterns and seasonality in a time series dataset by decomposing its features into foundational components.

    ### Purpose

    The Seasonal Decompose test aims to decompose the features of a time series dataset into their fundamental
    components: observed, trend, seasonal, and residuals. By utilizing the Seasonal Decomposition of Time Series by
    Loess (STL) method, the test identifies underlying patterns, predominantly seasonality, in the dataset's features.
    This aids in developing a more comprehensive understanding of the dataset, which in turn facilitates more effective
    model validation.

    ### Test Mechanism

    The testing process leverages the `seasonal_decompose` function from the `statsmodels.tsa.seasonal` library to
    evaluate each feature in the dataset. It isolates each feature into four components—observed, trend, seasonal, and
    residuals—and generates six subplot graphs per feature for visual interpretation. Prior to decomposition, the test
    scrutinizes and removes any non-finite values, ensuring the reliability of the analysis.

    ### Signs of High Risk

    - **Non-Finiteness**: Datasets with a high number of non-finite values may flag as high risk since these values are
    omitted before conducting the seasonal decomposition.
    - **Frequent Warnings**: Chronic failure to infer the frequency for a scrutinized feature indicates high risk.
    - **High Seasonality**: A significant seasonal component could potentially render forecasts unreliable due to
    overwhelming seasonal variation.

    ### Strengths

    - **Seasonality Detection**: Accurately discerns hidden seasonality patterns in dataset features.
    - **Visualization**: Facilitates interpretation and comprehension through graphical representations.
    - **Unrestricted Usage**: Not confined to any specific regression model, promoting wide-ranging applicability.

    ### Limitations

    - **Dependence on Assumptions**: Assumes that dataset features are periodically distributed. Features with no
    inferable frequency are excluded from the test.
    - **Handling Non-Finite Values**: Disregards non-finite values during analysis, potentially resulting in an
    incomplete understanding of the dataset.
    - **Unreliability with Noisy Datasets**: Produces unreliable results when used with datasets that contain heavy
    noise.
    """

    name = "seasonal_decompose"
    required_inputs = ["dataset"]
    default_params = {"seasonal_model": "additive"}
    tasks = ["regression"]
    tags = ["time_series_data", "seasonality", "statsmodels"]

    def store_seasonal_decompose(self, column, sd_one_column):
        """
        Stores the seasonal decomposition results in the test context so they
        can be re-used by other tests. Note we store one `sd` at a time for every
        column in the dataset.
        """
        sd_all_columns = self.context.get_context_data("seasonal_decompose") or dict()
        sd_all_columns[column] = sd_one_column
        self.context.set_context_data("seasonal_decompose", sd_all_columns)

    def serialize_seasonal_decompose(self, sd):
        """
        Serializes the seasonal decomposition results for one column into a
        JSON serializable format that can be sent to the API.
        """
        results = {
            "observed": sd.observed,
            "trend": sd.trend,
            "seasonal": sd.seasonal,
            "resid": sd.resid,
        }

        # Convert pandas Series to DataFrames, reset their indices, and convert the dates to strings
        dfs = [
            pd.DataFrame(series)
            .pipe(
                lambda x: (
                    x.reset_index()
                    if not isinstance(x.index, pd.DatetimeIndex)
                    else x.reset_index().rename(columns={x.index.name: "Date"})
                )
            )
            .assign(
                Date=lambda x: (
                    x["Date"].astype(str)
                    if "Date" in x.columns
                    else x.index.astype(str)
                )
            )
            for series in results.values()
        ]

        # Merge DataFrames on the 'Date' column
        merged_df = dfs[0]
        for df in dfs[1:]:
            merged_df = merged_df.merge(df, on="Date")
        # Convert the merged DataFrame into a list of dictionaries
        return merged_df.to_dict("records")

    def run(self):
        # Parse input parameters
        if "seasonal_model" not in self.params:
            raise ValueError("seasonal_model must be provided in params")
        seasonal_model = self.params["seasonal_model"]

        df = self.inputs.dataset.df

        results = {}
        figures = []

        for col in df.columns:
            series = df[col].dropna()

            # Check for non-finite values and handle them
            if not series[np.isfinite(series)].empty:
                inferred_freq = pd.infer_freq(series.index)

                if inferred_freq is not None:

                    # Only take finite values to seasonal_decompose
                    sd = seasonal_decompose(
                        series[np.isfinite(series)], model=seasonal_model
                    )
                    self.store_seasonal_decompose(col, sd)

                    results[col] = self.serialize_seasonal_decompose(sd)

                    # Create subplots using Plotly
                    fig = make_subplots(
                        rows=3,
                        cols=2,
                        subplot_titles=(
                            "Observed",
                            "Trend",
                            "Seasonal",
                            "Residuals",
                            "Histogram and KDE of Residuals",
                            "Normal Q-Q Plot of Residuals",
                        ),
                        vertical_spacing=0.1,
                    )

                    # Observed
                    fig.add_trace(
                        go.Scatter(x=sd.observed.index, y=sd.observed, name="Observed"),
                        row=1,
                        col=1,
                    )

                    # Trend
                    fig.add_trace(
                        go.Scatter(x=sd.trend.index, y=sd.trend, name="Trend"),
                        row=1,
                        col=2,
                    )

                    # Seasonal
                    fig.add_trace(
                        go.Scatter(x=sd.seasonal.index, y=sd.seasonal, name="Seasonal"),
                        row=2,
                        col=1,
                    )

                    # Residuals
                    fig.add_trace(
                        go.Scatter(x=sd.resid.index, y=sd.resid, name="Residuals"),
                        row=2,
                        col=2,
                    )

                    # Histogram with KDE
                    residuals = sd.resid.dropna()
                    fig.add_trace(
                        go.Histogram(x=residuals, nbinsx=100, name="Residuals"),
                        row=3,
                        col=1,
                    )

                    # Normal Q-Q plot
                    qq = stats.probplot(residuals, plot=None)
                    qq_line_slope, qq_line_intercept = stats.linregress(
                        qq[0][0], qq[0][1]
                    )[:2]
                    qq_line = qq_line_slope * np.array(qq[0][0]) + qq_line_intercept

                    fig.add_trace(
                        go.Scatter(
                            x=qq[0][0], y=qq[0][1], mode="markers", name="QQ plot"
                        ),
                        row=3,
                        col=2,
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=qq[0][0],
                            y=qq_line,
                            mode="lines",
                            name="QQ line",
                        ),
                        row=3,
                        col=2,
                    )

                    fig.update_layout(
                        height=1000,
                        title_text=f"Seasonal Decomposition for {col}",
                        showlegend=False,
                    )

                    figures.append(
                        Figure(
                            for_object=self,
                            key=f"{self.key}:{col}",
                            figure=fig,
                        )
                    )
                else:
                    warnings.warn(
                        f"No frequency could be inferred for variable '{col}'. "
                        "Skipping seasonal decomposition and plots for this variable."
                    )

        return self.cache_results(results, figures=figures)
