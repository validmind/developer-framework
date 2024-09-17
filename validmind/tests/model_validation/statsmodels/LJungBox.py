# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from statsmodels.stats.diagnostic import acorr_ljungbox

from validmind.vm_models import Metric


class LJungBox(Metric):
    """
    Assesses autocorrelations in dataset features by performing a Ljung-Box test on each feature.

    ### Purpose

    The Ljung-Box test is a type of statistical test utilized to ascertain whether there are autocorrelations within a
    given dataset that differ significantly from zero. In the context of a machine learning model, this test is
    primarily used to evaluate data utilized in regression tasks, especially those involving time series and
    forecasting.

    ### Test Mechanism

    The test operates by iterating over each feature within the training dataset and applying the `acorr_ljungbox`
    function from the `statsmodels.stats.diagnostic` library. This function calculates the Ljung-Box statistic and
    p-value for each feature. These results are then stored in a dictionary where the keys are the feature names and
    the values are dictionaries containing the statistic and p-value respectively. Generally, a lower p-value indicates
    a higher likelihood of significant autocorrelations within the feature.

    ### Signs of High Risk

    - High Ljung-Box statistic values or low p-values.
    - Presence of significant autocorrelations in the respective features.
    - Potential for negative impact on model performance or bias if autocorrelations are not properly handled.

    ### Strengths

    - Powerful tool for detecting autocorrelations within datasets, especially in time series data.
    - Provides quantitative measures (statistic and p-value) for precise evaluation.
    - Helps avoid issues related to autoregressive residuals and other challenges in regression models.

    ### Limitations

    - Cannot detect all types of non-linearity or complex interrelationships among variables.
    - Testing individual features may not fully encapsulate the dynamics of the data if features interact with each
    other.
    - Designed more for traditional statistical models and may not be fully compatible with certain types of complex
    machine learning models.
    """

    name = "ljung_box"
    required_inputs = ["dataset"]
    tasks = ["regression"]
    tags = ["time_series_data", "forecasting", "statistical_test", "statsmodels"]

    def run(self):
        """
        Calculates Ljung-Box test for each of the dataset features
        """
        x_train = self.inputs.dataset.df

        ljung_box_values = {}
        for col in x_train.columns:
            lb_results = acorr_ljungbox(x_train[col].values, return_df=True)

            ljung_box_values[col] = {
                "stat": lb_results["lb_stat"].values[0],
                "pvalue": lb_results["lb_pvalue"].values[0],
            }

        return self.cache_results(ljung_box_values)
