# Copyright © 2023 ValidMind Inc. All rights reserved.

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
    **Purpose**: The “High Cardinality” test functions to assess and evaluate the number of unique values present in
    the categorical columns of a dataset. Cardinality represents the measure of distinct elements residing in a set. In
    context of this test, high cardinality implies presence of a large quantity of unique, non-repetitive values in the
    dataset.

    **Test Mechanism**: This test begins by inferring the type of the dataset and initializing numeric threshold based
    on the test parameters. If the “threshold_type” is set to “percent”, it calculates the numeric threshold as the
    product of “percent_threshold” and the count of rows in the dataset. Subsequently, the test commences iteration
    through each column in the dataset. It limits the evaluation to those columns which are categorized as
    "Categorical". For each categorical column, the number of distinct values (n_distinct) and the percentage of
    distinct values (p_distinct) are computed. The test asserts success if n_distinct is less than the calculated
    numeric threshold. The summary method compiles results in tabulated form, with details for each column including
    column name, number of distinct values, percentage of distinct values, and pass/fail status.

    **Signs of High Risk**: High risk or failure in model performance may be indicated by a large number of distinct
    values (high cardinality) in one or more categorical columns. If any column fails the test (n_distinct >=
    num_threshold), it is a sign of high risk.

    **Strengths**: The High Cardinality test is valuable in detecting overfitting risks and potential noise. High
    cardinality in categorical variables may trigger overfitting in machine learning models as the models can
    excessively adapt to the training data. It also helps in identifying potential outliers and inconsistencies,
    therefore aids in enhancing the data quality. It can be applied to both classification and regression task types,
    which lends versatility to the test.

    **Limitations**: Despite its numerous benefits, the High Cardinality test has certain limitations. It is solely
    applicable to "Categorical" data types, and not suitable for numerical or continuous features, limiting its scope.
    Furthermore, the test does not inherently assert the relevance or importance of unique values in categorical
    features, thus critical data points may be overlooked. The threshold (both number and percent) used for the test is
    static and likely to be non-optimal for diverse datasets and applications, it might benefit from additional
    mechanisms to adapt and fine-tune this dynamic.
    """

    category = "data_quality"
    name = "cardinality"
    required_inputs = ["dataset"]
    default_params = {
        "num_threshold": 100,
        "percent_threshold": 0.1,
        "threshold_type": "percent",  # or "num"
    }
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "data_quality", "categorical_data"],
    }

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
