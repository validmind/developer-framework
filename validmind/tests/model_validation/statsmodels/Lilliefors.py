# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from statsmodels.stats.diagnostic import lilliefors

from validmind.vm_models import Metric


@dataclass
class Lilliefors(Metric):
    """
    Assesses the normality of feature distributions in an ML model's training dataset using the Lilliefors test.

    **Purpose**: The purpose of this metric is to utilize the Lilliefors test, named in honor of the Swedish
    statistician Hubert Lilliefors, in order to assess whether the features of the machine learning model's training
    dataset conform to a normal distribution. This is done because the assumption of normal distribution plays a vital
    role in numerous statistical procedures as well as numerous machine learning models. Should the features fail to
    follow a normal distribution, some model types may not operate at optimal efficiency. This can potentially lead to
    inaccurate predictions.

    **Test Mechanism**: The application of this test happens across all feature columns within the training dataset.
    For each feature, the Lilliefors test returns a test statistic and p-value. The test statistic quantifies how far
    the feature's distribution is from an ideal normal distribution, whereas the p-value aids in determining the
    statistical relevance of this deviation. The final results are stored within a dictionary, the keys of which
    correspond to the name of the feature column, and the values being another dictionary which houses the test
    statistic and p-value.

    **Signs of High Risk**:

    - If the p-value corresponding to a specific feature sinks below a pre-established significance level, generally
    set at 0.05, then it can be deduced that the distribution of that feature significantly deviates from a normal
    distribution. This can present a high risk for models that assume normality, as these models may perform
    inaccurately or inefficiently in the presence of such a feature.

    **Strengths**:

    - One advantage of the Lilliefors test is its utility irrespective of whether the mean and variance of the normal
    distribution are known in advance. This makes it a more robust option in real-world situations where these values
    might not be known.
    - Second, the test has the ability to screen every feature column, offering a holistic view of the dataset.

    **Limitations**:

    - Despite the practical applications of the Lilliefors test in validating normality, it does come with some
    limitations.
    - Firstly, it is only capable of testing unidimensional data, thus rendering it ineffective for datasets with
    interactions between features or multi-dimensional phenomena.
    - Additionally, the test might not be as sensitive as some other tests (like the Anderson-Darling test) in
    detecting deviations from a normal distribution.
    - Lastly, like any other statistical test, Lilliefors test may also produce false positives or negatives. Hence,
    banking solely on this test, without considering other characteristics of the data, may give rise to risks.
    """

    name = "lilliefors_test"
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
        Calculates Lilliefors test for each of the dataset features
        """
        x_train = self.train_ds.df

        lilliefors_values = {}
        for col in x_train.columns:
            l_stat, p_value = lilliefors(x_train[col].values)
            lilliefors_values[col] = {
                "stat": l_stat,
                "pvalue": p_value,
            }

        return self.cache_results(lilliefors_values)
