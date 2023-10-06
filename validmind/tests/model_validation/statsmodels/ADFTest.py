# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from statsmodels.tsa.stattools import adfuller

from validmind.vm_models import ThresholdTest, ThresholdTestResult


@dataclass
class ADFTest(ThresholdTest):
    """
    **Purpose**: The purpose of the Augmented Dickey-Fuller (ADF) metric test is to test the null hypothesis that a
    unit root is present in a time series. In other words, the ADF test aims to check the stationarity of a given
    time-series dataset. It plays a crucial role in the phases of time series analysis, regression tasks, and
    forecasting, as these techniques often require the data to be stationary.

    **Test Mechanism**: The ADF test applies the Python “statsmodels” library's function "adfuller" to each column of
    the training dataset. By doing so, it calculates the ADF statistic, p-value, the number of lags used, and the
    number of observations in the sample for each column. If the p-value for a column is smaller than the predefined
    threshold (typically 0.05), then it is considered as having passed the test, thus concluding that the series is
    stationary.

    **Signs of High Risk**: If the p-value exceeds the threshold value, the test for that column is considered as
    failed, which indicates a high risk or potential model performance issue. A high p-value implies that the null
    hypothesis (indicating a unit root) cannot be rejected, meaning that the series is non-stationary and may cause
    unreliable and spurious results in the model's performance and forecast.

    **Strengths**: The ADF test holds several key advantages:
    1. Test for stationarity: The ADF test provides a rigorous mechanism for testing the stationarity of time series
    data, which is critical for many machine learning and statistical models.
    2. Comprehensive output: The function provides rich output, including the number of lags used and the number of
    observations, which can be useful for understanding the behavior of the series.

    **Limitations**: However, the ADF test also presents some limitations:
    1. Dependence on threshold: The result of the test is highly dependent on the threshold chosen. An inappropriate
    threshold may lead to incorrect rejection or acceptance of the null hypothesis.
    2. Inefficient for trending data: The ADF test assumes no deterministic trend in the data. If a deterministic trend
    exists, the test may identify a stationary series as non-stationary.
    3. May lead to false positive: Particularly for larger datasets, the ADF test tends to reject the null hypothesis
    (indicating a unit root), which can lead to a high propensity for false positives.
    """

    category = "model_performance"  # right now we support "model_performance" and "data_quality"
    name = "adf_test"
    default_params = {"threshold": 0.05}
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
        x_train = self.train_ds.raw_dataset

        results = []
        for col in x_train.columns:
            # adf_values[col] = adfuller(x_train[col].values)
            adf, pvalue, usedlag, nobs, critical_values, icbest = adfuller(
                x_train[col].values
            )

            col_passed = pvalue < self.params["threshold"]
            results.append(
                ThresholdTestResult(
                    column=col,
                    passed=col_passed,
                    values={
                        "adf": adf,
                        "pvalue": pvalue,
                        "usedlag": usedlag,
                        "nobs": nobs,
                        "icbest": icbest,
                    },
                )
            )

        return self.cache_results(results, passed=all([r.passed for r in results]))
