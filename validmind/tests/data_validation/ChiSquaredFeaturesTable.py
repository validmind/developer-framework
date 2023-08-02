# Copyright © 2023 ValidMind Inc. All rights reserved.

import pandas as pd
from scipy.stats import chi2_contingency
from dataclasses import dataclass
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class ChiSquaredFeaturesTable(Metric):
    """
    Perform a Chi-Squared test of independence for each categorical variable with the target.
    The input dataset and target column are required.
    """

    name = "chi_squared_features_table"
    required_context = ["dataset"]
    default_params = {"cat_features": None, "p_threshold": 0.05}

    def run(self):
        target_column = self.dataset.target_column
        cat_features = self.params["cat_features"]
        p_threshold = self.params["p_threshold"]

        # Ensure cat_features is provided
        if not cat_features:
            raise ValueError("The 'cat_features' parameter must be provided.")

        df = self.dataset.df

        chi_squared_results = self.chi_squared_categorical_feature_selection(
            df, cat_features, target_column, p_threshold
        )

        return self.cache_results(
            {
                "chi_squared_results": chi_squared_results,
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
