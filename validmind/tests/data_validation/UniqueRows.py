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
class UniqueRows(ThresholdTest):
    """
    **Purpose**:
    The purpose of the UniqueRows test is to assess the quality of the data that is being fed into the ML model,
    specifically by checking that the number of unique rows in the dataset exceeds a certain threshold in order to
    ensure diversity in the data. This is important as having a diverse range of data is crucial in training an
    unbiased and robust model that performs well on unseen data.

    **Test Mechanism**:
    The testing mechanism first calculates the total number of rows in the dataset. Then, for each column in the
    dataset, the number of unique rows is counted. The test passes if the percentage of unique rows (calculated as the
    number of unique rows divided by the total number of rows) is less than the predefined minimum percent threshold
    provided as a parameter to the function. The results are then cached, and an overall pass or fail is issued based
    on whether all columns have passed the test.

    **Signs of High Risk**:
    Signs of high risk include columns of data where the number of unique rows is less than the predefined minimum
    percent threshold. This lack of diversity in the data can be seen as an indicator of poor data quality, which could
    potentially lead to model overfitting and a poor generalization ability, thereby posing a high risk.

    **Strengths**:
    The Strengths of the UniqueRows test include its ability to quickly and efficiently evaluate the diversity of data
    across each column in the dataset. It allows an easy and systematic way to check data quality in terms of
    uniqueness, which can be a critical aspect in creating an effective and unbiased ML model.

    **Limitations**:
    One limitation of the UniqueRows test is that it assumes that the quality of the data is directly proportional to
    its uniqueness, which may not always be the case. There might be scenarios where certain non-unique rows are
    important and shouldn't be discounted. Also, it doesn’t take into account the 'importance' of each column in
    predicting the output and treats all columns equally. Finally, this test will not be useful or appropriate for
    categorical variables where the number of unique categories is naturally limited.
    """

    category = "data_quality"
    name = "unique"
    required_inputs = ["dataset"]
    default_params = {"min_percent_threshold": 1}

    metadata = {
        "task_types": ["regression", "classification"],
        "tags": ["tabular_data"],
    }

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
        rows = self.dataset.df.shape[0]

        unique_rows = self.dataset.df.nunique()
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
