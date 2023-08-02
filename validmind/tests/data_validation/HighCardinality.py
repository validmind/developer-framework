# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

from pandas_profiling.config import Settings
from pandas_profiling.model.typeset import ProfilingTypeSet

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
)


@dataclass
class HighCardinality(ThresholdTest):
    """
    The high cardinality test measures the number of unique
    values found in categorical columns.
    """

    category = "data_quality"
    name = "cardinality"
    required_context = ["dataset"]
    default_params = {
        "num_threshold": 100,
        "percent_threshold": 0.1,
        "threshold_type": "percent",  # or "num"
    }

    def summary(self, results: List[TestResult], all_passed: bool):
        """
        The high cardinality test returns results like these:
        [{"values": {"n_distinct": 0, "p_distinct": 0.0}, "column": "Exited", "passed": true}]
        """
        results_table = [
            {
                "Column": result.column,
                "Number of Distinct Values": result.values["n_distinct"],
                "Percentage of Distinct Values (%)": result.values["p_distinct"] * 100,
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(
                        title="High Cardinality Results for Dataset"
                    ),
                )
            ]
        )

    def run(self):
        typeset = ProfilingTypeSet(Settings())
        dataset_types = typeset.infer_type(self.dataset.df)

        results = []
        rows = self.dataset.df.shape[0]

        num_threshold = self.params["num_threshold"]
        if self.params["threshold_type"] == "percent":
            num_threshold = int(self.params["percent_threshold"] * rows)

        for col in self.dataset.df.columns:
            # Only calculate high cardinality for categorical columns
            if str(dataset_types[col]) != "Categorical":
                continue

            n_distinct = self.dataset.df[col].nunique()
            p_distinct = n_distinct / rows

            passed = n_distinct < num_threshold

            results.append(
                TestResult(
                    column=col,
                    passed=passed,
                    values={
                        "n_distinct": n_distinct,
                        "p_distinct": p_distinct,
                    },
                )
            )

        return self.cache_results(results, passed=all([r.passed for r in results]))
