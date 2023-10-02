# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
from scipy.stats import chi2_contingency

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class ChiSquaredFeaturesTable(Metric):
    """
    **Purpose**: The purpose of this metric, `ChiSquaredFeaturesTable`, is to perform a Chi-Squared test of
    independence for each categorical feature variable with a given target column. The Chi-Squared test is designed to
    determine if there's a significant association between the categorical features and the target variable. It is
    typically used in the context of Model Risk Management to comprehend feature relevance and identify potential bias
    in a classification model.

    **Test Mechanism**: This test involves creating a contingency table for each categorical variable and the target
    variable, and then performing a Chi-Squared test. The Chi-Squared statistic and the p-value for each feature are
    calculated using this method. The p-value threshold is a parameter that can be adjusted, and a test will pass if
    the p-value is less than or equal to this threshold. If not, the test will fail. The test result for each feature -
    consisting of variable name, Chi-squared statistic, p-value, threshold, and pass/fail status - is aggregated into a
    final summary table.

    **Signs of High Risk**: Red Flags for high risk include high p-values (greater than the set threshold) for certain
    variables. These high p-values suggest there is not a statistically significant relationship between the feature
    and the target variables, resulting in a 'Fail' status. If a categorical feature has no relevant association with
    the target variable, it can signal that the machine learning model may not be performing well.

    **Strengths**: This test allows for a thorough examination of the interaction between a model's input features and
    the target output, helping to validate the relevance of the categorical features. It also provides a clear
    'Pass/Fail' output for each categorical feature. The ability to adjust the p-value threshold adds flexibility to
    suit different statistical standards.

    **Limitations**: The metric assumes that the data is tabular and categorical, which may not apply to all datasets.
    It is specifically designed for classification tasks and not suitable for regression scenarios. It's also important
    to remember that the Chi-squared test, like any test based on hypothesis testing, is not able to identify causal
    relationships; it can only reveal associations. Moreover, the test relies on an adjustable p-value threshold, and
    different threshold choices may lead to different conclusions about feature relevance.
    """

    name = "chi_squared_features_table"
    required_inputs = ["dataset"]
    default_params = {"cat_features": None, "p_threshold": 0.05}
    metadata = {
        "task_types": ["classification"],
        "tags": [
            "tabular_data",
            "categorical_data",
            "statistical_test",
            "binary_classification",
            "multiclass_classification",
        ],
    }

    def run(self):
        target_column = self.dataset.target_column
        cat_features = self.params["cat_features"]
        p_threshold = self.params["p_threshold"]

        # Ensure cat_features is provided
        if not cat_features:
            cat_features = self.dataset.get_categorical_features_columns()

        df = self.dataset.df

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
