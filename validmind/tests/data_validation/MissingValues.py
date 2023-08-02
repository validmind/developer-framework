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
class MissingValues(ThresholdTest):
    """
    Test that the number of missing values in the dataset across all features
    is less than a threshold
    """

    category = "data_quality"
    name = "missing"
    required_context = ["dataset"]
    default_params = {"min_threshold": 1}

    def summary(self, results: List[TestResult], all_passed: bool):
        """
        The missing values test returns results like these:
        [{"values": {"n_missing": 0, "p_missing": 0.0}, "column": "Exited", "passed": true}]
        """
        results_table = [
            {
                "Column": result.column,
                "Number of Missing Values": result.values["n_missing"],
                "Percentage of Missing Values (%)": result.values["p_missing"] * 100,
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(
                        title="Missing Values Results for Dataset"
                    ),
                )
            ]
        )

    def run(self):
        rows = self.dataset.df.shape[0]

        missing = self.dataset.df.isna().sum()
        results = [
            TestResult(
                column=col,
                passed=missing[col] < self.params["min_threshold"],
                values={"n_missing": missing[col], "p_missing": missing[col] / rows},
            )
            for col in missing.index
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))
