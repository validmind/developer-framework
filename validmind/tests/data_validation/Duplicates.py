# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from typing import List

import pandas as pd

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class Duplicates(ThresholdTest):
    """
    Tests dataset for duplicate entries, ensuring model reliability via data quality verification.

    ### Purpose

    The 'Duplicates' test is designed to check for duplicate rows within the dataset provided to the model. It serves
    as a measure of data quality, ensuring that the model isn't merely memorizing duplicate entries or being swayed by
    redundant information. This is an important step in the pre-processing of data for both classification and
    regression tasks.

    ### Test Mechanism

    This test operates by checking each row for duplicates in the dataset. If a text column is specified in the
    dataset, the test is conducted on this column; if not, the test is run on all feature columns. The number and
    percentage of duplicates are calculated and returned in a DataFrame. Additionally, a test is passed if the total
    count of duplicates falls below a specified minimum threshold.

    ### Signs of High Risk

    - A high number of duplicate rows in the dataset, which can lead to overfitting where the model performs well on
    the training data but poorly on unseen data.
    - A high percentage of duplicate rows in the dataset, indicating potential problems with data collection or
    processing.

    ### Strengths

    - Assists in improving the reliability of the model's training process by ensuring the training data is not
    contaminated with duplicate entries, which can distort statistical analyses.
    - Provides both absolute numbers and percentage values of duplicate rows, giving a thorough overview of data
    quality.
    - Highly customizable as it allows for setting a user-defined minimum threshold to determine if the test has been
    passed.

    ### Limitations

    - Does not distinguish between benign duplicates (i.e., coincidental identical entries in different rows) and
    problematic duplicates originating from data collection or processing errors.
    - The test becomes more computationally intensive as the size of the dataset increases, which might not be suitable
    for very large datasets.
    - Can only check for exact duplicates and may miss semantically similar information packaged differently.
    """

    name = "duplicates"
    required_inputs = ["dataset"]
    default_params = {"min_threshold": 1}
    tasks = ["classification", "regression"]
    tags = ["tabular_data", "data_quality", "text_data"]

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
        """
        The duplicates test returns results like these:
        [{"values": {"n_duplicates": 0, "p_duplicates": 0.0}, "passed": true}]
        So we build a table with 1 row and show number of duplicates and percentage of duplicates.
        """
        result = results[0]
        results_table = [{k: v for k, v in row.items()} for row in result.values]

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
        if self.inputs.dataset.text_column:
            columns = self.inputs.dataset.text_column
        else:
            columns = self.inputs.dataset.feature_columns

        df = self.inputs.dataset.df[columns]
        # Find duplicate rows
        duplicate_rows = df.duplicated()

        # Calculate number of duplicate rows
        duplicate_rows_count = duplicate_rows.sum()

        # Calculate total number of rows
        total_rows = len(df)

        # Calculate percentage of duplicate rows
        percentage_duplicate_rows = (duplicate_rows_count / total_rows) * 100

        # Create a DataFrame with results
        result_df = pd.DataFrame(
            {
                "Number of Duplicates": [duplicate_rows_count],
                "Percentage of Rows (%)": [percentage_duplicate_rows],
            }
        )

        # test has passed if the total sum of duplicates is less than the threshold
        n_duplicates = result_df["Number of Duplicates"].sum()
        passed = n_duplicates < self.params["min_threshold"]

        results = [
            ThresholdTestResult(
                passed=passed,
                values=result_df.to_dict(orient="records"),
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))

    def test(self):
        # Check that result object is not None
        assert self.result is not None
        # Check that we have a list of test results
        assert isinstance(self.result.test_results.results, list)
        # Check if the 'passed' variable in results reflects the test correctly
        for result in self.result.test_results.results[1:]:
            assert result.passed == (
                result.values["n_duplicates"] < self.params["min_threshold"]
            )
        expected_results_count = 1
        assert len(self.result.test_results.results) == expected_results_count
