# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
)


@dataclass
class Duplicates(ThresholdTest):
    """
    The duplicates test measures the number of duplicate entries found in the dataset.
    - If the dataset has a `text_column` property then the test will check for duplicate entries in that column.
    - If a primary key column is specified, the dataset is checked for duplicate primary keys as well.
    """

    category = "data_quality"
    name = "duplicates"
    required_inputs = ["dataset"]
    default_params = {"min_threshold": 1}

    def summary(self, results: List[TestResult], all_passed: bool):
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
            TestResult(
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
                TestResult(
                    column=col,
                    passed=col_passed,
                    values={
                        "n_duplicates": col_n_duplicates,
                        "p_duplicates": col_p_duplicates,
                    },
                )
            )

        return self.cache_results(results, passed=all([r.passed for r in results]))
