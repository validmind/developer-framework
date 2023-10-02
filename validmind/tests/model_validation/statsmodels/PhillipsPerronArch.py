# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from arch.unitroot import PhillipsPerron

from validmind.vm_models import Metric


@dataclass
class PhillipsPerronArch(Metric):
    """
    **Purpose**: The Phillips-Perron (PP) test is being used to establish the order of integration in time series data.
    It is a method for testing a null hypothesis that a time series is unit-root non-stationary. When applied to
    machine learning models, it helps in forecasting and understanding the stochastic behavior of data. In sense, it is
    used to ensure the robustness of the results and make valid predictions out of regression analysis models.

    **Test Mechanism**: The PP test is applied to each feature present in the dataset. A data frame is acquired from
    the dataset and for each column in this data frame, the PhillipsPerron method is used to calculate its statistic
    value, p-value, used lags and number of observations. This method is calculating the PP metric for each feature and
    caching the results.

    **Signs of High Risk**: Indicators of high risk related to this metric could include:
    - High P-value, which might suggest that the series has a unit root and thus is non-stationary.
    - Test statistic values that exceed the critical values, providing further evidence of non-stationarity.
    - If the 'usedlag' value is high for a series, there may be autocorrelation issues which can further complicate
    model performance.

    **Strengths**: The strengths of the PP test are as follows:
    - It is robust against heteroskedasticity in the error term.
    - It examines relatively long time series.
    - It helps to identify if the time series is stationary or not, which affects the selection of appropriate models
    for forecasting.

    **Limitations**: However, the PP test has some limitations:
    - It can only be utilized in a univariate time series framework.
    - The PP test does rely on asymptotic theory, therefore, for small sample sizes the power of the test can
    substantially reduce.
    - Non-stationary time series might require differencing to convert them into stationary series, which might lead to
    loss of important data points.
    """

    name = "phillips_perron"
    metadata = {
        "task_types": ["regression"],
        "tags": [
            "time_series_data",
            "forecasting",
            "statistical_test",
            "unit_root_test",
        ],
    }

    def run(self):
        """
        Calculates PP metric for each of the dataset features
        """
        dataset = self.dataset.df

        pp_values = {}
        for col in dataset.columns:
            pp = PhillipsPerron(dataset[col].values)
            pp_values[col] = {
                "stat": pp.stat,
                "pvalue": pp.pvalue,
                "usedlag": pp.lags,
                "nobs": pp.nobs,
            }

        return self.cache_results(pp_values)
