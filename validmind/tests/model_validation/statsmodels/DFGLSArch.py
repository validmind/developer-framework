# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from arch.unitroot import DFGLS

from validmind.vm_models import Metric


@dataclass
class DFGLSArch(Metric):
    """
    **Purpose**: The purpose of the Dickey-Fuller GLS (DFGLS) Arch metric is to establish the order of integration of
    time series data. In machine learning models that deal with time series and forecasting, this metric checks for the
    presence of a unit root i.e., it tests whether a time series is non-stationary, which is an integral first step in
    such analyses.

    **Test Mechanism**: In this code, the Dickey-Fuller GLS unit root test is employed on each feature of the dataset.
    In other words, it iterates over every individual column of the dataset and applies the DFGLS test to evaluate and
    report on the presence of a unit root. This information is then stored as output values such as 'stat' for the test
    statistic, 'pvalue' for the p-value, 'usedlag' for the number of lagged differences used in the regression and
    'nobs' for the number of observations.

    **Signs of High Risk**: High risk in this context would be determined by a high p-value. If the p-value for the
    DFGLS test is high (e.g., a common threshold is above 0.05), this indicates that the time series data is likely
    non-stationary, and thus poses a risk for generating unreliable forecasts or analyses.

    **Strengths**: The Dickey-Fuller GLS is a powerful technique to check the stationarity of times series data. It
    helps in confirming that the assumptions of the models are met before the actual building of the machine learning
    models can take place. The results given by this metric provides a clear perspective on whether the data is
    suitable for certain machine learning models, mainly those that require time-series to be stationary.

    **Limitations**: Despite its advantages, the DFGLS test also has some limitations. It can lead to incorrect
    conclusions if the time series has a structural break, or if the time series follows a trend but is otherwise
    stationary (in which case detrending might be necessary). Also, it doesn't work well with shorter time series data
    or with volatile data.
    """

    name = "dickey_fuller_gls"
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "forecasting", "unit_root_test"],
    }

    def run(self):
        """
        Calculates Dickey-Fuller GLS metric for each of the dataset features
        """
        dataset = self.dataset.df

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
