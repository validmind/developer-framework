# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
A TestSuite is a collection of TestPlans. It is a helpful way to organize
TestPlans that are related to each other. For example, a TestSuite could be
created for a specific use case or model methodology, to run a colllection
of plans for data validation and model validation with a single function call.
"""

from dataclasses import dataclass
from typing import ClassVar, List, Optional, Union

import ipywidgets as widgets

from ..dataset import VMDataset
from ..model import VMModel
from ..result.test_suite_result import TestPlanFailedResult, TestPlanResult
from ..test.test import Test
from ..test_context import TestContext
from ...tests import load_test
from ...errors import MissingRequiredTestContextError, should_raise_on_fail_fast
from ...logging import get_logger, log_performance
from ...tests import LoadTestError, load_test
from ...utils import clean_docstring, is_notebook, run_async, run_async_check

logger = get_logger(__name__)

TOP_LEVEL_SECTION_KEY = "__top_level__"


def name_to_key(name: str) -> str:
    """
    Converts a name to a key
    """
    return name.lower().replace(" ", "_")


@dataclass
class TestSuiteTest:
    """
    Wraps a 'Test' in a Test Suite and handles logic and state for that test
    """

    test_id: str
    _test_class: Test
    _test_instance: Test
    _result: object

    def __post_init__(self):
        """Load the test class from the test id"""
        try:
            self._test_class = load_test(self.test_id)
        except LoadTestError as e:
            self._result = TestPlanFailedResult(
                error=e,
                message=f"Failed to load test '{self.test_id}'",
                result_id=self.test_id,
            )
        except Exception as e:
            logger.error(f"Failed to load test '{self.test_id}': {e}")
            raise e

    def load(self, test_context: TestContext, test_config: dict = None):
        """Load an instance of the test class"""
        if not self._test_class:
            return

        try:
            self._test_instance = self._test_class(
                test_context=test_context,
                test_config=test_config,
            )
        except Exception as e:
            self._result = TestPlanFailedResult(
                error=e,
                message=f"Failed to load test '{self.test_id}'",
                result_id=self.test_id,
            )

    def run(self, fail_fast: bool = False):
        """Run the test"""
        if not self._test_class:
            return

        try:
            self._test_instance.validate_context()

            # run the test and log the performance if LOG_LEVEL is set to DEBUG
            log_performance(
                func=self._test_instance.run,
                name=self._test_instance.name,
                logger=logger,
            )()  # this is a decorator so we need to call it

        except Exception as e:
            if fail_fast and should_raise_on_fail_fast(e):
                raise e # Re-raise the exception if we are in fail fast mode

            logger.error(
                f"Failed to run test '{self._test_instance.name}': "\
                f"({e.__class__.__name__}) {e}"
            )
            self._result = TestPlanFailedResult(
                name=f"Failed {self._test_instance.test_type}",
                error=e,
                message=f"Failed to run '{self._test_instance.name}'",
                result_id=self._test_instance.name,
            )

            return

        if self._test_instance.result is None:
            self._result = TestPlanFailedResult(
                name=f"Failed {self._test_instance.test_type}",
                error=None,
                message=f"'{self._test_instance.name}' did not return a result",
                result_id=self._test_instance.name,
            )

            return

        if not isinstance(self._test_instance.result, TestPlanResult):
            self._result = TestPlanFailedResult(
                name=f"Failed {self._test_instance.test_type}",
                error=None,
                message=f"'{self._test_instance.name}' returned an invalid result: "\
                        f"{self._test_instance.result}",
                result_id=self._test_instance.name,
            )

            return

        self._result = self._test_instance.result

    def log(self):
        """Log the result for this test to ValidMind"""
        if not self._result:
            raise ValueError("Cannot log test result before running the test")

        self._result.log()

@dataclass
class TestSuiteSection:
    """
    Represents a section in a test suite
    """

    key: str
    name: Optional[str] = None
    description: Optional[str] = None
    tests: List[TestSuiteTest]


@dataclass
class TestSuiteConfig:
    """
    Represents the config which holds test parameters for tests in a suite
    """

    params: dict

    _global_params: dict
    _section_params: dict
    _test_params: dict

    def __post_init():
        """
        Post init hook
        """
        self._global_params = {}
        self._section_params = {}
        self._test_params = {}

        self._build_params()

    def _build_params(self):
        """
        Builds the params for the test suite
        """
        for key, value in self.params.items():
            if isinstance(value, dict):
                if key in


@dataclass
class TestSuite:
    """
    Base class for test suites. Test suites are used to define a grouping of tests that
    can be run as a suite against datasets and models. Test Suites can be defined by
    inheriting from this base class and defining the list of tests as a class variable.

    Tests can be a flat list of strings or may be nested into sections by using a dict
    """

    tests: ClassVar[List[Union[str, dict]]]

    sections: List[TestSuiteSection] = None

    test_context: TestContext = None
    config: TestSuiteConfig = None

    def __post_init__(self):
        """
        Post init hook (runs after dataclass init)
        """
        self.sections = []

        self._build_sections()

    def _build_sections(self):
        """
        Builds the sections for the test suite
        """
        if not self.tests:
            raise ValueError("No tests found in test suite")

        test_ids = []
        section_dicts = []
        for item in self.tests:
            if isinstance(item, str):
                test_ids.append(item)
            elif isinstance(item, dict):
                section_dicts.append(item)
            else:
                raise ValueError(f"Invalid test suite item: {item}")

        # create top-level section to hold tests that are not in a section
        top_level_section = TestSuiteSection(
            key=TOP_LEVEL_SECTION_KEY,
            tests=[TestSuiteTest(test_id) for test_id in test_ids],
        )
        self.sections.append(top_level_section)

        # create rest of the sections (if any)
        for section_dict in section_dicts:
            self.sections.append(
                TestSuiteSection(
                    key=name_to_key(section_dict["section_name"]),
                    name=section_dict["section_name"],
                    description=section_dict.get("section_description", ""),
                    tests=[
                        TestSuiteTest(test_id)
                        for test_id in section_dict["section_tests"]
                    ],
                )
            )


class TestSuiteLoader:
    """
    Loads a test suite by instantiating the test classes with the test context and
    config
    """

    def __init__(self, test_suite: TestSuite):
        self.test_suite = test_suite

    def load(self):
        """
        Loads the tests in a test suite
        """
        for section in self.test_suite.sections:
            for test in section.section_tests:
                test.load()


class TestSuiteRunner:
    """
    Runs a test suite
    """

    pbar: widgets.IntProgress = None
    pbar_description: widgets.Label = None
    pbar_box: widgets.HBox = None

    def __init__(self, test_suite: TestSuite):
        self.test_suite = test_suite

    def run(self):
        """
        Runs the test suite
        """
        for section in self.test_suite.sections:
            for test in section.section_tests:
                test.run()

    def log(self):
        """
        Logs the results of the last test suite run to ValidMind
        """
        pass


class TestSuiteViewer:
    """
    Shows the results of a test suite
    """

    def __init__(self, test_suite: TestSuite):
        self.test_suite = test_suite

    def view(self):
        """
        Views the results of the last test suite run
        """
        pass
