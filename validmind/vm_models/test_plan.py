"""
TestPlan class
"""
import asyncio
from dataclasses import dataclass
from typing import ClassVar, List

import ipywidgets as widgets
from IPython.display import display

from ..logging import get_logger, log_performance
from ..utils import clean_docstring, is_notebook, run_async, run_async_check
from .dataset import Dataset
from .model import Model
from .test_context import TestContext
from .test_plan_result import TestPlanResult

logger = get_logger(__name__)


@dataclass
class TestPlan:
    """
    Base class for test plans. Test plans are used to define any
    arbitrary grouping of tests that will be run on a dataset or model.
    """

    # Class Variables
    name: ClassVar[str]
    required_context: ClassVar[List[str]]
    tests: ClassVar[List[object]] = []
    test_plans: ClassVar[List[object]] = []
    results: ClassVar[List[TestPlanResult]] = []

    # Instance Variables
    config: dict() = None
    _global_config: dict() = None
    _test_configs: dict() = None
    test_context: TestContext = None
    # Stores a reference to the child test plan instances
    _test_plan_instances: List[object] = None

    # Single dataset for dataset-only tests
    dataset: Dataset = None

    # Model and corresponding datasets for model related tests
    model: Model = None

    # Multiple models for model comparison tests
    models: List[Model] = None

    # ipywidgets progress bar
    pbar: widgets.IntProgress = None
    pbar_description: widgets.Label = None
    pbar_box: widgets.HBox = None

    # Stores the HTML summary of the test plan
    summary: str = None

    def __repr__(self):
        class_name = type(self).__name__

        if self.config is None:
            return f"{class_name}(test_context={self.test_context})"

        return f"{class_name}(test_context={self.test_context}, config={{...}})"

    def __post_init__(self):
        if self.test_context is not None:
            self.dataset = self.test_context.dataset
            self.model = self.test_context.model
            self.models = self.test_context.models

        self.validate_context()

        self._split_configs()

    def _split_configs(self):
        """Splits the config into a global config and test configs"""
        if self.config is None:
            return

        self._global_config = {}
        self._test_configs = {}

        test_names = [test.name for test in self.tests]

        for key, value in self.config.items():
            if key in test_names:
                self._test_configs[key] = value
            else:
                self._global_config[key] = value

    def title(self):
        """
        Returns the title of the test plan. Defaults to the title
        version of the test plan name
        """
        return self.name.title().replace("_", " ")

    def description(self):
        """
        Returns the description of the test plan. Defaults to the
        docstring of the test plan
        """
        return self.__doc__

    def validate_context(self):
        """
        Validates that the context elements are present
        in the instance so that the test plan can be run
        """
        for element in self.required_context:
            if not hasattr(self, element):
                raise ValueError(
                    f"Test plan '{self.name}' requires '{element}' to be present in the test context"
                )

            if getattr(self, element) is None:
                raise ValueError(
                    f"Test plan '{self.name}' requires '{element}' to be present in the test context"
                )

    def get_config_params_for_test(self, test_name):
        """
        Returns the config for a given test, if it exists. The `config`
        attribute is a dictionary where the keys are the test names and
        the values are dictionaries of config values for that test.

        The key in the config must match the name of the test, i.e. for
        a test called "time_series_univariate_inspection_raw" we could
        pass a config like this:

        {
            "time_series_univariate_inspection_raw": {
                "columns": ["col1", "col2"]
            }
        }
        """
        if self.config is None:
            return None

        return {
            **self._global_config,
            **self._test_configs.get(test_name, {}),
        }  # merges the global config with the test config

    def _init_pbar(self, render_summary: bool = True, send: bool = True):
        """
        Initializes the progress bar elements
        """
        self.pbar = widgets.IntProgress(
            value=0,
            min=0,
            max=len(self.tests) * 2 if send else len(self.results),  # tests and results
            step=1,
            bar_style="",
            orientation="horizontal",
        )
        self.pbar_description = widgets.Label(value="Running test plan...")
        # Display them in a horizontal box
        self.pbar_box = widgets.HBox([self.pbar_description, self.pbar])

        if render_summary:
            display(self.pbar_box)

    def run(  # noqa C901 'TestPlan.run' is too complex
        self, render_summary: bool = True, send: bool = True
    ):
        """
        Runs the test plan

        Args:
            render_summary: Defaults to True. Whether to render the summary of the test
                plan. When it's False, this allows test suites to collect the results of
                sub test plans and render them all at once with widgets
            send: Whether to send the results to the backend

        Returns:
            None
        """
        self.results = []  # Empty the results cache on every run

        if self.test_context is None:
            self.test_context = TestContext(
                dataset=self.dataset,
                model=self.model,
                models=self.models,
            )

        if self.pbar is None:
            self._init_pbar(render_summary=render_summary, send=send)

        for test in self.tests:
            test_instance = test(
                test_context=self.test_context,
                params=self.get_config_params_for_test(test.name),
            )

            self.pbar_description.value = f"Running {test.test_type}: {test.name}"

            # run the test and log the performance if LOG_LEVEL is set to DEBUG
            log_performance(
                test_instance.run,
                test_instance.name,
                logger=logger,
            )()

            if test_instance.result is None:
                self.pbar_description.value = "Test returned None, skipping..."
                self.pbar.value += 1
                continue

            if not isinstance(test_instance.result, TestPlanResult):
                raise ValueError(
                    f"'{test_instance.name}' must return an instance of TestPlanResult Base Class"
                )

            self.results.append(test_instance.result)
            self.pbar.value += 1

        if send:
            run_async(self.log_results)
            run_async_check(self._check_progress)

        # TODO: remove
        for test_plan in self.test_plans:
            test_plan_instance = test_plan(
                config=self.config,
                test_context=self.test_context,
                # pbar=self.pbar,
            )
            test_plan_instance.run(send=send)

            # Build up the subtest plan instances so we can log them
            if self._test_plan_instances is None:
                self._test_plan_instances = []

            self._test_plan_instances.append(test_plan_instance)

        self.summarize(render_summary)

    async def _check_progress(self):
        done = False
        while not done:
            if self.pbar.value == self.pbar.max:
                self.pbar_description.value = "Test plan complete!"
                done = True
            await asyncio.sleep(0.5)

    async def log_results(self):
        """Logs the results of the test plan to ValidMind

        This method will be called after the test plan has been run and all results have been
        collected. This method will log the results to ValidMind.
        """
        self.pbar_description.value = (
            f"Sending results of test plan '{self.name}' to ValidMind..."
        )

        for result in self.results:
            self.pbar_description.value = (
                f"Sending result to ValidMind: {result.result_id}..."
            )

            try:
                await result.log()
            except Exception as e:
                log = f"Failed to log result: {result} for test plan result '{str(result)}'"
                self.pbar_description.value = log
                logger.error(log)
                raise e

            self.pbar.value += 1

    def _results_title(self) -> str:
        """
        Builds the title for the results of the test plan
        """
        return f"<h2>Results for <i>{self.title()}</i> Test Plan:</h2><hr>"

    def _results_description(self) -> str:
        """
        Builds the description for the results of the test plan. Subclasses
        should override this method to provide an appropriate description
        """
        return f'<div class="result">{clean_docstring(self.description())}</div>'

    def _results_summary(self) -> str:
        """
        Builds a summary of the results for each of the tests in the test plan
        """
        accordions = {}
        id = 0
        for result in self.results:
            result_widget = result._to_widget()
            if result_widget:
                accordions[result.result_id] = {
                    "id": id,
                    "widget": result_widget,
                    "result": result,
                }
                id += 1

        return accordions

    def summarize(self, render_summary: bool = True):
        """Summarizes the results of the test plan

        This method will be called after the test plan has been run and all results have been
        logged to ValidMind. It will summarize the results of the test plan by creating an
        html table with the results of each test. This html table will be displayed in an
        VS Code, Jupyter or other notebook environment.
        """
        if render_summary and not is_notebook():
            logger.info("Cannot render summary outside of a notebook environment")
            return

        if len(self.results) == 0:
            return

        vbox_children = []

        # Only show the title if we are rendering the summary here
        if render_summary:
            vbox_children.append(widgets.HTML(value=self._results_title()))

        vbox_children.append(widgets.HTML(value=self._results_description()))

        accordion_contents = self._results_summary()
        accordion_items = [v["widget"] for v in accordion_contents.values()]
        accordion_widget = widgets.Accordion(children=accordion_items)

        for result_id, accordion_item in accordion_contents.items():
            result = accordion_item["result"]
            result_name = f"{result.name}: " if result.name else ""
            title = f'{result_name }{result_id.title().replace("_", " ")} ({result_id})'
            accordion_widget.set_title(accordion_item["id"], title)

        vbox_children.append(accordion_widget)

        style_footer = widgets.HTML(
            value="""
        <style>
            .result {
                margin: 10px 0;
                padding: 10px;
                background-color: #f1f1f1;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        </style>
        """
        )

        # Don't duplicate the footer if we are not rendering the summary here
        if render_summary:
            vbox_children.append(style_footer)

        self.summary = widgets.VBox(vbox_children)

        if render_summary:
            display(self.summary)

    def _get_all_subtest_plan_results(self) -> List[TestPlanResult]:
        """
        Recursively gets all sub test plan results since a test plan
        can have sub test plans which can have sub test plans and so on.
        """
        results = []
        sub_test_plans = self._test_plan_instances or []
        for test_plan in sub_test_plans:
            if test_plan.results is not None:
                results.extend(test_plan.results)

            results.extend(test_plan._get_all_subtest_plan_results())

        return results

    def get_results(self, result_id: str = None) -> List[TestPlanResult]:
        """
        Returns one or more results of the test plan. Includes results from
        sub test plans.
        """
        all_results = (self.results or []) + self._get_all_subtest_plan_results()
        if result_id is None:
            return all_results

        return [result for result in all_results if result.result_id == result_id]
