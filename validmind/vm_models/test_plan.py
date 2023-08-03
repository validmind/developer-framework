# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
TestPlan class
"""
import asyncio
from dataclasses import dataclass
from typing import ClassVar, List, Union

import ipywidgets as widgets
from IPython.display import display

from ..errors import MissingRequiredTestContextError
from ..logging import get_logger, log_performance
from ..tests import load_test, LoadTestError
from ..utils import clean_docstring, is_notebook, run_async, run_async_check
from .dataset import VMDataset
from .model import Model
from .test_context import TestContext, TestContextUtils
from .test_plan_result import TestPlanFailedResult, TestPlanResult

logger = get_logger(__name__)


@dataclass
class TestPlan:
    """
    Base class for test plans. Test plans are used to define any
    arbitrary grouping of tests that will be run on a dataset or model.
    """

    # Class Variables
    name: ClassVar[str]
    tests: ClassVar[Union[List[str], List[dict], List[TestContextUtils]]]
    results: ClassVar[List[TestPlanResult]]

    # Instance Variables
    config: dict() = None
    _global_config: dict() = None
    _test_configs: dict() = None
    test_context: TestContext = None

    # Reference to the test classes (dynamic import after initialization)
    _tests: List[object] = None

    # Single dataset for dataset-only tests
    dataset: VMDataset = None

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

        self._init_tests()
        self._split_configs()

    def _split_configs(self):
        """Splits the config into a global config and test configs"""
        if self.config is None:
            return

        self._global_config = {}
        self._test_configs = {}

        test_names = [test.name for test in self._tests]

        for key, value in self.config.items():
            if key in test_names:
                self._test_configs[key] = value
            else:
                self._global_config[key] = value

    def _load_test(self, test_id: str, test_class_props: dict = None):
        """Loads a test class from a test id and appends it to the list of tests"""
        try:
            test_class = load_test(test_id)

            if test_class_props:
                for key, val in test_class_props.items():
                    setattr(test_class, key, val)

            self._tests.append(test_class)

        except LoadTestError as e:
            self.results.append(
                TestPlanFailedResult(
                    error=e,
                    message=f"Failed to load test '{test_id}'",
                    result_id=test_id,
                )
            )

        except Exception as e:
            logger.error(f"Failed to load test '{test_id}': {e}")
            raise e

    def _init_tests(self):
        """Dynamically import the test classes based on the test names"""
        self.results = []
        self._tests = []

        for test_id_or_class in self.tests:
            # Check if test_id_or_class is a class and if it is a subclass of TestContextUtils
            if isinstance(test_id_or_class, type) and issubclass(
                test_id_or_class,
                TestContextUtils,  # TODO: use a dedicated base class for metric/test
            ):  # if its a test class, we just add it to the list
                test_id_or_class.id = test_id_or_class.name
                self._tests.append(test_id_or_class)
                continue

            test_class_props = None
            if isinstance(test_id_or_class, dict):
                # if its a dictionary, we pull the test_id out and then treat the rest
                # of the dictionary as the attributes to set on the test class
                # this is used to set a ref_id from the template
                test_class_props = {
                    key: val
                    for key, val in test_id_or_class.items()
                    if key != "test_id"
                }
                test_class_props["id"] = test_id_or_class["test_id"]
                test_id_or_class = test_id_or_class["test_id"]

            self._load_test(test_id_or_class, test_class_props)

    def get_required_context(self) -> List[str]:
        """
        Returns the required context for the test plan. Defaults to the
        required context of the tests

        Returns:
            List[str]: A list of required context elements
        """
        required_context = set()

        # bubble up the required context from the tests
        for test in self._tests:
            if not hasattr(test, "required_context"):
                continue
            required_context.update(test.required_context)

        return list(required_context)

    def get_default_config(self) -> dict:
        """Returns the default configuration for the test plan

        Each test in a test plan can accept parameters and those parameters can have
        default values. Both the parameters and their defaults are set in the test
        class and a config object can be passed to the test plan's run method to
        override the defaults. This function returns a dictionary containing the
        parameters and their default values for every test to allow users to view
        and set values

        Returns:
            dict: A dictionary of test names and their default parameters
        """
        default_config = {}

        for test in self._tests:
            default_config[test.id] = test.default_params

        return default_config

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

        def recursive_attr_check(obj, attr_chain):
            attrs = attr_chain.split(".")
            if not hasattr(obj, attrs[0]) or getattr(obj, attrs[0]) is None:
                return False
            return len(attrs) == 1 or recursive_attr_check(
                getattr(obj, attrs[0]),
                ".".join(attrs[1:]),
            )

        for element in self.get_required_context():
            logger.debug(f"Checking if required context '{element}' is present")
            if not recursive_attr_check(self, element):
                raise MissingRequiredTestContextError(
                    f"{element}' is required_context and must be passed "
                    "as a keyword argument to the test plan"
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
            max=len(self.tests) * 2 if send else len(self.results),  # tests + results
            step=1,
            bar_style="",
            orientation="horizontal",
        )
        self.pbar_description = widgets.Label(value="Running test plan...")
        # Display them in a horizontal box
        self.pbar_box = widgets.HBox([self.pbar_description, self.pbar])

        if render_summary:
            display(self.pbar_box)

    def _run_test(self, test):
        try:
            # run the test and log the performance if LOG_LEVEL is set to DEBUG
            log_performance(
                func=test.run,
                name=test.name,
                logger=logger,
            )()  # this is a decorator so we need to call it
        except Exception as e:
            logger.error(f"Failed to run test '{test.name}': {e}")
            test.result = TestPlanFailedResult(
                name=f"Failed {test.test_type}",
                error=e,
                message=f"Failed to run '{test.name}'",
                result_id=test.name,
            )

        if test.result is None:
            test.result = TestPlanFailedResult(
                name=f"Failed {test.test_type}",
                error=None,
                message=f"'{test.name}' did not return a result",
                result_id=test.name,
            )
            return

        if not isinstance(test.result, TestPlanResult):
            test.result = TestPlanFailedResult(
                name=f"Failed {test.test_type}",
                error=None,
                message=f"'{test.name}' returned an invalid result: {test.result}",
                result_id=test.name,
            )
            return

        self.results.append(test.result)

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
        if self.test_context is None:
            self.test_context = TestContext(
                dataset=self.dataset,
                model=self.model,
                models=self.models,
            )

        self.validate_context()

        if self.pbar is None:
            self._init_pbar(render_summary=render_summary, send=send)

        for test in self._tests:
            test_instance = test(
                test_context=self.test_context,
                params=self.get_config_params_for_test(test.name),
            )

            self.pbar_description.value = f"Running {test.test_type}: {test.name}"

            self._run_test(test_instance)

            self.pbar.value += 1

        if send:
            run_async(self.log_results)
            run_async_check(self._check_progress)

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

        index = 0
        for result in self.results:
            if result_widget := result._to_widget():
                accordions[result.result_id] = {
                    "id": index,
                    "widget": result_widget,
                    "result": result,
                }
                index += 1

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

        accordion_widget = widgets.Accordion(
            children=[v["widget"] for v in accordion_contents.values()],
        )
        # add titles to all the accordion items
        for result_id, accordion_item in accordion_contents.items():
            result = accordion_item["result"]

            test_title = result_id.split(".")[-1].title().replace("_", " ")
            if isinstance(result, TestPlanFailedResult):
                title = f"❌ {result.name}: {test_title} ({result_id})"
            else:
                title = f"{result.name}: {test_title} ({result_id})"

            try:
                accordion_widget.set_title(index=accordion_item["id"], title=title)
            except Exception as e:
                raise e

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

    def get_results(self, result_id: str = None) -> List[TestPlanResult]:
        """
        Returns one or more results of the test plan.
        """
        all_results = self.results or []

        if result_id is None:
            return all_results

        return [result for result in all_results if result.result_id == result_id]
