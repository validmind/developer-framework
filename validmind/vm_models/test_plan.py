"""
TestPlan class
"""
import os

from dataclasses import dataclass
from typing import ClassVar, List

from IPython.display import display, HTML
from tqdm import tqdm

from ..utils import is_notebook
from .dataset import Dataset
from .model import Model
from .test_context import TestContext
from .test_plan_result import TestPlanResult

VM_SUMMARIZE_TEST_PLANS = os.environ.get("VM_SUMMARIZE_TEST_PLANS", "True")


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
    test_context: TestContext = None
    # Stores a reference to the child test plan instances
    _test_plan_instances: List[object] = None

    # Single dataset for dataset-only tests
    dataset: Dataset = None

    # Model and corresponding datasets for model related tests
    model: Model = None
    train_ds: Dataset = None
    test_ds: Dataset = None

    # tqdm progress bar
    pbar: tqdm = None

    def __repr__(self):
        class_name = type(self).__name__

        if self.config is None:
            return f"{class_name}(test_context={self.test_context})"

        return f"{class_name}(test_context={self.test_context}, config={{...}})"

    def __post_init__(self):
        if self.test_context is not None:
            self.dataset = self.test_context.dataset
            self.model = self.test_context.model
            self.train_ds = self.test_context.train_ds
            self.test_ds = self.test_context.test_ds

        self.validate_context()

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

        return self.config.get(test_name, None)

    def run(self, send=True):  # noqa C901 'TestPlan.run' is too complex
        """
        Runs the test plan
        """
        self.results = []  # Empty the results cache on every run

        if self.test_context is None:
            self.test_context = TestContext(
                dataset=self.dataset,
                model=self.model,
                train_ds=self.train_ds,
                test_ds=self.test_ds,
            )

        if self.pbar is None:
            self.pbar = tqdm(
                total=len(self.tests),
                desc=f"Running test plan: '{self.name}'",
                leave=False,
            )
        else:
            # if already initiated (meaning we are in a sub test plan), reset it
            self.pbar.reset(total=len(self.tests))
            self.pbar.set_description(f"Running sub test plan: '{self.name}'")

        for test in self.tests:
            # TODO: we need to unify key/name for any object
            if hasattr(test, "key"):
                test_name = test.key
            elif hasattr(test, "name"):
                test_name = test.name

            test_params = self.get_config_params_for_test(test_name)
            test_instance = test(self.test_context, params=test_params)

            self.pbar.set_description(f"Running {test.test_type}: {test_instance.name}")

            result = test_instance.run()

            if result is None:
                self.pbar.set_description("Test returned None, skipping...")
                self.pbar.update(1)
                continue

            if not isinstance(result, TestPlanResult):
                raise ValueError(
                    f"'{test_instance.name}' must return an instance of TestPlanResult Base Class"
                )

            self.results.append(result)
            self.pbar.update(1)

        # Set the progress bar to 100% if it's not already
        self.pbar.update(self.pbar.total - self.pbar.n)

        if send:
            self.log_results()

        for test_plan in self.test_plans:
            test_plan_instance = test_plan(
                config=self.config,
                test_context=self.test_context,
                pbar=self.pbar,
            )
            test_plan_instance.run(send=send)

            # Build up the subtest plan instances so we can log them
            if self._test_plan_instances is None:
                self._test_plan_instances = []

            self._test_plan_instances.append(test_plan_instance)

        self.pbar.close()

        if VM_SUMMARIZE_TEST_PLANS == "True":
            self.summarize()

    def log_results(self):
        """Logs the results of the test plan to ValidMind

        This method will be called after the test plan has been run and all results have been
        collected. This method will log the results to ValidMind.
        """
        self.pbar.reset(total=len(self.results))
        self.pbar.set_description(
            f"Sending results of test plan execution '{self.name}' to ValidMind..."
        )

        for result in self.results:
            self.pbar.set_description(f"Logging result: {result}")

            try:
                result.log()
            except Exception as e:
                self.pbar.set_description(
                    f"Failed to log result: {result} for test plan result '{str(result)}'"
                )
                print(e)
                raise e

            self.pbar.update(1)

    def _results_title(self, html: str = "") -> str:
        """
        Builds the title for the results of the test plan
        """
        html += f"<h2>Results for <i>{self.title()}</i> Test Plan:</h2><hr>"

        return html

    def _results_description(self, html: str = "") -> str:
        """
        Builds the description for the results of the test plan. Subclasses
        should override this method to provide an appropriate description
        """
        html += f'<div class="result">{self.description()}</div>'
        return html

    def _results_summary(self, html: str = "") -> str:
        """
        Builds a summary of the results for each of the tests in the test plan
        """
        for result in self.results:
            result_html = result._to_html()
            if result_html:
                html += f'<div class="result">{result_html}</div>'

        return html

    def summarize(self):
        """Summarizes the results of the test plan

        This method will be called after the test plan has been run and all results have been
        logged to ValidMind. It will summarize the results of the test plan by creating an
        html table with the results of each test. This html table will be displayed in an
        VS Code, Jupyter or other notebook environment.
        """
        if not is_notebook():
            return

        if len(self.results) == 0:
            return

        html = ""
        html = self._results_title(html)
        html = self._results_description(html)
        html = self._results_summary(html)

        html += """
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

        display(HTML(html))

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
