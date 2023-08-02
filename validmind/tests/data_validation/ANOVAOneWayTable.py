# Copyright © 2023 ValidMind Inc. All rights reserved.

import pandas as pd
from dataclasses import dataclass
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata
from scipy.stats import f_oneway


@dataclass
class ANOVAOneWayTable(Metric):
    """
    Perform an ANOVA F-test for each numerical variable with the target.
    The input dataset and target column are required.
    """

    name = "anova_one_way_table"
    required_context = ["dataset"]
    default_params = {"num_features": None, "p_threshold": 0.05}

    def run(self):
        target_column = self.dataset.target_column
        num_features = self.params["num_features"]
        p_threshold = self.params["p_threshold"]

        df = self.dataset.df

        anova_results = self.anova_numerical_features(
            df, num_features, target_column, p_threshold
        )

        return self.cache_results(
            {
                "anova_results": anova_results,
            }
        )

    def anova_numerical_features(self, df, features, target, p_threshold):
        # Ensure the columns exist in the dataframe
        for var in features:
            if var not in df.columns:
                raise ValueError(f"The column '{var}' does not exist in the dataframe.")
        if target not in df.columns:
            raise ValueError(
                f"The target column '{target}' does not exist in the dataframe."
            )

        # Ensure the target variable is not included in num_vars
        if target in features:
            features.remove(target)

        results = []

        for var in features:
            # Perform the ANOVA test
            class_0 = df[df[target] == 0][var]
            class_1 = df[df[target] == 1][var]

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
