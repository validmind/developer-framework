"""__TEST_NAME__ Metric"""

from dataclasses import dataclass

from validmind.logging import get_logger
from validmind.vm_models import (
    Figure,
    Metric,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)

logger = get_logger(__name__)


@dataclass
class __TEST_NAME__(Metric):
    """
    Test Description goes here.
    """

    name = "__TEST_ID__"
    required_inputs = []  # model, dataset, etc.
    default_params = {}
    metadata = {
        "task_types": [],  # classification, regression, etc. Should be one of ValidMind's task types
        "tags": [],  # time_series_data, tabular_data, forecasting, etc. Can be any string
    }

    def run(self):
        """Run the test and cache the results

        Returns:
            MetricResultWrapper: The results of the test.
        """
        figure = None  # you can use plotly to create a figure here

        table_with_numbers = {
            "A": [1, 2, 3, 4, 5],
            "B": [6, 7, 8, 9, 10],
        }

        return self.cache_results(
            metric_value=table_with_numbers,
            # figures=[
            #     Figure(
            #         for_object=self,
            #         key=self.name,
            #         figure=figure,
            #         metadata={},  # add metadata to the figure
            #     )
            # ],  # return a figure by importing from validmind.vm_models
        )

    def summary(self, metric_value) -> ResultSummary:
        """Summarize the results of the test.

        Args:
            metric_value (Union[dict, list, pd.DataFrame]): The cached results of the test.

        Returns:
            ResultSummary: The summarized results.
        """
        return ResultSummary(
            results=[
                ResultTable(
                    data=metric_value,
                    metadata=ResultTableMetadata(title="__TEST_NAME__ Results"),
                ),
            ]
        )
