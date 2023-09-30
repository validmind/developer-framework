# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
A TestSuite is a collection of TestPlans. It is a helpful way to organize
TestPlans that are related to each other. For example, a TestSuite could be
created for a specific use case or model methodology, to run a colllection
of plans for data validation and model validation with a single function call.
"""

from dataclasses import dataclass
from typing import ClassVar, List, Optional, Union

from ...errors import should_raise_on_fail_fast
from ...logging import get_logger, log_performance
from ...tests import LoadTestError, load_test
from ..test.test import Test
from ..test_context import TestContext
from .result import TestSuiteFailedResult, TestSuiteResult

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

    result: object

    def __post_init__(self):
        """Load the test class from the test id"""
        try:
            self._test_class = load_test(self.test_id)
        except LoadTestError as e:
            self.result = TestSuiteFailedResult(
                error=e,
                message=f"Failed to load test '{self.test_id}'",
                result_id=self.test_id,
            )
        except Exception as e:
            logger.error(f"Failed to load test '{self.test_id}': {e}")
            raise e

    @property
    def title(self):
        return self.test_id.split(".")[-1].title().replace("_", " ")

    def get_default_params(self):
        """Returns the default params for the test"""
        if not self._test_class:
            return {}

        return self._test_class.default_params

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
            self.result = TestSuiteFailedResult(
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
                raise e  # Re-raise the exception if we are in fail fast mode

            logger.error(
                f"Failed to run test '{self._test_instance.name}': "
                f"({e.__class__.__name__}) {e}"
            )
            self.result = TestSuiteFailedResult(
                name=f"Failed {self._test_instance.test_type}",
                error=e,
                message=f"Failed to run '{self._test_instance.name}'",
                result_id=self._test_instance.name,
            )

            return

        if self._test_instance.result is None:
            self.result = TestSuiteFailedResult(
                name=f"Failed {self._test_instance.test_type}",
                error=None,
                message=f"'{self._test_instance.name}' did not return a result",
                result_id=self._test_instance.name,
            )

            return

        if not isinstance(self._test_instance.result, TestSuiteResult):
            self.result = TestSuiteFailedResult(
                name=f"Failed {self._test_instance.test_type}",
                error=None,
                message=f"'{self._test_instance.name}' returned an invalid result: "
                f"{self._test_instance.result}",
                result_id=self._test_instance.name,
            )

            return

        self.result = self._test_instance.result

    async def log(self):
        """Log the result for this test to ValidMind"""
        if not self.result:
            raise ValueError("Cannot log test result before running the test")

        await self.result.log()


@dataclass
class TestSuiteSection:
    """
    Represents a section in a test suite
    """

    key: str
    name: Optional[str] = None
    description: Optional[str] = None
    tests: List[TestSuiteTest]

    def get_required_inputs(self) -> List[str]:
        """
        Returns the required inputs for the test plan. Defaults to the
        required inputs of the tests

        Returns:
            List[str]: A list of required inputs elements
        """
        required_inputs = set()

        # bubble up the required inputs from the tests
        for test in self.tests:
            if not hasattr(test, "required_inputs") or test.required_inputs is None:
                continue

            required_inputs.update(test.required_inputs)

        return list(required_inputs)

    def get_default_config(self):
        """Returns the default configuration for the test suite section"""
        section_default_config = {}

        for test in self.tests:
            section_default_config[test.id] = test.get_default_params()

        return section_default_config


@dataclass
class TestSuite:
    """
    Base class for test suites. Test suites are used to define a grouping of tests that
    can be run as a suite against datasets and models. Test Suites can be defined by
    inheriting from this base class and defining the list of tests as a class variable.

    Tests can be a flat list of strings or may be nested into sections by using a dict
    """

    name: ClassVar[str]
    tests: ClassVar[List[Union[str, dict]]]

    sections: List[TestSuiteSection] = None

    test_context: TestContext = None

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

    @property
    def description(self):
        return self.__doc__

    @property
    def title(self):
        return self.name.title().replace("_", " ")

    def num_tests(self) -> int:
        """
        Returns the total number of tests in the test suite
        """
        num_tests = 0

        for section in self.sections:
            num_tests += len(section.tests)

        return num_tests

    def get_required_inputs(self) -> List[str]:
        """
        Returns the required inputs for the test suite.
        """
        required_inputs = set()

        for test_plan in self._test_plan_instances:
            required_inputs.update(test_plan.get_required_inputs())

        return list(required_inputs)

    def get_default_config(self) -> dict:
        """Returns the default configuration for the test suite

        Each test in a test suite can accept parameters and those parameters can have
        default values. Both the parameters and their defaults are set in the test
        class and a config object can be passed to the test suite's run method to
        override the defaults. This function returns a dictionary containing the
        parameters and their default values for every test to allow users to view
        and set values

        Returns:
            dict: A dictionary of test names and their default parameters
        """
        default_config = {}

        for section in self.sections:
            default_config = {**default_config, **section.get_default_config()}

        return default_config
