# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd
from arch.unitroot import PhillipsPerron
from numpy.linalg import LinAlgError

from validmind.logging import get_logger
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata

logger = get_logger(__name__)


@dataclass
class PhillipsPerronArch(Metric):
    """
    Executes Phillips-Perron test to assess the stationarity of time series data in each ML model feature.

    **Purpose**: The Phillips-Perron (PP) test is used to establish the order of integration in time series data,
    testing a null hypothesis that a time series is unit-root non-stationary. This is vital in forecasting and
    understanding the stochastic behavior of data within machine learning models. Essentially, the PP test aids in
    confirming the robustness of results and generating valid predictions from regression analysis models.

    **Test Mechanism**: The PP test is conducted for each feature in the dataset. A data frame is created from the
    dataset, and for each column in this frame, the PhillipsPerron method calculates the statistic value, p-value, used
    lags, and number of observations. This process computes the PP metric for each feature and stores the results for
    future reference.

    **Signs of High Risk**:
    - A high P-value could imply that the series has a unit root and is therefore non-stationary.
    - Test statistic values that surpass critical values indicate additional evidence of non-stationarity.
    - A high 'usedlag' value for a series could point towards autocorrelation issues which could further impede the
    model's performance.

    **Strengths**:
    - Resilience against heteroskedasticity in the error term is a significant strength of the PP test.
    - Its capacity to handle long time series data.
    - Its ability to determine whether the time series is stationary or not, influencing the selection of suitable
    models for forecasting.

    **Limitations**:
    - The PP test can only be employed within a univariate time series framework.
    - The test relies on asymptotic theory, which means the test's power can significantly diminish for small sample
    sizes.
    - The need to convert non-stationary time series into stationary series through differencing might lead to loss of
    vital data points.
    """

    name = "phillips_perron"
    required_inputs = ["dataset"]
    tasks = ["regression"]
    tags = [
        "time_series_data",
        "forecasting",
        "statistical_test",
        "unit_root_test",
    ]

    def run(self):
        """
        Calculates PP metric for each of the dataset features
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

        # Initialize a list to store Phillips-Perron results
        pp_values = []

        for col in dataset.columns:
            try:
                pp = PhillipsPerron(dataset[col].values)
                pp_values.append(
                    {
                        "Variable": col,
                        "stat": pp.stat,
                        "pvalue": pp.pvalue,
                        "usedlag": pp.lags,
                        "nobs": pp.nobs,
                    }
                )
            except LinAlgError as e:
                logger.error(f"Error processing column '{col}': {e}")
                pp_values.append(
                    {
                        "Variable": col,
                        "stat": None,
                        "pvalue": None,
                        "usedlag": None,
                        "nobs": None,
                        "error": str(e),
                    }
                )

        return self.cache_results({"phillips_perron_results": pp_values})

    def summary(self, metric_value):
        """
        Build a table for summarizing the Phillips-Perron results
        """
        pp_results = metric_value["phillips_perron_results"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pp_results,
                    metadata=ResultTableMetadata(title="Phillips-Perron Test Results"),
                )
            ]
        )
