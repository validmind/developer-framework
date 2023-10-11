# Copyright © 2023 ValidMind Inc. All rights reserved.

import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose

from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric

logger = get_logger(__name__)


class SeasonalDecompose(Metric):
    """
    Decomposes dataset features into observed, trend, seasonal, and residual components to identify patterns and
    validate dataset.

    **Purpose**: This test utilizes the Seasonal Decomposition of Time Series by Loess (STL) method to decompose a
    dataset into its fundamental components: observed, trend, seasonal, and residuals. The purpose is to identify
    implicit patterns, majorly any seasonality, in the dataset's features which aid in developing a more comprehensive
    understanding and effectively validating the dataset.

    **Test Mechanism**: The testing process exploits the `seasonal_decompose` function from the
    `statsmodels.tsa.seasonal` library to evaluate each feature in the dataset. It isolates each feature into four
    components: observed, trend, seasonal, and residuals, and generates essentially six subplot graphs per feature for
    visual interpretation of the results. Prior to the seasonal decomposition, non-finite values are scrutinized and
    removed thus, ensuring reliability in the analysis.

    **Signs of High Risk**:
    - **Non-Finiteness**: If a dataset carries too many non-finite values it might flag high risk as these values are
    omitted before conducting the seasonal decomposition.
    - **Frequent Warnings**: The test could be at risk if it chronically fails to infer frequency for a scrutinized
    feature.
    - **High Seasonality**: A high seasonal component could potentially render forecasts unreliable due to overwhelming
    seasonal variation.

    **Strengths**:
    - **Seasonality Detection**: The code aptly discerns hidden seasonality patterns in the features of datasets.
    - **Visualization**: The test facilitates interpretation and comprehension via graphical representations.
    - **Unrestricted Usage**: The code is not confined to any specific regression model, thereby promoting wide-ranging
    applicability.

    **Limitations**:
    - **Dependence on Assumptions**: The test presumes that features in the dataset are periodically distributed. If no
    frequency could be inferred for a variable, that feature is excluded from the test.
    - **Handling Non-finite Values**: The test disregards non-finite values during the analysis which could potentially
    result in incomplete understanding of the dataset.
    - **Unreliability with Noisy Datasets**: The test tends to produce unreliable results when used with heavy noise
    present in the dataset.
    """

    category = "univariate_analysis"
    name = "seasonal_decompose"
    required_inputs = ["dataset"]
    default_params = {"seasonal_model": "additive"}
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "seasonality", "statsmodels"],
    }

    def store_seasonal_decompose(self, column, sd_one_column):
        """
        Stores the seasonal decomposition results in the test context so they
        can be re-used by other tests. Note we store one `sd` at a time for every
        column in the dataset.
        """
        sd_all_columns = (
            self.test_context.get_context_data("seasonal_decompose") or dict()
        )
        sd_all_columns[column] = sd_one_column
        self.test_context.set_context_data("seasonal_decompose", sd_all_columns)

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
                lambda x: x.reset_index()
                if not isinstance(x.index, pd.DatetimeIndex)
                else x.reset_index().rename(columns={x.index.name: "Date"})
            )
            .assign(
                Date=lambda x: x["Date"].astype(str)
                if "Date" in x.columns
                else x.index.astype(str)
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

        df = self.dataset.df

        results = {}
        figures = []

        for col in df.columns:
            series = df[col].dropna()

            # Check for non-finite values and handle them
            if not series[np.isfinite(series)].empty:
                inferred_freq = pd.infer_freq(series.index)

                if inferred_freq is not None:
                    logger.info(f"Frequency of {col}: {inferred_freq}")

                    # Only take finite values to seasonal_decompose
                    sd = seasonal_decompose(
                        series[np.isfinite(series)], model=seasonal_model
                    )
                    self.store_seasonal_decompose(col, sd)

                    results[col] = self.serialize_seasonal_decompose(sd)

                    # Create subplots
                    fig, axes = plt.subplots(3, 2)
                    width, _ = fig.get_size_inches()
                    fig.set_size_inches(width, 15)
                    fig.subplots_adjust(hspace=0.3)
                    fig.suptitle(
                        f"Seasonal Decomposition for {col}",
                        fontsize=20,
                        weight="bold",
                        y=0.95,
                    )

                    # Original seasonal decomposition plots
                    # Observed
                    sd.observed.plot(ax=axes[0, 0])
                    axes[0, 0].set_title("Observed", fontsize=18)
                    axes[0, 0].set_xlabel("")
                    axes[0, 0].tick_params(axis="both", labelsize=18)

                    # Trend
                    sd.trend.plot(ax=axes[0, 1])
                    axes[0, 1].set_title("Trend", fontsize=18)
                    axes[0, 1].set_xlabel("")
                    axes[0, 1].tick_params(axis="both", labelsize=18)

                    # Seasonal
                    sd.seasonal.plot(ax=axes[1, 0])
                    axes[1, 0].set_title("Seasonal", fontsize=18)
                    axes[1, 0].set_xlabel("")
                    axes[1, 0].tick_params(axis="both", labelsize=18)

                    # Residuals
                    sd.resid.plot(ax=axes[1, 1])
                    axes[1, 1].set_title("Residuals", fontsize=18)
                    axes[1, 1].set_xlabel("")
                    axes[1, 1].tick_params(axis="both", labelsize=18)

                    # Histogram with KDE
                    residuals = sd.resid.dropna()
                    sns.histplot(residuals, kde=True, ax=axes[2, 0])
                    axes[2, 0].set_title("Histogram and KDE of Residuals", fontsize=18)
                    axes[2, 0].set_xlabel("")
                    axes[2, 0].tick_params(axis="both", labelsize=18)

                    # Normal Q-Q plot
                    stats.probplot(residuals, plot=axes[2, 1])
                    axes[2, 1].set_title("Normal Q-Q Plot of Residuals", fontsize=18)
                    axes[2, 1].set_xlabel("")
                    axes[2, 1].tick_params(axis="both", labelsize=18)

                    # Do this if you want to prevent the figure from being displayed
                    plt.close("all")

                    figures.append(
                        Figure(
                            for_object=self,
                            key=f"{self.key}:{col}",
                            figure=fig,
                        )
                    )
                else:
                    warnings.warn(
                        f"No frequency could be inferred for variable '{col}'. Skipping seasonal decomposition and plots for this variable."
                    )

        return self.cache_results(results, figures=figures)
