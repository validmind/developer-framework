# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd
from arch.unitroot import ZivotAndrews
from numpy.linalg import LinAlgError

from validmind.logging import get_logger
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata

logger = get_logger(__name__)


@dataclass
class ZivotAndrewsArch(Metric):
    """
    Evaluates the order of integration and stationarity of time series data using Zivot-Andrews unit root test.

    **Purpose**: The Zivot-Andrews Arch metric is used to evaluate the order of integration for a time series data in a
    machine learning model. It's designed to test for stationarity, a crucial aspect in time series analysis where data
    points are not dependent on time. Stationarity means that the statistical properties such as mean, variance and
    autocorrelation are all constant over time.

    **Test Mechanism**: The Zivot-Andrews unit root test is performed on each feature in the dataset using the
    `ZivotAndrews` function from the `arch.unitroot` module. This function returns the Zivot-Andrews metric for each
    feature, which includes the statistical value, p-value (probability value), the number of used lags, and the number
    of observations. The p-value is later used to decide on the null hypothesis (the time series has a unit root and is
    non-stationary) based on a chosen level of significance.

    **Signs of High Risk**:
    - A high p-value can suggest high risk. This might indicate that there's insufficient evidence to reject the null
    hypothesis, which would mean the time series has a unit root and is therefore non-stationary.
    - Non-stationary time series data can lead to misleading statistics and unreliable machine learning models.

    **Strengths**:
    - The Zivot-Andrews Arch metric dynamically tests for stationarity against structural breaks in time series data,
    offering robust evaluation of stationarity in features.
    - This metric is especially beneficial with financial, economic, or other time-series data where data observations
    lack a consistent pattern and structural breaks may occur.

    **Limitations**:
    - The Zivot-Andrews Arch metric assumes that data is derived from a single-equation, autoregressive model. It may,
    therefore, not be appropriate for multivariate time series data or data which does not align with the
    autoregressive model assumption.
    - It might not take into account unexpected shocks or changes in the series trend which can both have a significant
    impact on the stationarity of the data.
    """

    name = "zivot_andrews"
    required_inputs = ["dataset"]
    tasks = ["regression"]
    tags = ["time_series_data", "stationarity", "unit_root_test"]

    def run(self):
        """
        Calculates Zivot-Andrews metric for each of the dataset features
        """
        dataset = self.inputs.dataset.df

        # Check if the dataset is a time series
        if not isinstance(dataset.index, (pd.DatetimeIndex, pd.PeriodIndex)):
            raise ValueError(
                "Dataset index must be a datetime or period index for time series analysis."
            )

        # Preprocessing: Drop rows with any NaN values
        if dataset.isnull().values.any():
            logger.warning(
                "Dataset contains missing values. Rows with NaNs will be dropped."
            )
            dataset = dataset.dropna()

        # Convert to numeric and handle non-numeric data
        dataset = dataset.apply(pd.to_numeric, errors="coerce")

        # Initialize a list to store Zivot-Andrews results
        za_values = []

        for col in dataset.columns:
            try:
                za = ZivotAndrews(dataset[col].values)
                za_values.append(
                    {
                        "Variable": col,
                        "stat": za.stat,
                        "pvalue": za.pvalue,
                        "usedlag": za.lags,
                        "nobs": za.nobs,
                    }
                )
            except (LinAlgError, ValueError) as e:
                logger.error(f"Error while processing column '{col}'. Details: {e}")
                za_values.append(
                    {
                        "Variable": col,
                        "stat": None,
                        "pvalue": None,
                        "usedlag": None,
                        "nobs": None,
                        "error": str(e),
                    }
                )

        return self.cache_results({"zivot_andrews_results": za_values})

    def summary(self, metric_value):
        """
        Build a table for summarizing the Zivot-Andrews results
        """
        za_results = metric_value["zivot_andrews_results"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=za_results,
                    metadata=ResultTableMetadata(title="Zivot-Andrews Test Results"),
                )
            ]
        )
