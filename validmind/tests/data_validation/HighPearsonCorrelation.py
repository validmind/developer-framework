# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class HighPearsonCorrelation(ThresholdTest):
    """
    **Purpose**: The Pearson Correlation test is intended to measure the linear relationship between features in the
    dataset, specifically ensuring that the pairwise Pearson correlation coefficients do not surpass a certain
    threshold. High correlation between two variables might indicate redundancy or multicollinearity. Identifying such
    correlations can alert the risk management team or developers about issues in the dataset which may have an impact
    on the performance and interpretability of the Machine Learning model.

    **Test Mechanism**: This Python implementation of the test first generates pairwise Pearson correlations for all
    the features in the dataset. It then sorts these correlations and eliminates duplicate and self-correlations (where
    a feature is correlated with itself). A Pass or Fail is assigned based on whether the absolute value of the
    correlation coefficient exceeds a predefined threshold (default to 0.3). The top 10 strongest correlations,
    regardless of whether they pass or fail, are returned.

    **Signs of High Risk**: The presence of correlation coefficients exceeding the specified threshold indicates high
    risk. This means that the features share a strong linear relationship, leading to potential multicollinearity and
    model overfitting. Redundancy of variables can undermine the interpretability of the model because it’s unclear
    which variable's predictive power is true.

    **Strengths**:
    - The Pearson Correlation test is a simple and fast way to identify pairwise relationships between features.
    - Provides clear output: Results show the pairs of correlated variables along with their Pearson correlation
    coefficient and a Pass or Fail status.
    - Helps in early identification of potential multicollinearity issues which can impact model training.

    **Limitations**:
    - Limited to linear relationships only: Pearson correlation cannot depict non-linear relationships or dependencies.
    - Sensitive to outliers: A few outliers can significantly change the correlation coefficient.
    - Redundancy identification only possible for pairwise correlation: If three or more variables are linearly
    dependent, this method might not identify that complex relationship.
    - Top 10 result limitation: It only keeps the top 10 high correlations, which might not fully capture the data's
    complexity. Configuration for the number of kept results needs to be implemented.
    """

    category = "data_quality"
    name = "pearson_correlation"
    required_inputs = ["dataset"]
    default_params = {"max_threshold": 0.3}
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "data_quality", "correlation"],
    }

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
        """
        The high pearson correlation test returns results like these:
        [{"values": {"correlations": [{"column": "NumOfProducts", "correlation": -0.3044645622389459}]}, "column": "Balance", "passed": false}]
        """
        results_table = [
            {
                "Columns": f'({result.column}, {result.values["correlations"][0]["column"]})',
                "Coefficient": result.values["correlations"][0]["correlation"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(
                        title="High Pearson Correlation Results for Dataset"
                    ),
                )
            ]
        )

    def run(self):
        corr = self.dataset.df.corr(numeric_only=True)

        # Create a table of correlation coefficients and column pairs
        corr_table = corr.unstack().sort_values(
            kind="quicksort", key=abs, ascending=False
        )
        corr_df = pd.DataFrame(corr_table).reset_index()
        corr_df.columns = ["Column1", "Column2", "Coefficient"]

        # Remove duplicate correlations and self-correlations
        corr_df = corr_df.loc[corr_df["Column1"] < corr_df["Column2"]]

        # Assign Pass/Fail based on correlation coefficient
        corr_df["Pass/Fail"] = np.where(
            corr_df["Coefficient"].abs() <= self.params["max_threshold"], "Pass", "Fail"
        )

        # Only keep the top 10 correlations. TODO: configurable
        corr_df = corr_df.head(10)

        passed = corr_df["Pass/Fail"].eq("Pass").all()

        results = [
            ThresholdTestResult(
                column=col1,
                values={
                    "correlations": [
                        {
                            "column": col2,
                            "correlation": coeff,
                        }
                    ]
                },
                passed=pass_fail == "Pass",
            )
            for _, (col1, col2, coeff, pass_fail) in corr_df.iterrows()
        ]

        return self.cache_results(results, passed=passed)
