# Copyright © 2023 ValidMind Inc. All rights reserved.

from statsmodels.tsa.stattools import adfuller

from validmind.vm_models import Metric


class ADF(Metric):
    """
    Assesses the stationarity of a time series dataset using the Augmented Dickey-Fuller (ADF) test.

    **Purpose**: The Augmented Dickey-Fuller (ADF) test metric is used here to determine the order of integration,
    i.e., the stationarity of a given time series data. The stationary property of data is pivotal in many machine
    learning models as it impacts the reliability and effectiveness of predictions and forecasts.

    **Test Mechanism**: The ADF test starts by executing the ADF function from the statsmodels library on every feature
    of the dataset. Multiple outputs are generated for each run, including the ADF test statistic and p-value, count of
    lags used, the number of observations factored into the test, critical values at various confidence levels, and the
    maximized information criterion. These results are stored for each feature for subsequent analysis.

    **Signs of High Risk**:
    - An inflated ADF statistic and high p-value (generally above 0.05) insinuate a high risk to the model's
    performance due to the presence of a unit root indicating non-stationarity.
    - Such non-stationarity might result in untrustworthy or insufficient forecasts.

    **Strengths**:
    - The ADF test is robust to more sophisticated correlation within the data, which empowers it to be deployed in
    settings where data might display complex stochastic behavior.
    - The ADF test provides explicit outputs like test statistics, critical values, and information criterion, thereby
    enhancing our understanding and transparency of the model validation process.

    **Limitations**:
    - The ADF test might demonstrate low statistical power, making it challenging to differentiate between a unit root
    and near-unit-root processes causing false negatives.
    - The test assumes the data follows an autoregressive process, which might not be the case all the time.
    - The ADF test finds it demanding to manage time series data with structural breaks.
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
