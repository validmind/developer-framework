# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from statsmodels.sandbox.stats.runs import runstest_1samp

from validmind.vm_models import Metric


class RunsTest(Metric):
    """
    Executes Runs Test on ML model to detect non-random patterns in output data sequence.

    **Purpose**: The Runs Test is a statistical procedure used to determine whether the sequence of data extracted from
    the ML model behaves randomly or not. Specifically, it analyzes runs, sequences of consecutive positives or
    negatives, in the data to check if there are more or fewer runs than expected under the assumption of randomness.
    This can be an indication of some pattern, trend, or cycle in the model's output which may need attention.

    **Test Mechanism**: The testing mechanism applies the Runs Test from the statsmodels module on each column of the
    training dataset. For every feature in the dataset, a Runs Test is executed, whose output includes a Runs Statistic
    and P-value. A low P-value suggests that data arrangement in the feature is not likely to be random. The results
    are stored in a dictionary where the keys are the feature names, and the values are another dictionary storing the
    test statistic and the P-value for each feature.

    **Signs of High Risk**:
    - High risk is indicated when the P-value is close to zero.
    - If the p-value is less than a predefined significance level (like 0.05), it suggests that the runs (series of
    positive or negative values) in the model's output are not random and are longer or shorter than what is expected
    under a random scenario.
    - This would mean there's a high risk of non-random distribution of errors or model outcomes, suggesting potential
    issues with the model.

    **Strengths**:
    - The strength of the Runs Test is that it's straightforward and fast for detecting non-random patterns in data
    sequence.
    - It can validate assumptions of randomness, which is particularly valuable for checking error distributions in
    regression models, trendless time series data, and making sure a classifier doesn't favour one class over another.
    - Moreover, it can be applied to both classification and regression tasks, making it versatile.

    **Limitations**:
    - The test assumes that the data is independently and identically distributed (i.i.d.), which might not be the case
    for many real-world datasets.
    - The conclusion drawn from the low p-value indicating non-randomness does not provide information about the type
    or the source of the detected pattern.
    - Also, it is sensitive to extreme values (outliers), and overly large or small run sequences can influence the
    results.
    - Furthermore, this test does not provide model performance evaluation; it is used to detect patterns in the
    sequence of outputs only.
    """

    name = "runs_test"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "statistical_test", "statsmodels"],
    }

    def run(self):
        """
        Calculates the run test for each of the dataset features
        """
        x_train = self.inputs.dataset.df

        runs_test_values = {}
        for col in x_train.columns:
            runs_stat, runs_p_value = runstest_1samp(x_train[col].values)

            runs_test_values[col] = {
                "stat": runs_stat,
                "pvalue": runs_p_value,
            }

        return self.cache_results(runs_test_values)
