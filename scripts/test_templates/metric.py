"""__TEST_NAME__ Metric"""

from dataclasses import dataclass

from validmind.logging import get_logger
from validmind.vm_models import (
    Metric,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestPlanMetricResult,
)

logger = get_logger(__name__)


@dataclass
class __TEST_NAME__(Metric):
    """
    Automatically detects the AR order of a time series using both BIC and AIC.
    """

    name = "__TEST_ID__"
    required_context = []
    default_params = {}

    def run(self) -> TestPlanMetricResult:
        """Run the test and cache the results

        Returns:
            TestPlanMetricResult: The results of the test.
        """
        return self.cache_results(
            metric_value={
                "hello": "world",
            },
            figures=None,  # return a figure by importing from validmind.vm_models
        )

    def summary(self, cached_results: TestPlanMetricResult) -> ResultSummary:
        """Summarize the results of the test.

        Args:
            cached_results (TestPalnMetricResult): The cached results of the test.

        Returns:
            ResultSummary: The summarized results.
        """
        return ResultSummary(
            results=[
                ResultTable(
                    data=cached_results["hello"],
                    metadata=ResultTableMetadata(title="__TEST_NAME__ Results"),
                ),
            ]
        )