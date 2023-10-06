# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class MissingValues(ThresholdTest):
    """
    **Purpose**: This test is designed to measure the number of missing values in the dataset across all the features.
    This offers a way to evaluate the data quality, which is crucial to the predictive strength and reliability of any
    machine learning model. It aims to ensure that the ratio of missing data to total data is less than a predefined
    threshold, which in this case defaults to 1.

    **Test Mechanism**: The test iteratively runs through each column in the dataset, counting the number of missing
    values (NaNs) and calculating the percentage of missing values compared to the total number of rows. It then checks
    if the number of missing values is less than the pre-defined `min_threshold`. The results are summarized in a table
    that lists each column, the number of missing values, the percentage of missing values in each column, and a
    Pass/Fail status based on the comparison with the threshold.

    **Signs of High Risk**: A high risk is indicated when the number of missing values in any column exceeds the
    `min_threshold` value. Another sign of high risk is when there are missing values spread across many columns. In
    both cases, the test would issue a "Fail" mark on the Pass/Fail status.

    **Strengths**: This test helps to identify the presence and extent of missing data quickly and at a granular level
    (each feature in the dataset). It provides an effective and straightforward way to maintain data quality, which is
    crucial for building effective machine learning models.

    **Limitations**: While the test can efficiently detect missing data, it does not address the root causes of these
    missing values or suggest ways to impute or handle such values. It also does not consider situations where a
    feature has a significant amount of missing values, but still less than the `min_threshold`, which might also
    affect the model in cases where `min_threshold` is set too high. Lastly, this test does not account for data
    encoded as values (e.g., "-999" or "None"), which may technically not be missing but could carry the same
    implications.
    """

    category = "data_quality"
    name = "missing"
    required_inputs = ["dataset"]
    default_params = {"min_threshold": 1}
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "data_quality"],
    }

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
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
            ThresholdTestResult(
                column=col,
                passed=missing[col] < self.params["min_threshold"],
                values={"n_missing": missing[col], "p_missing": missing[col] / rows},
            )
            for col in missing.index
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))
