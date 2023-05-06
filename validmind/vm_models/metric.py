"""
Class for storing ValidMind metric objects and associated
data for display and reporting purposes
"""
from dataclasses import dataclass
from typing import ClassVar, List, Optional, Union

import pandas as pd

from .figure import Figure
from .metric_result import MetricResult
from .test_context import TestContext, TestContextUtils
from .test_plan_result import TestPlanMetricResult


@dataclass
class Metric(TestContextUtils):
    """
    Metric objects track the schema supported by the ValidMind API

    TODO: Metric should validate required context too
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
    result: TestPlanMetricResult = None

    def __post_init__(self):
        """
        Set default params if not provided
        """
        if self.params is None:
            self.params = self.default_params

    @property
    def name(self):
        return self.key

    def description(self):
        """
        Return the metric description. Should be overridden by subclasses. Defaults
        to returning the class' docstring
        """
        return self.__doc__.strip()

    def run(self, *args, **kwargs):
        """
        Run the metric calculation and cache its results
        """
        raise NotImplementedError

    def cache_results(
        self,
        metric_value: Optional[Union[dict, list, pd.DataFrame]] = None,
        figures: Optional[List[Figure]] = None,
    ):
        """
        Cache the results of the metric calculation and do any post-processing if needed

        Args:
            metric_value (Union[dict, list, pd.DataFrame]): The value of the metric
            figures (Optional[object]): Any figures to attach to the test plan result

        Returns:
            TestPlanResult: The test plan result object
        """
        # At a minimum, send the metric description
        result_metadata = [
            {
                "content_id": f"metric_description:{self.name}",
                "text": self.description(),
            }
        ]

        test_plan_result = TestPlanMetricResult(
            result_id=self.name,
            result_metadata=result_metadata,
        )

        if metric_value is not None:
            test_plan_result.metric = MetricResult(
                type=self.type,
                scope=self.scope,
                key=self.key,
                value=metric_value,
                value_formatter=self.value_formatter,
            )

        # Allow metrics to attach figures to the test plan result
        if figures:
            test_plan_result.figures = figures

        self.result = test_plan_result

        return self.result
