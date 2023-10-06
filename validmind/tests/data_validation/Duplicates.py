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
    **Purpose**: The Duplicates test aims to evaluate the quality of data in an ML model by identifying duplicate
    entries in the dataset. It specifically targets duplication in a designated text column or among the primary keys
    of the dataset, which can have significant implications for model performance and integrity. Duplicate entries can
    potentially distort data distribution and skew model training.

    **Test Mechanism**: The test works by counting the total number of duplicate entries within the dataset. If a
    'text_column' property is specified, the algorithm will count duplicates within this column. If any primary key is
    declared, the test will be run on the primary keys as well. The number of duplicates ('n_duplicates') is then
    compared to a predefined minimum threshold (default 'min_threshold' is set to 1) to determine if the test has
    passed. Results include total number of duplicates, and the percentage of duplicate rows in the overall dataset
    ('p_duplicates').

    **Signs of High Risk**: The existence of a significant number of duplicates, especially exceeding the minimum
    threshold, indicates high risk. Potential issues include an overrepresentation of certain data (thus skewing
    results), or the indication of inefficient data collecting methods leading to data redundancy. Models that
    predominantly fail this test may need to have their data preprocessing methods or source data reviewed.

    **Strengths**: The Duplicates test is versatile and can be applied to both text data and tabular data formats. It
    also provides results calculated both as a count and as a percentage of the total dataset, facilitating a
    comprehensive understanding of the extent of duplication. This metric can effectively flag data quality issues that
    can skew your model performance and lead to inaccurate predictions.

    **Limitations**: The Duplicates test only targets exact duplication in entries, which might overlook close
    'almost-duplicate' entries, or normalized forms of entries, that may also impact data distribution and model
    integrity. Data variations due to errors, slight changes in phrasing, or other inconsistencies may not be detected.
    Furthermore, a high number of duplicates in a dataset may not always indicate poor data quality, depending on the
    nature of data and the problem being addressed.
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
