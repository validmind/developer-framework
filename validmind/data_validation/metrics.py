"""
Metrics functions for any Pandas-compatible datasets
"""

from dataclasses import dataclass
from typing import ClassVar


from ..vm_models import Metric, TestContext, TestContextUtils, TestPlanResult


@dataclass
class DatasetMetadata(TestContextUtils):
    """
    Custom class to collect a set of descriptive statistics for a dataset.
    This class will log dataset metadata via `log_dataset` instead of a metric.
    Dataset metadat is necessary to initialize dataset object that can be related
    to different metrics and test results
    """

    test_type: ClassVar[str] = "DatasetMetadata"

    # Test Context
    test_context: TestContext

    name = "dataset_metadata"
    result: TestPlanResult = None

    def run(self):
        """
        Just set the dataset to the result attribute of the test plan result
        and it will be logged via the `log_dataset` function
        """
        self.result = TestPlanResult(dataset=self.dataset)

        return self.result


@dataclass
class DatasetDescription(Metric):
    """
    Collects a set of descriptive statistics for a dataset
    """

    type = "dataset"
    key = "dataset_description"

    def __post_init__(self):
        self.scope = self.dataset.type

    def run(self):
        # This will populate the "fields" attribute in the dataset object
        self.dataset.describe()
        return self.cache_results(self.dataset.fields)
