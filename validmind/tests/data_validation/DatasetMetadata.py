# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import ClassVar

from validmind.vm_models import TestContext, TestContextUtils, TestPlanDatasetResult


@dataclass
class DatasetMetadata(TestContextUtils):
    """
    Custom class to collect a set of descriptive statistics for a dataset.
    This class will log dataset metadata via `log_dataset` instead of a metric.
    Dataset metadata is necessary to initialize dataset object that can be related
    to different metrics and test results
    """

    # Test Context
    test_context: TestContext

    # Class Variables
    test_type: ClassVar[str] = "DatasetMetadata"
    required_context: ClassVar[list] = []
    default_params: ClassVar[dict] = {}

    # Instance Variables
    name = "dataset_metadata"
    params: dict = None
    result: TestPlanDatasetResult = None

    def __post_init__(self):
        """
        Set default params if not provided
        """
        if self.params is None:
            self.params = self.default_params

    def run(self):
        """
        Just set the dataset to the result attribute of the test plan result
        and it will be logged via the `log_dataset` function
        """
        self.result = TestPlanDatasetResult(
            result_id="dataset_metadata", dataset=self.dataset
        )

        return self.result
