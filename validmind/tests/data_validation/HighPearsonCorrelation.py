# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
)


@dataclass
class HighPearsonCorrelation(ThresholdTest):
    """
    Test that the pairwise Pearson correlation coefficients between the
    features in the dataset do not exceed a specified threshold.
    """

    category = "data_quality"
    name = "pearson_correlation"
    required_context = ["dataset"]
    default_params = {"max_threshold": 0.3}

    def summary(self, results: List[TestResult], all_passed: bool):
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
            TestResult(
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
