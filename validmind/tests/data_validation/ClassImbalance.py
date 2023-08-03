# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

from validmind.logging import get_logger
from validmind.vm_models import (
    VMDataset,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
)

logger = get_logger(__name__)


@dataclass
class ClassImbalance(ThresholdTest):
    """
    The class imbalance test measures the disparity between the majority
    class and the minority class in the target column.
    """

    category = "data_quality"
    name = "class_imbalance"
    required_context = ["dataset"]
    default_params = {"min_percent_threshold": 0.2}

    def summary(self, results: List[TestResult], all_passed: bool):
        """
        The class imbalance test returns results like these:
        [{"values": {"0": 0.798, "1": 0.202}, "column": "Exited", "passed": true}]
        So we build a table with 2 rows, one for each class.
        """

        results_table = []
        result = results[0]
        for class_name, class_percent in result.values.items():
            results_table.append(
                {
                    "Class": f'{class_name} ({"Negative" if class_name == "0" or class_name == 0 else "Positive"})',
                    "Percentage of Rows (%)": class_percent * 100,
                }
            )

        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(
                        title=f"Class Imbalance Results for Column {self.dataset.target_column}"
                    ),
                )
            ]
        )

    def run(self):
        # Can only run this test if we have a Dataset object
        if not isinstance(self.dataset, VMDataset):
            raise ValueError("ClassImbalance requires a validmind Dataset object")

        if self.dataset.target_column is None:
            logger.info(
                "Skipping class_imbalance test because no target column is defined"
            )
            return

        target_column = self.dataset.target_column
        imbalance_percentages = self.dataset.df[target_column].value_counts(
            normalize=True
        )

        # Does the minority class represent more than our threshold?
        passed = imbalance_percentages.min() > self.params["min_percent_threshold"]
        results = [
            TestResult(
                column=target_column,
                passed=passed,
                values=imbalance_percentages.to_dict(),
            )
        ]

        return self.cache_results(results, passed=passed)
