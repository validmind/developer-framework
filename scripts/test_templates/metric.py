"""__TEST_NAME__ Metric"""

from dataclasses import dataclass

from validmind.logging import get_logger
from validmind.vm_models import (
    Metric,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestSuiteMetricResult,
)

logger = get_logger(__name__)


@dataclass
class __TEST_NAME__(Metric):
    """
    Automatically detects the AR order of a time series using both BIC and AIC.
    """

    name = "__TEST_ID__"
    required_inputs = []  # model, dataset, etc. (model.train_ds, model.test_ds)
    default_params = {}
    metadata = {
        "task_types": [],  # classification, regression, etc. Should be one of ValidMind's task types
        "tags": [],  # time_series_data, tabular_data, forecasting, etc. Can be any string
    }

    def run(self) -> TestSuiteMetricResult:
        """Run the test and cache the results

        Returns:
            TestSuiteMetricResult: The results of the test.
        """
        figure = None  # you can use plotly to create a figure here

        return self.cache_results(
            metric_value={
                "hello": "world",
            },
            figures=[
                Figure(
                    for_object=self,
                    key="__test_id__",
                    figure=figure,
                    metadata={},  # add metadata to the figure
                )
            ],  # return a figure by importing from validmind.vm_models
        )

    def summary(self, cached_results: TestSuiteMetricResult) -> ResultSummary:
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
