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
class Duplicates(ThresholdTest):
    """
    Checks for and quantifies the presence of duplicate entries in the dataset or a specified column.

    **Purpose**: The Duplicates test is designed to assess the data quality of an ML model by identifying any duplicate
    entries in the data set. It focuses on seeking out duplication in a specified text column or among the primary keys
    of the data set, which could have serious implications for the performance and integrity of the model. Duplicate
    entries could potentially skew the data distribution and influence model training inaccurately.

    **Test Mechanism**: This test operates by calculating the total number of duplicate entries in the data set. The
    algorithm will count duplicates within the 'text_column' if this property is specified. If primary keys are
    defined, the test will also be applied on them. The count of duplicates ('n_duplicates') is then compared to a
    predefined minimum threshold (the default 'min_threshold' is set at 1) to determine whether the test has passed or
    not. The results include the total number of duplicates as well as the percentage of duplicate rows in comparison
    to the overall dataset ('p_duplicates').

    **Signs of High Risk**:
    - A large amount of duplicates, particularly those exceeding the predefined minimum threshold, point toward a high
    risk situation.
    - Overrepresentation of certain data which can lead to skewed results.
    - Indication of inefficient data collecting techniques leading to data redundancy.
    - Models that fail this test predominantly may necessitate a closer examination of their data preprocessing methods
    or source data.

    **Strengths**:
    - The Duplicates test is highly adaptable, being capable of being used with both text data and tabular data formats.
    - It is able to provide results both numerically and as a percentage of the total data set, allowing for a broader
    understanding of the extent of duplication.
    - Its utility lies in effectively flagging any data quality issues that could potentially upset model performance
    and generate erroneous predictions.

    **Limitations**:
    - The Duplicates test solely targets exact duplication in entries, meaning it may overlook near-duplicates or
    normalized forms of entries that might also affect data distribution and model integrity.
    - Data variations caused by errors, phrasing changes, or inconsistencies may not be detected.
    - A substantial number of duplicates in a datasets may not always denote poor data quality, as this can be
    dependent on the nature of the data and the problem being addressed.
    """

    category = "data_quality"
    name = "duplicates"
    required_inputs = ["dataset"]
    default_params = {"min_threshold": 1}
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "data_quality", "text_data"],
    }

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
        rows = self.dataset.df.shape[0]

        duplicate_rows_query = {"keep": False}
        if self.dataset.text_column:
            duplicate_rows_query["subset"] = [self.dataset.text_column]

        duplicate_rows = self.dataset.df[
            self.dataset.df.duplicated(**duplicate_rows_query)
        ]

        duplicate_rows_group_by = (
            self.dataset.text_column
            if self.dataset.text_column
            else self.dataset.df.columns.tolist()
        )

        percentage_colummn_assign = {
            "Percentage of Rows (%)": lambda x: x["Number of Duplicates"] / rows * 100
        }

        duplicate_results = (
            duplicate_rows.groupby(duplicate_rows_group_by)
            .size()
            .reset_index(name="Number of Duplicates")
            .sort_values(by=["Number of Duplicates"], ascending=False)
            .assign(**percentage_colummn_assign)
        )

        # test has passed if the total sum of duplicates is less than the threshold
        n_duplicates = duplicate_results["Number of Duplicates"].sum()
        passed = n_duplicates < self.params["min_threshold"]

        results = [
            ThresholdTestResult(
                passed=passed,
                values=duplicate_results.to_dict(orient="records"),
            )
        ]

        # Additionally, run duplicates test on fields that are primary keys
        primary_keys = []
        for field in self.dataset.fields:
            if field.get("type_options", None) and field.get("type_options").get(
                "primary_key", False
            ):
                primary_keys.append(field["id"])

        for col in primary_keys:
            col_n_duplicates = len(
                self.dataset.df[self.dataset.df[col].duplicated(keep=False)]
            )
            col_p_duplicates = col_n_duplicates / rows
            col_passed = col_n_duplicates < self.params["min_threshold"]
            results.append(
                ThresholdTestResult(
                    column=col,
                    passed=col_passed,
                    values={
                        "n_duplicates": col_n_duplicates,
                        "p_duplicates": col_p_duplicates,
                    },
                )
            )

        return self.cache_results(results, passed=all([r.passed for r in results]))
