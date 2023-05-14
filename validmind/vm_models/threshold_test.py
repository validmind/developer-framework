"""
(Threshold)Test class wrapper. Our API exposes the concept of of a
Test (as test_results) but we'll refer to it as a ThresholdTest to
avoid confusion with the "tests" in the general data science/modeling sense.

TODO: Test definitions should be supported in the API too
"""

from dataclasses import dataclass
from typing import ClassVar, List, Optional

from .figure import Figure
from .result_summary import ResultSummary, ResultTable
from .test_context import TestContext, TestContextUtils
from .test_plan_result import TestPlanTestResult
from .test_result import TestResult, TestResults
from ..utils import clean_docstring


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
    result: TestResults = None

    def __post_init__(self):
        """
        Set default params if not provided
        """
        if self.params is None:
            self.params = self.default_params
        else:
            self.params = {**self.default_params, **self.params}

    def description(self):
        """
        Return the test description. Should be overridden by subclasses. Defaults
        to returning the class' docstring
        """
        return self.__doc__.strip()

    def summary(self, results: Optional[List[TestResult]], all_passed: bool):
        """
        Return the threshold test summary. Should be overridden by subclasses. Defaults to showing
        a table with test_name(optional), column and passed.

        The test summary allows renderers (e.g. Word and ValidMind UI) to display a
        short summary of the test results.
        """
        if results is None:
            return None

        results_table = []
        for test_result in results:
            result_object = {
                "passed": test_result.passed,
            }

            if test_result.test_name is not None:
                result_object["test_name"] = test_result.test_name
            if test_result.column is not None:
                result_object["column"] = test_result.column

            results_table.append(result_object)

        return ResultSummary(results=[ResultTable(data=results_table)])

    def run(self, *args, **kwargs):
        """
        Run the test and cache its results
        """
        raise NotImplementedError

    def cache_results(
        self,
        test_results_list: List[TestResult],
        passed: bool,
        figures: Optional[List[Figure]] = None,
    ):
        """
        Cache the individual results of the threshold test as a list of TestResult objects

        Args:
            result (List[TestResult]): The results of the threshold test
            passed (bool): Whether the threshold test passed or failed

        Returns:
            TestPlanResult: The test plan result object
        """
        # Rename to self.result
        # At a minimum, send the test description
        result_metadata = [
            {
                "content_id": f"test_description:{self.name}",
                "text": clean_docstring(self.description()),
            }
        ]

        result_summary = self.summary(test_results_list, passed)

        self.result = TestPlanTestResult(
            result_id=self.name,
            result_metadata=result_metadata,
            test_results=TestResults(
                category=self.category,
                test_name=self.name,
                params=self.params,
                passed=passed,
                results=test_results_list,
                summary=result_summary,
            ),
        )

        # Allow test results to attach figures to the test plan result
        if figures:
            self.result.figures = figures

        return self.result
