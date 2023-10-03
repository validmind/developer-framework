# Copyright © 2023 ValidMind Inc. All rights reserved.
from dataclasses import dataclass

from ...errors import should_raise_on_fail_fast
from ...logging import get_logger, log_performance
from ...tests import LoadTestError, load_test
from ...utils import test_id_to_name
from ..test.test import Test
from ..test_context import TestContext
from .result import TestSuiteFailedResult, TestSuiteResult

logger = get_logger(__name__)


@dataclass
class TestSuiteTest:
    """
    Wraps a 'Test' in a Test Suite and handles logic and state for that test
    """

    test_id: str

    _test_class: Test = None
    _test_instance: Test = None

    result: object = None

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
        return test_id_to_name(self.test_id)

    @property
    def name(self):
        return self._test_class.name

    @property
    def test_type(self):
        return self._test_class.test_type

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
                params=test_config,
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
