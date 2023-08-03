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
class TooManyZeroValues(ThresholdTest):
    """
    The zeros test finds columns that have too many zero values.
    """

    category = "data_quality"
    name = "zeros"
    required_context = ["dataset"]
    default_params = {"max_percent_threshold": 0.03}

    def summary(self, results: List[TestResult], all_passed: bool):
        """
        The zeros test returns results like these:
        [{"values": {"n_zeros": 10000, "p_zeros": 1.0}, "column": "Exited", "passed": true}]
        """
        results_table = [
            {
                "Column": result.column,
                "Number of Zero Values": result.values["n_zeros"],
                "Percentage of Zero Values (%)": result.values["p_zeros"] * 100,
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(title="Zeros Results for Dataset"),
                )
            ]
        )

    def run(self):
        rows = self.dataset.df.shape[0]
        typeset = ProfilingTypeSet(Settings())
        dataset_types = typeset.infer_type(self.dataset.df)
        results = []

        for col in self.dataset.df.columns:
            # Only calculate zeros for numerical columns
            if str(dataset_types[col]) != "Numeric":
                continue

            value_counts = self.dataset.df[col].value_counts()

            if 0 not in value_counts.index:
                continue

            n_zeros = value_counts[0]
            p_zeros = n_zeros / rows

            results.append(
                TestResult(
                    column=col,
                    passed=p_zeros < self.params["max_percent_threshold"],
                    values={
                        "n_zeros": n_zeros,
                        "p_zeros": p_zeros,
                    },
                )
            )

        return self.cache_results(results, passed=all([r.passed for r in results]))
