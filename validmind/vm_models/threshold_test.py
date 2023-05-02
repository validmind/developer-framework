"""
(Threshold)Test class wrapper. Our API exposes the concept of of a
Test (as test_results) but we'll refer to it as a ThresholdTest to
avoid confusion with the "tests" in the general data science/modeling sense.

TODO: Test definitions should be supported in the API too
"""

from dataclasses import dataclass
from typing import ClassVar, List, Optional

from .figure import Figure
from .test_context import TestContext, TestContextUtils
from .test_plan_result import TestPlanTestResult
from .test_result import TestResult, TestResults


@dataclass
class ThresholdTest(TestContextUtils):
    """
    A threshold test is a combination of a metric/plot we track and a
    corresponding set of parameters and thresholds values that allow
    us to determine whether the metric/plot passes or fails.

    TODO: ThresholdTest should validate required context too
    """

    # Test Context
    test_context: TestContext

    # Class Variables
    test_type: ClassVar[str] = "ThresholdTest"
    category: ClassVar[str] = ""
    name: ClassVar[str] = ""
    default_params: ClassVar[dict] = {}

    # Instance Variables
    params: dict = None
    test_results: TestResults = None

    def __post_init__(self):
        """
        Set default params if not provided
        """
        if self.params is None:
            self.params = self.default_params
        else:
            self.params = {**self.default_params, **self.params}

    def run(self, *args, **kwargs):
        """
        Run the test and cache its results
        """
        raise NotImplementedError

    def cache_results(
        self,
        results: List[TestResult],
        passed: bool,
        figures: Optional[List[Figure]] = None,
    ):
        """
        Cache the individual results of the threshold test as a list of TestResult objects

        Args:
            results (List[TestResult]): The results of the threshold test
            passed (bool): Whether the threshold test passed or failed

        Returns:
            TestPlanResult: The test plan result object
        """
        self.test_results = TestPlanTestResult(
            result_id=self.name,
            test_results=TestResults(
                category=self.category,
                test_name=self.name,
                params=self.params,
                passed=passed,
                results=results,
            ),
        )

        # Allow test results to attach figures to the test plan result
        if figures:
            self.test_results.figures = figures

        return self.test_results
