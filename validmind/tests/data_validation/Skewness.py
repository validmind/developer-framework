# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from typing import List

from ydata_profiling.config import Settings
from ydata_profiling.model.typeset import ProfilingTypeSet

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class Skewness(ThresholdTest):
    """
    Evaluates the skewness of numerical data in a dataset to check against a defined threshold, aiming to ensure data
    quality and optimize model performance.

    ### Purpose

    The purpose of the Skewness test is to measure the asymmetry in the distribution of data within a predictive
    machine learning model. Specifically, it evaluates the divergence of said distribution from a normal distribution.
    Understanding the level of skewness helps identify data quality issues, which are crucial for optimizing the
    performance of traditional machine learning models in both classification and regression settings.

    ### Test Mechanism

    This test calculates the skewness of numerical columns in the dataset, focusing specifically on numerical data
    types. The calculated skewness value is then compared against a predetermined maximum threshold, which is set by
    default to 1. If the skewness value is less than this maximum threshold, the test passes; otherwise, it fails. The
    test results, along with the skewness values and column names, are then recorded for further analysis.

    ### Signs of High Risk

    - Substantial skewness levels that significantly exceed the maximum threshold.
    - Persistent skewness in the data, indicating potential issues with the foundational assumptions of the machine
    learning model.
    - Subpar model performance, erroneous predictions, or biased inferences due to skewed data distributions.

    ### Strengths

    - Fast and efficient identification of unequal data distributions within a machine learning model.
    - Adjustable maximum threshold parameter, allowing for customization based on user needs.
    - Provides a clear quantitative measure to mitigate model risks related to data skewness.

    ### Limitations

    - Only evaluates numeric columns, potentially missing skewness or bias in non-numeric data.
    - Assumes that data should follow a normal distribution, which may not always be applicable to real-world data.
    - Subjective threshold for risk grading, requiring expert input and recurrent iterations for refinement.
    """

    name = "skewness"
    required_inputs = ["dataset"]
    default_params = {"max_threshold": 1}
    tasks = ["classification", "regression"]
    tags = ["tabular_data", "data_quality"]

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
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
        dataset_types = typeset.infer_type(self.inputs.dataset.df)

        skewness = self.inputs.dataset.df.skew(numeric_only=True)

        results = []
        passed = []

        for col in skewness.index:
            # Only calculate skewness for numerical columns
            if str(dataset_types[col]) != "Numeric":
                continue

            col_skewness = skewness[col]
            col_pass = abs(col_skewness) < self.params["max_threshold"]
            passed.append(col_pass)
            results.append(
                ThresholdTestResult(
                    column=col,
                    passed=col_pass,
                    values={
                        "skewness": col_skewness,
                    },
                )
            )

        return self.cache_results(results, passed=all(passed))
