# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd
from statsmodels.tsa.stattools import adfuller

from validmind.logging import get_logger
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata

logger = get_logger(__name__)


@dataclass
class ADF(Metric):
    """
    Assesses the stationarity of a time series dataset using the Augmented Dickey-Fuller (ADF) test.

    **Purpose**: The Augmented Dickey-Fuller (ADF) test metric is used here to determine the order of integration,
    i.e., the stationarity of a given time series data. The stationary property of data is pivotal in many machine
    learning models as it impacts the reliability and effectiveness of predictions and forecasts.

    **Test Mechanism**: The ADF test starts by executing the ADF function from the statsmodels library on every feature
    of the dataset. Multiple outputs are generated for each run, including the ADF test statistic and p-value, count of
    lags used, the number of observations factored into the test, critical values at various confidence levels, and the
    maximized information criterion. These results are stored for each feature for subsequent analysis.

    **Signs of High Risk**:
    - An inflated ADF statistic and high p-value (generally above 0.05) insinuate a high risk to the model's
    performance due to the presence of a unit root indicating non-stationarity.
    - Such non-stationarity might result in untrustworthy or insufficient forecasts.

    **Strengths**:
    - The ADF test is robust to more sophisticated correlation within the data, which empowers it to be deployed in
    settings where data might display complex stochastic behavior.
    - The ADF test provides explicit outputs like test statistics, critical values, and information criterion, thereby
    enhancing our understanding and transparency of the model validation process.

    **Limitations**:
    - The ADF test might demonstrate low statistical power, making it challenging to differentiate between a unit root
    and near-unit-root processes causing false negatives.
    - The test assumes the data follows an autoregressive process, which might not be the case all the time.
    - The ADF test finds it demanding to manage time series data with structural breaks.
    """

    name = "adf"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["regression"],
        "tags": [
            "time_series_data",
            "statsmodels",
            "forecasting",
            "statistical_test",
            "stationarity",
        ],
    }

    def summary(self, metric_value: dict):
        table = pd.DataFrame.from_dict(metric_value, orient="index")
        table = table.reset_index()
        table.columns = [
            "Feature",
            "ADF Statistic",
            "P-Value",
            "Used Lag",
            "Number of Observations",
            "Critical Values",
            "IC Best",
        ]
        table = table.rename_axis("Index", axis=1)

        return ResultSummary(
            results=[
                ResultTable(
                    data=table,
                    metadata=ResultTableMetadata(
                        title="ADF Test Results for Each Feature"
                    ),
                ),
            ]
        )

    def run(self):
        """
        Calculates ADF metric for each of the dataset features
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

        adf_values = {}
        for col in dataset.columns:
            try:
                adf_result = adfuller(dataset[col].values)
                adf_values[col] = {
                    "ADF Statistic": adf_result[0],
                    "P-Value": adf_result[1],
                    "Used Lag": adf_result[2],
                    "Number of Observations": adf_result[3],
                    "Critical Values": adf_result[4],
                    "IC Best": adf_result[5],
                }
            except Exception as e:
                logger.error(f"Error processing column '{col}': {e}")
                adf_values[col] = {
                    "ADF Statistic": None,
                    "P-Value": None,
                    "Used Lag": None,
                    "Number of Observations": None,
                    "Critical Values": None,
                    "IC Best": None,
                    "Error": str(e),
                }

        return self.cache_results(adf_values)