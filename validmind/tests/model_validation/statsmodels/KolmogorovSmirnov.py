# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from statsmodels.stats.diagnostic import kstest_normal

from validmind.errors import InvalidTestParametersError
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class KolmogorovSmirnov(Metric):
    """
    Assesses whether each feature in the dataset aligns with a normal distribution using the Kolmogorov-Smirnov test.

    ### Purpose

    The Kolmogorov-Smirnov (KS) test evaluates the distribution of features in a dataset to determine their alignment
    with a normal distribution. This is important because many statistical methods and machine learning models assume
    normality in the data distribution.

    ### Test Mechanism

    This test calculates the KS statistic and corresponding p-value for each feature in the dataset. It does so by
    comparing the cumulative distribution function of the feature with an ideal normal distribution. The KS statistic
    and p-value for each feature are then stored in a dictionary. The p-value threshold to reject the normal
    distribution hypothesis is not preset, providing flexibility for different applications.

    ### Signs of High Risk

    - Elevated KS statistic for a feature combined with a low p-value, indicating a significant divergence from a
    normal distribution.
    - Features with notable deviations that could create problems if the model assumes normality in data distribution.

    ### Strengths

    - The KS test is sensitive to differences in the location and shape of empirical cumulative distribution functions.
    - It is non-parametric and adaptable to various datasets, as it does not assume any specific data distribution.
    - Provides detailed insights into the distribution of individual features.

    ### Limitations

    - The test's sensitivity to disparities in the tails of data distribution might cause false alarms about
    non-normality.
    - Less effective for multivariate distributions, as it is designed for univariate distributions.
    - Does not identify specific types of non-normality, such as skewness or kurtosis, which could impact model fitting.
    """

    name = "kolmogorov_smirnov"
    required_inputs = ["dataset"]
    default_params = {"dist": "norm"}
    tasks = ["classification", "regression"]
    tags = [
        "tabular_data",
        "data_distribution",
        "statistical_test",
        "statsmodels",
    ]

    def summary(self, metric_value):
        results_table = metric_value["metrics_summary"]

        results_table = [
            {"Column": k, "stat": result["stat"], "pvalue": result["pvalue"]}
            for k, result in results_table.items()
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(title="KS Test results"),
                )
            ]
        )

    def run(self):
        """
        Calculates KS for each of the dataset features
        """
        data_distribution = self.params["dist"]
        if data_distribution not in ["norm" or "exp"]:
            InvalidTestParametersError("Dist parameter must be either 'norm' or 'exp'")

        x_train = self.inputs.dataset.df[self.inputs.dataset.feature_columns_numeric]
        ks_values = {}
        for col in x_train.columns:
            ks_stat, p_value = kstest_normal(x_train[col].values, data_distribution)
            ks_values[col] = {"stat": ks_stat, "pvalue": p_value}

        print(ks_values)
        return self.cache_results({"metrics_summary": ks_values})
