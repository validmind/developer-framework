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
class Skewness(ThresholdTest):
    """
    The skewness test measures the extent to which a distribution of
    values differs from a normal distribution. A positive skew describes
    a longer tail of values in the right and a negative skew describes a
    longer tail of values in the left.
    """

    category = "data_quality"
    name = "skewness"
    required_context = ["dataset"]
    default_params = {"max_threshold": 1}

    def summary(self, results: List[TestResult], all_passed: bool):
        """
        The skewness test returns results like these:
        [{"values": {"skewness": 1.0}, "column": "NumOfProducts", "passed": false}]
        """
        results_table = [
            {
                "Column": result.column,
                "Skewness": result.values["skewness"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(title="Skewness Results for Dataset"),
                )
            ]
        )

    def run(self):
        typeset = ProfilingTypeSet(Settings())
        dataset_types = typeset.infer_type(self.dataset.df)

        skewness = self.dataset.df.skew(numeric_only=True)
        passed = all(abs(skewness) < self.params["max_threshold"])
        results = []

        for col in skewness.index:
            # Only calculate skewness for numerical columns
            if str(dataset_types[col]) != "Numeric":
                continue

            col_skewness = skewness[col]
            results.append(
                TestResult(
                    column=col,
                    passed=abs(col_skewness) < self.params["max_threshold"],
                    values={
                        "skewness": col_skewness,
                    },
                )
            )

        return self.cache_results(results, passed=passed)
