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
class TooManyZeroValues(ThresholdTest):
    """
    **Purpose**:
    The 'TooManyZeroValues' test is used to identify numerical columns in the data that have an abundance of zero
    values. If a column has too many zeros, it could indicate data sparsity or potential lack of variation, which may
    limit its utility in a machine learning model. The test quantifies 'too many' as a percentage of total values, set
    by default to 3%.

    **Test Mechanism**:
    The application of this test involves iterating over each column of the dataset and determining if the column
    corresponds to numerical data. When a numeric column is identified, the function calculates the total count of zero
    values and their ratio to the total row number. If the proportion exceeds the preset threshold parameter (default
    0.03 or 3%), the column fails the test. The results from each column are summarised in a report that indicates the
    number and the percentage of zero values for each numeric column, along with whether the column passed or failed
    the test.

    **Signs of High Risk**:
    The indicators of high risk associated with this test include:
    1. Numeric columns with a high ratio of zero values to the total number of rows (beyond the set threshold).
    2. Columns where all values registered are zero, implying a complete lack of data variation.

    **Strengths**:
    This test offers several advantages:
    1. Helps in identifying columns with excessive zero values which otherwise might go unnoticed in a large dataset.
    2. Offers flexibility to adjust the threshold of what counts as 'too many' zero values, accommodating the specific
    needs of a given analysis or model.
    3. Reports both the count and percentage of zero values, shedding more light on the distribution and proportion of
    zeros within a column.
    4. Focuses specifically on numerical data, preventing the misapplication to non-numerical columns and avoiding
    false test failures.

    **Limitations**:
    Certain limitation of this metric include:
    1. It merely checks for zero values and does not assess the relevance or the impact of other potentially
    problematic values in the dataset such as extremely high or extremely low numbers, null values or outliers.
    2. It cannot detect a pattern of zeros, which might be important in time series or longitudinal data.
    3. Zeroes might be meaningful in certain contexts, so labelling them as 'too many' could be a misinterpretation of
    the data.
    4. This test does not account for the dataset’s context and disregards that for certain columns, a high presence of
    zero values could be normal and does not necessarily indicate low data quality.
    5. Cannot evaluate non-numerical or categorical columns, that might carry different types of concerns or issues.
    """

    category = "data_quality"
    name = "zeros"
    required_inputs = ["dataset"]
    default_params = {"max_percent_threshold": 0.03}

    metadata = {
        "task_types": ["regression", "classification"],
        "tags": ["tabular_data"],
    }

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
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
                ThresholdTestResult(
                    column=col,
                    passed=p_zeros < self.params["max_percent_threshold"],
                    values={
                        "n_zeros": n_zeros,
                        "p_zeros": p_zeros,
                    },
                )
            )

        return self.cache_results(results, passed=all([r.passed for r in results]))
