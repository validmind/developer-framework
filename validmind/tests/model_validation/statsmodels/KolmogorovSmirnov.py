# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from statsmodels.stats.diagnostic import kstest_normal

from validmind.vm_models import Metric


@dataclass
class KolmogorovSmirnov(Metric):
    """
    **Purpose**: The Kolmogorov-Smirnov (KS) test featured in this metric is aimed at evaluating the distribution of a
    dataset's features. Particularly, it assesses whether each feature's data follows a normal distribution, which is a
    crucial assumption in many statistical methods and machine learning models.

    **Test Mechanism**: The KS test implemented here computes the KS statistic and the corresponding p-value for each
    column in a dataset. These values are determined by comparing the cumulative distribution function of the dataset's
    feature with a theoretical normal distribution. A feature-wise KS statistic and p-value are then stored in a
    dictionary. The threshold p-value, below which the null hypothesis (that the data comes from a normal distribution)
    can be rejected, is not explicitly set in this implementation and can be defined in accordance with the specific
    application.

    **Signs of High Risk**: A higher KS statistic for a feature and a low p-value would suggest a significant
    discrepancy between that feature's distribution and a normal distribution. Features with substantial deviations
    might cause problems if the model in use assumes a normal distribution of data, hence pose a risk.

    **Strengths**: The KS test is sensitive to differences in both the location and shape of the empirical cumulative
    distribution functions of two samples. It's non-parametric and doesn't assume any specific distribution for the
    data, making it versatile for various datasets. Being a feature-oriented test, it provides granular insights about
    the data distribution.

    **Limitations**: The KS test may be overly sensitive to deviations in the tails of the data distribution,
    potentially flagging them as non-normal even in cases where these deviations are not necessarily a concern for the
    model. Moreover, the test could become less powerful with multivariate distributions since it's primarily used for
    univariate distributions. Also, as it's a goodness-of-fit test, it does not point out specific forms of
    non-normality such as skewness or kurtosis that could be relevant for model fitting.
    """

    name = "kolmogorov_smirnov"
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
        Calculates KS for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        ks_values = {}
        for col in x_train.columns:
            ks_stat, p_value = kstest_normal(x_train[col].values, "norm")
            ks_values[col] = {"stat": ks_stat, "pvalue": p_value}

        return self.cache_results(ks_values)
