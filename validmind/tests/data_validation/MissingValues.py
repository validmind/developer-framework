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
class MissingValues(ThresholdTest):
    """
    Evaluates dataset quality by ensuring missing value ratio across all features does not exceed a set threshold.

    ### Purpose

    The Missing Values test is designed to evaluate the quality of a dataset by measuring the number of missing values
    across all features. The objective is to ensure that the ratio of missing data to total data is less than a
    predefined threshold, defaulting to 1, in order to maintain the data quality necessary for reliable predictive
    strength in a machine learning model.

    ### Test Mechanism

    The mechanism for this test involves iterating through each column of the dataset, counting missing values
    (represented as NaNs), and calculating the percentage they represent against the total number of rows. The test
    then checks if these missing value counts are less than the predefined `min_threshold`. The results are shown in a
    table summarizing each column, the number of missing values, the percentage of missing values in each column, and a
    Pass/Fail status based on the threshold comparison.

    ### Signs of High Risk

    - When the number of missing values in any column exceeds the `min_threshold` value.
    - Presence of missing values across many columns, leading to multiple instances of failing the threshold.

    ### Strengths

    - Quick and granular identification of missing data across each feature in the dataset.
    - Provides an effective and straightforward means of maintaining data quality, essential for constructing efficient
    machine learning models.

    ### Limitations

    - Does not suggest the root causes of the missing values or recommend ways to impute or handle them.
    - May overlook features with significant missing data but still less than the `min_threshold`, potentially
    impacting the model.
    - Does not account for data encoded as values like "-999" or "None," which might not technically classify as
    missing but could bear similar implications.
    """

    name = "missing"
    required_inputs = ["dataset"]
    default_params = {"min_threshold": 1}
    tasks = ["classification", "regression"]
    tags = ["tabular_data", "data_quality"]

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
        rows = self.inputs.dataset.df.shape[0]

        missing = self.inputs.dataset.df.isna().sum()
        results = [
            ThresholdTestResult(
                column=col,
                passed=missing[col] < self.params["min_threshold"],
                values={"n_missing": missing[col], "p_missing": missing[col] / rows},
            )
            for col in missing.index
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))
