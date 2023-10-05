# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from statsmodels.tsa.stattools import kpss

from validmind.vm_models import Metric


@dataclass
class KPSS(Metric):
    """
    **Purpose**: The Kwiatkowski-Phillips-Schmidt-Shin (KPSS) unit root test is utilized to check the stationarity of
    data within the machine learning model. It is used on time-series data specifically, to establish the order of
    integration, which in turn helps in providing accurate forecasting. The baseline condition for any time series
    model is that the series should be stationary.

    **Test Mechanism**: Given a dataset, this metric calculates the KPSS score for each feature in the dataset. Each
    KPSS score consists of a statistic, a p-value, a used lag, and critical values. The KPSS score calculates the
    hypothesis that an observable time series is stationary around a deterministic trend. If the calculated statistic
    is greater than the critical value, the null hypothesis is rejected, indicating that the series is not stationary.

    **Signs of High Risk**: High risk in relation to this metric would be signified by a high KPSS score, specifically
    if the calculated statistic is greater than the critical value. This implies that the null hypothesis is rejected
    and the series is not stationary, making the model ineffective for forecasting.

    **Strengths**: The KPSS test has several advantages. It assesses directly the stationarity of a series, which is
    the basic condition of many time-series models and is therefore a crucial step in model validation. Furthermore,
    the underlying intuition of the test is intuitive and straightforward, making it easily understandable for
    developers and risk management teams.

    **Limitations**: Despite its strengths, KPSS does have some limitations. The test assumes the absence of a unit
    root in the series and does not differentiate between series that are stationary and series that are
    near-stationary. The test may also have limited power against certain alternatives, and the validity of the test
    depends on the number of lags chosen.
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
