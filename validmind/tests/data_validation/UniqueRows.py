# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

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
class UniqueRows(ThresholdTest):
    """
    Verifies the diversity of the dataset by ensuring that the count of unique rows exceeds a prescribed threshold.

    ### Purpose

    The UniqueRows test is designed to gauge the quality of the data supplied to the machine learning model by
    verifying that the count of distinct rows in the dataset exceeds a specific threshold, thereby ensuring a varied
    collection of data. Diversity in data is essential for training an unbiased and robust model that excels when faced
    with novel data.

    ### Test Mechanism

    The testing process starts with calculating the total number of rows in the dataset. Subsequently, the count of
    unique rows is determined for each column in the dataset. If the percentage of unique rows (calculated as the ratio
    of unique rows to the overall row count) is less than the prescribed minimum percentage threshold given as a
    function parameter, the test passes. The results are cached and a final pass or fail verdict is given based on
    whether all columns have successfully passed the test.

    ### Signs of High Risk

    - A lack of diversity in data columns, demonstrated by a count of unique rows that falls short of the preset
    minimum percentage threshold, is indicative of high risk.
    - This lack of variety in the data signals potential issues with data quality, possibly leading to overfitting in
    the model and issues with generalization, thus posing a significant risk.

    ### Strengths

    - The UniqueRows test is efficient in evaluating the data's diversity across each information column in the dataset.
    - This test provides a quick, systematic method to assess data quality based on uniqueness, which can be pivotal in
    developing effective and unbiased machine learning models.

    ### Limitations

    - A limitation of the UniqueRows test is its assumption that the data's quality is directly proportionate to its
    uniqueness, which may not always hold true. There might be contexts where certain non-unique rows are essential and
    should not be overlooked.
    - The test does not consider the relative 'importance' of each column in predicting the output, treating all
    columns equally.
    - This test may not be suitable or useful for categorical variables, where the count of unique categories is
    inherently limited.
    """

    name = "unique"
    required_inputs = ["dataset"]
    default_params = {"min_percent_threshold": 1}

    tasks = ["regression", "classification"]
    tags = ["tabular_data"]

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
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
        rows = self.inputs.dataset.df.shape[0]

        unique_rows = self.inputs.dataset.df.nunique()
        results = [
            ThresholdTestResult(
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
