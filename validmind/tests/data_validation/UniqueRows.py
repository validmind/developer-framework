# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
)


@dataclass
class UniqueRows(ThresholdTest):
    """
    Test that the number of unique rows is greater than a threshold
    """

    category = "data_quality"
    name = "unique"
    required_context = ["dataset"]
    default_params = {"min_percent_threshold": 1}

    def summary(self, results: List[TestResult], all_passed: bool):
        """
        The unique rows test returns results like these:
        [{"values": {"n_unique": 10000, "p_unique": 1.0}, "column": "Exited", "passed": true}]
        """
        results_table = [
            {
                "Column": result.column,
                "Number of Unique Values": result.values["n_unique"],
                "Percentage of Unique Values (%)": result.values["p_unique"] * 100,
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(
                        title="Unique Rows Results for Dataset"
                    ),
                )
            ]
        )

    def run(self):
        rows = self.dataset.df.shape[0]

        unique_rows = self.dataset.df.nunique()
        results = [
            TestResult(
                column=col,
                passed=(unique_rows[col] / rows) < self.params["min_percent_threshold"],
                values={
                    "n_unique": unique_rows[col],
                    "p_unique": unique_rows[col] / rows,
                },
            )
            for col in unique_rows.index
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))
