"""__TEST_NAME__ Threshold Test"""

from dataclasses import dataclass
from typing import List

from validmind.logging import get_logger
from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTestResult,
    ThresholdTest,
)

logger = get_logger(__name__)


@dataclass
class __TEST_NAME__(ThresholdTest):
    """
    Test that the model's prediction accuracy on a dataset meets or
    exceeds a predefined threshold.
    """

    name = "__TEST_ID__"
    required_inputs = []  # model, dataset, etc.
    default_params = {}
    tasks = [],  # classification, regression, etc. Should be one of ValidMind's task types
        "tags": [],  # time_series_data, tabular_data, forcasting, etc. Can be any string
    }

    def run(self):
        """Run the test and cache the results

        Returns:
            ThresholdTestResultWrapper: The results of the test.
        """
        table_with_numbers = {
            "A": [1, 2, 3, 4, 5],
            "B": [6, 7, 8, 9, 10],
        }

        return self.cache_results(
            test_results_list=[
                ThresholdTestResult(
                    passed=True,  # whether this test passed
                    values=table_with_numbers,
                )
            ],
            passed=True,  # whether all tests passed
            figures=None,  # return a figure by importing from validmind.vm_models
        )

    def summary(
        self, results: List[ThresholdTestResult], all_passed: bool
    ) -> ResultSummary:
        """Summarize the results of the test.

        Args:
            results (List[ThresholdTestResult]): The results of the test.
            all_passed (bool): Whether all tests passed.

        Returns:
            ResultSummary: A summary of the test results.
        """
        return ResultSummary(
            results=[
                ResultTable(
                    data=results,
                    metadata=ResultTableMetadata(
                        title="__TEST_NAME__ Test Results",
                    ),
                )
            ]
        )
