# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd
from scipy.stats import chi2_contingency

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class ChiSquaredFeaturesTable(Metric):
    """
    Executes Chi-Squared test for each categorical feature against a target column to assess significant association.

    **Purpose**: The `ChiSquaredFeaturesTable` metric is used to carry out a Chi-Squared test of independence for each
    categorical feature variable against a designated target column. The primary goal is to determine if a significant
    association exists between the categorical features and the target variable. This method typically finds its use in
    the context of Model Risk Management to understand feature relevance and detect potential bias in a classification
    model.

    **Test Mechanism**: The testing process generates a contingency table for each categorical variable and the target
    variable, after which a Chi-Squared test is performed. Using this approach, the Chi-Squared statistic and the
    p-value for each feature are calculated. The p-value threshold is a modifiable parameter, and a test will qualify
    as passed if the p-value is less than or equal to this threshold. If not, the test is labeled as failed. The
    outcome for each feature - comprising the variable name, Chi-squared statistic, p-value, threshold, and pass/fail
    status - is incorporated into a final summary table.

    **Signs of High Risk**:
    - High p-values (greater than the set threshold) for specific variables could indicate a high risk.
    - These high p-values allude to the absence of a statistically significant relationship between the feature and the
    target variables, resulting in a 'Fail' status.
    - A categorical feature lacking a relevant association with the target variable could be a warning that the machine
    learning model might not be performing optimally.

    **Strengths**:
    - The test allows for a comprehensive understanding of the interaction between a model's input features and the
    target output, thus validating the relevance of categorical features.
    - It also produces an unambiguous 'Pass/Fail' output for each categorical feature.
    - The opportunity to adjust the p-value threshold contributes to flexibility in accommodating different statistical
    standards.

    **Limitations**:
    - The metric presupposes that data is tabular and categorical, which may not always be the case with all datasets.
    - It is distinctively designed for classification tasks, hence unsuitable for regression scenarios.
    - The Chi-squared test, akin to any hypothesis testing-based test, cannot identify causal relationships, but only
    associations.
    - Furthermore, the test hinges on an adjustable p-value threshold, and varying threshold selections might lead to
    different conclusions regarding feature relevance.
    """

    name = "chi_squared_features_table"
    required_inputs = ["dataset"]
    default_params = {"cat_features": None, "p_threshold": 0.05}
    tasks = ["classification"]
    tags = [
        "tabular_data",
        "categorical_data",
        "statistical_test",
        "binary_classification",
        "multiclass_classification",
    ]

    def run(self):
        target_column = self.inputs.dataset.target_column
        cat_features = self.params["cat_features"]
        p_threshold = self.params["p_threshold"]

        # Ensure cat_features is provided
        if not cat_features:
            cat_features = self.inputs.dataset.feature_columns_categorical

        df = self.inputs.dataset.df

        chi_squared_results = self.chi_squared_categorical_feature_selection(
            df, cat_features, target_column, p_threshold
        )

        return self.cache_results(
            {
                "chi_squared_results": chi_squared_results.to_dict(orient="records"),
            }
        )

    def chi_squared_categorical_feature_selection(
        self, df, cat_features, target, p_threshold
    ):
        # Ensure the columns exist in the dataframe
        for var in cat_features:
            if var not in df.columns:
                raise ValueError(f"The column '{var}' does not exist in the dataframe.")
        if target not in df.columns:
            raise ValueError(
                f"The target column '{target}' does not exist in the dataframe."
            )

        results = []

        for var in cat_features:
            # Create a contingency table
            contingency_table = pd.crosstab(df[var], df[target])

            # Perform the Chi-Square test
            chi2, p, _, _ = chi2_contingency(contingency_table)

            # Add the result to the list of results
            results.append(
                [var, chi2, p, p_threshold, "Pass" if p <= p_threshold else "Fail"]
            )

        # Convert results to a DataFrame and return
        results_df = pd.DataFrame(
            results,
            columns=[
                "Variable",
                "Chi-squared statistic",
                "p-value",
                "Threshold",
                "Pass/Fail",
            ],
        )

        # Sort by p-value in ascending order
        results_df = results_df.sort_values(by="p-value")

        return results_df

    def summary(self, metric_value):
        chi_squared_results_table = metric_value["chi_squared_results"]
        return ResultSummary(
            results=[
                ResultTable(
                    data=chi_squared_results_table,
                    metadata=ResultTableMetadata(
                        title="Chi-Squared Test Results for Categorical Features"
                    ),
                )
            ]
        )
