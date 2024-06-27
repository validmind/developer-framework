# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd
from scipy.stats import f_oneway

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class ANOVAOneWayTable(Metric):
    """
    Applies one-way ANOVA (Analysis of Variance) to identify statistically significant numerical features in the
    dataset.

    **Purpose**: The ANOVA (Analysis of Variance) One-Way Table metric is utilized to determine whether the mean of
    numerical variables differs across different groups identified by target or categorical variables. Its primary
    purpose is to scrutinize the significant impact of categorical variables on numerical ones. This method proves
    essential in identifying statistically significant features corresponding to the target variable present in the
    dataset.

    **Test Mechanism**: The testing mechanism involves the ANOVA F-test's performance on each numerical variable
    against the target. If no specific features are mentioned, all numerical features are tested. A p-value is produced
    for each test and compared against a certain threshold (default being 0.05 if not specified). If the p-value is
    less than or equal to this threshold, the feature is marked as 'Pass', indicating significant mean difference
    across the groups. Otherwise, it's marked as 'Fail'. The test produces a DataFrame that includes variable name, F
    statistic value, p-value, threshold, and pass/fail status for every numerical variable.

    **Signs of High Risk**:
    - A large number of 'Fail' results in the ANOVA F-test could signify high risk or underperformance in the model.
    This issue may arise when multiple numerical variables in the dataset don't exhibit any significant difference
    across the target variable groups.
    - Features with high p-values also indicate a high risk as they imply a greater chance of obtaining observed data
    given that the null hypothesis is true.

    **Strengths**:
    - The ANOVA One Way Table is highly efficient in identifying statistically significant features by simultaneously
    comparing group means.
    - Its flexibility allows the testing of all numerical features in the dataset when no specific ones are mentioned.
    - This metric provides a convenient method to measure the statistical significance of numerical variables and
    assists in selecting those variables influencing the classifier's predictions considerably.

    **Limitations**:
    - This metric assumes that the data is normally distributed, which may not always be the case leading to erroneous
    test results.
    - The sensitivity of the F-test to variance changes may hinder this metric's effectiveness, especially for datasets
    with high variance.
    - The ANOVA One Way test does not specify which group means differ statistically from others; it strictly asserts
    the existence of a difference.
    - The metric fails to provide insights into variable interactions, and significant effects due to these
    interactions could easily be overlooked.
    """

    name = "anova_one_way_table"
    required_inputs = ["dataset"]
    default_params = {"features": None, "p_threshold": 0.05}
    tasks = ["classification"]
    tags = [
        "tabular_data",
        "statistical_test",
        "multiclass_classification",
        "binary_classification",
        "numerical_data",
    ]

    def run(self):
        features = self.params["features"]
        p_threshold = self.params["p_threshold"]

        # Select all numerical features if none are specified
        if features is None:
            features = self.inputs.dataset.feature_columns_numeric

        anova_results = self.anova_numerical_features(features, p_threshold)

        return self.cache_results(
            {
                "anova_results": anova_results.to_dict(orient="records"),
            }
        )

    def anova_numerical_features(self, features, p_threshold):
        target_column = self.inputs.dataset.target_column
        df = self.inputs.dataset.df

        # Ensure the columns exist in the dataframe
        for var in features:
            if var not in df.columns:
                raise ValueError(f"The column '{var}' does not exist in the dataframe.")
        if target_column not in df.columns:
            raise ValueError(
                f"The target column '{target_column}' does not exist in the dataframe."
            )

        # Ensure the target variable is not included in num_vars
        if target_column in features:
            features.remove(target_column)

        results = []

        for var in features:
            # Perform the ANOVA test
            class_0 = df[df[target_column] == 0][var]
            class_1 = df[df[target_column] == 1][var]

            f, p = f_oneway(class_0, class_1)

            # Add the result to the list of results
            results.append(
                [var, f, p, p_threshold, "Pass" if p <= p_threshold else "Fail"]
            )

        # Convert results to a DataFrame and return
        results_df = pd.DataFrame(
            results,
            columns=["Variable", "F statistic", "p-value", "Threshold", "Pass/Fail"],
        )

        # Sort by p-value in ascending order
        results_df = results_df.sort_values(by="p-value")

        return results_df

    def summary(self, metric_value):
        anova_results_table = metric_value["anova_results"]
        return ResultSummary(
            results=[
                ResultTable(
                    data=anova_results_table,
                    metadata=ResultTableMetadata(
                        title="ANOVA F-Test Results for Numerical Features"
                    ),
                )
            ]
        )
