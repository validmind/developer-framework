# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Threshold based tests
"""

from typing import List
from dataclasses import dataclass

from validmind.vm_models import (
    TestResult,
    ThresholdTest,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)


@dataclass
class Duplicates(ThresholdTest):
    """
    The duplicates test measures the number of duplicate entries found in the text_column
    of the dataset. If a primary key column is specified, the dataset is checked for
    duplicate primary keys as well.
    """

    category = "data_quality"
    # Changing the name test to avoid a name clash
    name = "nlp_duplicates"
    required_context = ["dataset", "dataset.text_column"]
    default_params = {"min_threshold": 1}

    def summary(self, results: List[TestResult], all_passed: bool):
        """
        The duplicates test returns results like these:
        [{"values": {"n_duplicates": 0, "p_duplicates": 0.0}, "passed": true}]

        So we build a table with 1 row and show number of duplicates and percentage of duplicates.
        """
        result = results[0]
        results_table = [
            {
                "Number of Duplicates": result.values["n_duplicates"],
                "Percentage of Duplicates (%)": result.values["p_duplicates"] * 100,
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(
                        title="Duplicate Rows Results for Dataset"
                    ),
                )
            ]
        )

    def run(self):
        rows = self.dataset.df.shape[0]
        n_duplicates = len(
            self.dataset.df[
                self.dataset.df.duplicated(
                    subset=[self.dataset.text_column], keep=False
                )
            ]
        )
        p_duplicates = n_duplicates / rows
        passed = p_duplicates < self.params["min_threshold"]

        results = [
            TestResult(
                passed=passed,
                values={"n_duplicates": n_duplicates, "p_duplicates": p_duplicates},
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))
