# Copyright © 2023 ValidMind Inc. All rights reserved.

from statsmodels.tsa.stattools import adfuller

from validmind.vm_models import Metric


class ADF(Metric):
    """
    Augmented Dickey-Fuller unit root test for establishing the order of integration of
    time series
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

    def run(self):
        """
        Calculates ADF metric for each of the dataset features
        """
        dataset = self.dataset.df

        adf_values = {}
        for col in dataset.columns:
            adf, pvalue, usedlag, nobs, critical_values, icbest = adfuller(
                dataset[col].values
            )
            adf_values[col] = {
                "stat": adf,
                "pvalue": pvalue,
                "usedlag": usedlag,
                "nobs": nobs,
                "critical_values": critical_values,
                "icbest": icbest,
            }

        return self.cache_results(adf_values)
