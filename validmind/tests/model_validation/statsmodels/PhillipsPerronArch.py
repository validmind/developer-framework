# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from arch.unitroot import PhillipsPerron

from validmind.vm_models import Metric


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
