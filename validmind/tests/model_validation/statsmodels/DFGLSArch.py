# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from arch.unitroot import DFGLS

from validmind.vm_models import Metric


@dataclass
class DFGLSArch(Metric):
    """
    Executes Dickey-Fuller GLS metric to determine order of integration and check stationarity in time series data.

    **Purpose**: The Dickey-Fuller GLS (DFGLS) Arch metric is utilized to determine the order of integration in time
    series data. For machine learning models dealing with time series and forecasting, this metric evaluates the
    existence of a unit root, thereby checking whether a time series is non-stationary. This analysis is a crucial
    initial step when dealing with time series data.

    **Test Mechanism**: This code implements the Dickey-Fuller GLS unit root test on each attribute of the dataset.
    This process involves iterating through every column of the dataset and applying the DFGLS test to assess the
    presence of a unit root. The resulting information, including the test statistic ('stat'), the p-value ('pvalue'),
    the quantity of lagged differences utilized in the regression ('usedlag'), and the number of observations ('nobs'),
    is subsequently stored.

    **Signs of High Risk**:
    - A high p-value for the DFGLS test represents a high risk. Specifically, a p-value above a typical threshold of
    0.05 suggests that the time series data is quite likely to be non-stationary, thus presenting a high risk for
    generating unreliable forecasts.

    **Strengths**:
    - The Dickey-Fuller GLS test is a potent tool for checking the stationarity of time series data.
    - It helps to verify the assumptions of the models before the actual construction of the machine learning models
    proceeds.
    - The results produced by this metric offer a clear insight into whether the data is appropriate for specific
    machine learning models, especially those demanding the stationarity of time series data.

    **Limitations**:
    - Despite its benefits, the DFGLS test does present some drawbacks. It can potentially lead to inaccurate
    conclusions if the time series data incorporates a structural break.
    - If the time series tends to follow a trend while still being stationary, the test might misinterpret it,
    necessitating further detrending.
    - The test also presents challenges when dealing with shorter time series data or volatile data, not producing
    reliable results in these cases.
    """

    name = "dickey_fuller_gls"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "forecasting", "unit_root_test"],
    }

    def run(self):
        """
        Calculates Dickey-Fuller GLS metric for each of the dataset features
        """
        dataset = self.inputs.dataset.df

        dfgls_values = {}
        for col in dataset.columns:
            dfgls_out = DFGLS(dataset[col].values)
            dfgls_values[col] = {
                "stat": dfgls_out.stat,
                "pvalue": dfgls_out.pvalue,
                "usedlag": dfgls_out.lags,
                "nobs": dfgls_out.nobs,
            }

        return self.cache_results(dfgls_values)
