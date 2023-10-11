# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from statsmodels.tsa.stattools import kpss

from validmind.vm_models import Metric


@dataclass
class KPSS(Metric):
    """
    Executes KPSS unit root test to validate stationarity of time-series data in machine learning model.

    **Purpose**: The Kwiatkowski-Phillips-Schmidt-Shin (KPSS) unit root test is utilized to ensure the stationarity of
    data within the machine learning model. It specifically works on time-series data to establish the order of
    integration, which is a prime requirement for accurate forecasting, given the fundamental condition for any time
    series model is that the series should be stationary.

    **Test Mechanism**: This metric evaluates the KPSS score for every feature present in the dataset. Within the KPSS
    score, there are various components, namely: a statistic, a p-value, a used lag, and critical values. The core
    scheme behind the KPSS score is to test the hypothesis that an observable time series is stationary around a
    deterministic trend. If the computed statistic surpasses the critical value, the null hypothesis is dismissed,
    inferring the series is non-stationary.

    **Signs of High Risk**:
    - High KPSS score represents a considerable risk, particularly if the calculated statistic is higher than the
    critical value.
    - If the null hypothesis is rejected and the series is recognized as non-stationary, it heavily influences the
    model's forecasting capability rendering it less effective.

    **Strengths**:
    - The KPSS test directly measures the stationarity of a series, allowing it to fulfill a key prerequisite for many
    time-series models, making it a valuable tool for model validation.
    - The logics underpinning the test are intuitive and simple, making it understandable and accessible for developers
    and risk management teams.

    **Limitations**:
    - The KPSS test presumes the absence of a unit root in the series and does not differentiate between series that
    are stationary and those border-lining stationarity.
    - The test might show restricted power against specific alternatives.
    - The reliability of the test is contingent on the number of lags selected, which introduces potential bias in the
    measurement.
    """

    name = "kpss"
    metadata = {
        "task_types": ["regression"],
        "tags": [
            "time_series_data",
            "forecasting",
            "stationarity",
            "unit_root_test",
            "statsmodels",
        ],
    }

    def run(self):
        """
        Calculates KPSS for each of the dataset features
        """
        dataset = self.dataset.df

        kpss_values = {}
        for col in dataset.columns:
            kpss_stat, pvalue, usedlag, critical_values = kpss(dataset[col].values)
            kpss_values[col] = {
                "stat": kpss_stat,
                "pvalue": pvalue,
                "usedlag": usedlag,
                "critical_values": critical_values,
            }

        return self.cache_results(kpss_values)
