"""
Class for storing ValidMind metric objects and associated
data for display and reporting purposes
"""
from dataclasses import dataclass
from typing import ClassVar, Optional, Union

import pandas as pd

from .metric_result import MetricResult
from .test_context import TestContext
from .test_plan_result import TestPlanResult


@dataclass
class Metric:
    """
    Metric objects track the schema supported by the ValidMind API
    """

    # Test Context
    test_context: TestContext

    # Class Variables
    test_type: ClassVar[str] = "Metric"
    type: ClassVar[str] = ""  # type of metric: "training", "evaluation", etc.
    scope: ClassVar[str] = ""  # scope of metric: "training_dataset"
    key: ClassVar[str] = ""  # unique identifer for metric: "accuracy"
    value_formatter: ClassVar[Optional[str]] = None  # "records" or "key_values"
    default_params: ClassVar[dict] = {}

    # Instance Variables
    params: dict = None
    result: MetricResult = None

    def __post_init__(self):
        """
        Set default params if not provided
        """
        if self.params is None:
            self.params = self.default_params

    @property
    def name(self):
        return self.key

    @property
    def dataset(self):
        return self.test_context.dataset

    @property
    def model(self):
        return self.test_context.model

    @property
    def train_ds(self):
        return self.test_context.train_ds

    @property
    def test_ds(self):
        return self.test_context.test_ds

    @property
    def y_train_predict(self):
        return self.test_context.y_train_predict

    @property
    def y_test_predict(self):
        return self.test_context.y_test_predict

    def class_predictions(self, y_predict):
        """
        Converts a set of probability predictions to class predictions
        """
        # TODO: parametrize at some point
        return (y_predict > 0.5).astype(int)

    def run(self, *args, **kwargs):
        """
        Run the metric calculation and cache its results
        """
        raise NotImplementedError

    def cache_results(self, metric_value: Union[dict, list, pd.DataFrame]):
        """
        Cache the results of the metric calculation and do any post-processing if needed
        """
        self.result = TestPlanResult(
            metric=MetricResult(
                type=self.type,
                scope=self.scope,
                key=self.key,
                value=metric_value,
                value_formatter=self.value_formatter,
            )
        )

        return self.result
