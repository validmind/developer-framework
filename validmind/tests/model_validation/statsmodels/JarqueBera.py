# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from statsmodels.stats.stattools import jarque_bera

from validmind.vm_models import Metric


class JarqueBera(Metric):
    """
    Assesses normality of dataset features in an ML model using the Jarque-Bera test.

    **Purpose**: The purpose of the Jarque-Bera test as implemented in this metric is to determine if the features in
    the dataset of a given Machine Learning model follows a normal distribution. This is crucial for understanding the
    distribution and behavior of the model's features, as numerous statistical methods assume normal distribution of
    the data.

    **Test Mechanism**: The test mechanism involves computing the Jarque-Bera statistic, p-value, skew, and kurtosis
    for each feature in the dataset. It utilizes the 'jarque_bera' function from the 'statsmodels' library in Python,
    storing the results in a dictionary. The test evaluates the skewness and kurtosis to ascertain whether the dataset
    follows a normal distribution. A significant p-value (typically less than 0.05) implies that the data does not
    possess normal distribution.

    **Signs of High Risk**:
    - A high Jarque-Bera statistic and a low p-value (usually less than 0.05) indicates high-risk conditions.
    - Such results suggest the data significantly deviates from a normal distribution. If a machine learning model
    expects feature data to be normally distributed, these findings imply that it may not function as intended.

    **Strengths**:
    - This test provides insights into the shape of the data distribution, helping determine whether a given set of
    data follows a normal distribution.
    - This is particularly useful for risk assessment for models that assume a normal distribution of data.
    - By measuring skewness and kurtosis, it provides additional insights into the nature and magnitude of a
    distribution's deviation.

    **Limitations**:
    - The Jarque-Bera test only checks for normality in the data distribution. It cannot provide insights into other
    types of distributions.
    - Datasets that aren't normally distributed but follow some other distribution might lead to inaccurate risk
    assessments.
    - The test is highly sensitive to large sample sizes, often rejecting the null hypothesis (that data is normally
    distributed) even for minor deviations in larger datasets.
    """

    name = "jarque_bera"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": [
            "tabular_data",
            "data_distribution",
            "statistical_test",
            "statsmodels",
        ],
    }

    def run(self):
        """
        Calculates JB for each of the dataset features
        """
        x_train = self.inputs.dataset.df

        jb_values = {}
        for col in x_train.columns:
            jb_stat, jb_pvalue, jb_skew, jb_kurtosis = jarque_bera(x_train[col].values)

            jb_values[col] = {
                "stat": jb_stat,
                "pvalue": jb_pvalue,
                "skew": jb_skew,
                "kurtosis": jb_kurtosis,
            }

        return self.cache_results(jb_values)
