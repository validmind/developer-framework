# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from statsmodels.stats.diagnostic import lilliefors

from validmind.vm_models import Metric


@dataclass
class Lilliefors(Metric):
    """
    **Purpose**: The Lilliefors test, named after the Swedish statistician Hubert Lilliefors, is used in this context
    to determine whether the features of the machine learning model's training dataset follow a normal distribution.
    Normality of distribution is a critical assumption in many statistical procedures and machine learning models. If
    the features do not follow a normal distribution, certain types of models may not function optimally, potentially
    leading to inaccurate predictions.

    **Test Mechanism**: The test is applied to every feature column in the training dataset. For each feature, the
    Lilliefors test computes a test statistic and a p-value. The test statistic quantifies how far the distribution of
    the feature is from a perfect normal distribution, while the p-value provides a measure of the statistical
    significance of this deviation. The results are stored in a dictionary where keys are feature column names, and
    values are another dictionary containing the test statistic and p-value.

    **Signs of High Risk**: If the p-value for a feature is less than a predetermined significance level (typically
    0.05), this would indicate that the distribution of the feature significantly deviates from a normal distribution.
    This suggests a high risk as models assuming normality may not work accurately or efficiently with such a feature.

    **Strengths**: This Lilliefors test is particularly useful because it does not require the mean and variance of the
    normal distribution to be known in advance, making it a robust choice for real-world data where these values are
    often unknown. The test is capable of screening every feature column, providing a comprehensive view of the dataset.

    **Limitations**: While the Lilliefors test is a practical tool to gauge normality, it has a few limitations. It can
    only test one-dimensional data, so it is not suited for datasets with interactions between features or
    multi-dimensional phenomena. Additionally, the test may have lower power compared to other tests (like
    Anderson-Darling test) which means it's slightly less sensitive at detecting departures from normality. Finally,
    like any statistical test, it can yield false positives or negatives, so relying on it alone without considering
    other characteristics of the data could be risky.
    """

    name = "lilliefors_test"
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
        x_train = self.train_ds.df

        lilliefors_values = {}
        for col in x_train.columns:
            l_stat, p_value = lilliefors(x_train[col].values)
            lilliefors_values[col] = {
                "stat": l_stat,
                "pvalue": p_value,
            }

        return self.cache_results(lilliefors_values)
