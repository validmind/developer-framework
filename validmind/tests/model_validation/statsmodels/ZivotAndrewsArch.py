# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from arch.unitroot import ZivotAndrews

from validmind.vm_models import Metric


@dataclass
class ZivotAndrewsArch(Metric):
    """
    **Purpose**: The Zivot-Andrews Arch metric is used to evaluate the order of integration for a time series data in a
    machine learning model. It's designed to test for stationarity, a crucial aspect in time series analysis where data
    points are assumed not to be dependent on time. Stationarity is an indication that the statistical properties such
    as mean, variance and autocorrelation are all constant over time.

    **Test Mechanism**: For each feature in the dataset, the Zivot-Andrews unit root test is performed using
    ZivotAndrews function imported from the arch.unitroot module. It returns the zivot-andrews metric for each feature
    which consists of the statistical value, p-value (probability value), the number of used lags and the number of
    observations. The p-value is then later utilized to make a decision on the null hypothesis (unit root exists,
    series is non-stationary) based on a chosen significance level.

    **Signs of High Risk**: High risk can be suggested by a high p-value. This could imply that there's an insufficient
    basis to reject the null hypothesis, which states that the time series has a unit root and is therefore
    non-stationary. Non-stationary time series data may lead to misleading statistics and unreliable Machine Learning
    models.

    **Strengths**: The Zivot-Andrews Arch metric can dynamically test for stationarity against structural breaks in
    time series data, which provides a robust evaluation of stationarity of features. It becomes very useful in the
    cases of financial, economic or any time-series data where data observations don't have a consistent pattern, and
    structural breaks might occur.

    **Limitations**: The Zivot-Andrews Arch metric test assumes that data under consideration comes from a
    single-equation, autoregressive model. Thus, it may not be suitable for multivariate time series data or data that
    doesn't follow the autoregressive model assumption. Additionally, it might not account for sudden shocks or changes
    in the trend of the time series data which can significantly impact the stationarity of the data.
    """

    name = "zivot_andrews"
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "stationarity", "unit_root_test"],
    }

    def run(self):
        """
        Calculates Zivot-Andrews metric for each of the dataset features
        """
        dataset = self.dataset.df

        za_values = {}
        for col in dataset.columns:
            za = ZivotAndrews(dataset[col].values)
            za_values[col] = {
                "stat": za.stat,
                "pvalue": za.pvalue,
                "usedlag": za.lags,
                "nobs": za.nobs,
            }

        return self.cache_results(za_values)
