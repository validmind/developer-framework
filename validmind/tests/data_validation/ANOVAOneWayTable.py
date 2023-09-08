# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
from scipy.stats import f_oneway

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class ANOVAOneWayTable(Metric):
    """
    Perform an ANOVA F-test for each numerical variable with the target.
    The input dataset and target column are required.
    """

    name = "anova_one_way_table"
    required_inputs = ["dataset"]
    default_params = {"features": None, "p_threshold": 0.05}

    def run(self):
        features = self.params["features"]
        p_threshold = self.params["p_threshold"]

        # Select all numerical features if none are specified
        if features is None:
            features = self.dataset.get_numeric_features_columns()

        anova_results = self.anova_numerical_features(features, p_threshold)

        return self.cache_results(
            {
                "anova_results": anova_results.to_dict(orient="records"),
            }
        )

    def anova_numerical_features(self, features, p_threshold):
        target_column = self.dataset.target_column
        df = self.dataset.df

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
