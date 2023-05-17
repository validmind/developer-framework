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
from ..utils import clean_docstring


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
    name: ClassVar[str] = ""  # unique identifer for metric: "accuracy"
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
    def key(self):
        """
        Keep the key for compatibility reasons
        """
        return self.name

    def description(self):
        """
        Return the metric description. Should be overridden by subclasses. Defaults
        to returning the class' docstring
        """
        return self.__doc__.strip()

    def summary(self, metric_value: Optional[Union[dict, list, pd.DataFrame]] = None):
        """
        Return the metric summary. Should be overridden by subclasses. Defaults to None.
        The metric summary allows renderers (e.g. Word and ValidMind UI) to display a
        short summary of the metric results.

        We return None here because the metric summary is optional.
        """
        return None

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
        if metric_value is None and figures is None:
            raise ValueError(
                "Metric must provide a metric value or figures to cache_results"
            )

        # At a minimum, send the metric description
        result_metadata = [
            {
                "content_id": f"metric_description:{self.name}",
                "text": clean_docstring(self.description()),
            }
        ]

        result_summary = self.summary(metric_value)

        test_plan_result = TestPlanMetricResult(
            result_id=self.name,
            result_metadata=result_metadata,
        )

        # We can send an empty result to push an empty metric with a summary and plots
        metric_result_value = metric_value if metric_value is not None else {}

        test_plan_result.metric = MetricResult(
            type=self.type,
            scope=self.scope,
            key=self.key,
            value=metric_result_value,
            value_formatter=self.value_formatter,
            summary=result_summary,
        )

        # Allow metrics to attach figures to the test plan result
        if figures:
            test_plan_result.figures = figures

        self.result = test_plan_result

        return self.result
