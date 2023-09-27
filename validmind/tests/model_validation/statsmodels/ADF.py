# Copyright © 2023 ValidMind Inc. All rights reserved.

from statsmodels.tsa.stattools import adfuller

from validmind.vm_models import Metric


class ADF(Metric):
    """
    **Purpose**: The Augmented Dickey-Fuller (ADF) test is primarily utilized in this scenario to ascertain the order
    of integration of a given time series. In other words, it’s a metric to assess the stationarity of the time series
    data employed in the machine learning model. The stationary property of time series data is critical in many models
    as it directly impacts the reliability and robustness of predictions and forecasts.

    **Test Mechanism**: This test initiates by executing the ADF function from the statsmodels library for every
    feature in the dataset. Each run results in numerous outputs, including the ADF test statistic, the corresponding
    p-value, number of lags used, number of observations included in the test, critical values at different confidence
    levels, and the maximized information criterion. The results are then cached for each attribute for further
    analysis.

    **Signs of High Risk**: Observing a large ADF statistic and high p-value (typically above 0.05) would yet suggest a
    high risk for the model's performance. As both metrics indicate the presence of a unit root, they thus signify
    non-stationarity in the data series. Such characteristics can often lead to unreliable or inadequate forecasts.

    **Strengths**: The ADF test has the advantage of being robust to higher-order correlation within the dataset. This
    intrinsic merit makes it feasible to use in a variety of instances where data may exhibit complex stochastic
    behavior. Additionally, providing detailed information such as test statistics, critical values, and information
    criterion enhances the interpretability and transparency of the model validation process.

    **Limitations**: However, the ADF test does have its share of limitations. It might exhibit low statistical power,
    making it difficult for to distinguish between a unit root and a level of near-unit-root. This may lead to false
    negatives, where the test fails to reject a null hypothesis of a unit root when, in reality, it should.
    Furthermore, the ADF test assumes that the underlying series follows an autoregressive process, which might not
    always be the case. Lastly, handling time series with structural breaks can be challenging.
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
