# Copyright © 2023 ValidMind Inc. All rights reserved.
import asyncio

import ipywidgets as widgets
from IPython.display import display

from ...logging import get_logger
from ...utils import is_notebook, run_async, run_async_check
from ..test_context import TestContext
from .summary import TestSuiteSummary
from .test_suite import TestSuite

logger = get_logger(__name__)


class TestSuiteRunner:
    """
    Runs a test suite
    """

    suite: TestSuite = None
    context: TestContext = None
    config: dict = None

    _global_config: dict = None
    _test_configs: dict = None

    pbar: widgets.IntProgress = None
    pbar_description: widgets.Label = None
    pbar_box: widgets.HBox = None

    def __init__(self, suite: TestSuite, context: TestContext, config: dict = None):
        self.suite = suite
        self.context = context
        self.config = config or {}

        self._split_configs()
        self._init_tests()

    def _split_configs(self):
        """Splits the config into a global config and test configs"""
        self._global_config = {}
        self._test_configs = {}

        for key, value in self.config.items():
            test_ids = [test.test_id for test in self.suite.get_tests()]

            if key in test_ids:
                self._test_configs[key] = value
            else:
                self._global_config[key] = value

    def _init_tests(self):
        """
        Loads the tests in a test suite
        """
        for section in self.suite.sections:
            for test in section.tests:
                test.load(
                    test_context=self.context,
                    test_config={
                        **self._global_config,
                        **self._test_configs.get(test.test_id, {}),
                    },
                )

    def _start_progress_bar(self, send: bool = True):
        """
        Initializes the progress bar elements
        """
        # TODO: make this work for when user runs only a section of the test suite
        # if we are sending then there is a task for each test and logging its result
        num_tasks = self.suite.num_tests() * 2 if send else self.suite.num_tests()

        self.pbar_description = widgets.Label(value="Running test suite...")
        self.pbar = widgets.IntProgress(max=num_tasks, orientation="horizontal")
        self.pbar_box = widgets.HBox([self.pbar_description, self.pbar])

        display(self.pbar_box)

    def _stop_progress_bar(self):
        self.pbar_description.value = "Test suite complete!"

    async def log_results(self):
        """Logs the results of the test suite to ValidMind

        This method will be called after the test suite has been run and all results have been
        collected. This method will log the results to ValidMind.
        """
        self.pbar_description.value = (
            f"Sending results of test suite '{self.suite.suite_id}' to ValidMind..."
        )

        tests = [test for section in self.suite.sections for test in section.tests]
        # TODO: use asyncio.gather here for better performance
        for test in tests:
            self.pbar_description.value = (
                f"Sending result to ValidMind: {test.test_id}..."
            )

            try:
                await test.log()
            except Exception as e:
                self.pbar_description.value = "Failed to send result to ValidMind"
                logger.error(f"Failed to log result: {test.result}")

                raise e

            self.pbar.value += 1

    async def _check_progress(self):
        done = False

        while not done:
            if self.pbar.value == self.pbar.max:
                self.pbar_description.value = "Test suite complete!"
                done = True

            await asyncio.sleep(0.5)

    def summarize(self):
        if not is_notebook():
            return logger.info("Test suite done...")

        summary = TestSuiteSummary(
            title=self.suite.title,
            description=self.suite.description,
            sections=self.suite.sections,
        )
        summary.display()

    def run(self, send: bool = True, fail_fast: bool = False):
        """Runs the test suite, renders the summary and sends the results to ValidMind

        Args:
            send (bool, optional): Whether to send the results to ValidMind.
                Defaults to True.
            fail_fast (bool, optional): Whether to stop running tests after the first
                failure. Defaults to False.
        """
        self._start_progress_bar(send=send)

        for section in self.suite.sections:
            for test in section.tests:
                self.pbar_description.value = f"Running {test.test_type}: {test.name}"
                test.run(fail_fast=fail_fast)
                self.pbar.value += 1

        if send:
            run_async(self.log_results)
            run_async_check(self._check_progress)

        self.summarize()

        self._stop_progress_bar()
