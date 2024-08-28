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
class HighCardinality(ThresholdTest):
    """
    Assesses the number of unique values in categorical columns to detect high cardinality and potential overfitting.

    ### Purpose

    The “High Cardinality” test is used to evaluate the number of unique values present in the categorical columns of a
    dataset. In this context, high cardinality implies the presence of a large number of unique, non-repetitive values
    in the dataset.

    ### Test Mechanism

    The test first infers the dataset's type and then calculates an initial numeric threshold based on the test
    parameters. It only considers columns classified as "Categorical". For each of these columns, the number of
    distinct values (n_distinct) and the percentage of distinct values (p_distinct) are calculated. The test will pass
    if n_distinct is less than the calculated numeric threshold. Lastly, the results, which include details such as
    column name, number of distinct values, and pass/fail status, are compiled into a table.

    ### Signs of High Risk

    - A large number of distinct values (high cardinality) in one or more categorical columns implies a high risk.
    - A column failing the test (n_distinct >= num_threshold) is another indicator of high risk.

    ### Strengths

    - The High Cardinality test is effective in early detection of potential overfitting and unwanted noise.
    - It aids in identifying potential outliers and inconsistencies, thereby improving data quality.
    - The test can be applied to both classification and regression task types, demonstrating its versatility.

    ### Limitations

    - The test is restricted to only "Categorical" data types and is thus not suitable for numerical or continuous
    features, limiting its scope.
    - The test does not consider the relevance or importance of unique values in categorical features, potentially
    causing it to overlook critical data points.
    - The threshold (both number and percent) used for the test is static and may not be optimal for diverse datasets
    and varied applications. Further mechanisms to adjust and refine this threshold could enhance its effectiveness.
    """

    name = "cardinality"
    required_inputs = ["dataset"]
    default_params = {
        "num_threshold": 100,
        "percent_threshold": 0.1,
        "threshold_type": "percent",  # or "num"
    }
    tasks = ["classification", "regression"]
    tags = ["tabular_data", "data_quality", "categorical_data"]

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
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
        dataset_types = typeset.infer_type(self.inputs.dataset.df)

        results = []
        rows = self.inputs.dataset.df.shape[0]

        num_threshold = self.params["num_threshold"]
        if self.params["threshold_type"] == "percent":
            num_threshold = int(self.params["percent_threshold"] * rows)

        for col in self.inputs.dataset.df.columns:
            # Only calculate high cardinality for categorical columns
            if str(dataset_types[col]) != "Categorical":
                continue

            n_distinct = self.inputs.dataset.df[col].nunique()
            p_distinct = n_distinct / rows

            passed = n_distinct < num_threshold

            results.append(
                ThresholdTestResult(
                    column=col,
                    passed=passed,
                    values={
                        "n_distinct": n_distinct,
                        "p_distinct": p_distinct,
                    },
                )
            )

        return self.cache_results(results, passed=all([r.passed for r in results]))
