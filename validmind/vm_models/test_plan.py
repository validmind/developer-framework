"""
TestPlan class
"""
from dataclasses import dataclass
from typing import ClassVar, List

from IPython.display import display, HTML
from tqdm import tqdm

from .dataset import Dataset
from .model import Model
from .test_context import TestContext
from .test_plan_result import TestPlanResult

# A test plan can have 1 or more test plans


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

    # Single dataset for dataset-only tests
    dataset: Dataset = None

    # Model and corresponding datasets for model related tests
    model: Model = None
    train_ds: Dataset = None
    test_ds: Dataset = None

    # tqdm progress bar
    pbar: tqdm = None

    def __post_init__(self):
        if self.test_context is not None:
            self.dataset = self.test_context.dataset
            self.model = self.test_context.model
            self.train_ds = self.test_context.train_ds
            self.test_ds = self.test_context.test_ds

        self.validate_context()

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

    def run(self, send=True):
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
            test_instance = test(self.test_context)

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

        if send:
            self.log_results()

        for test_plan in self.test_plans:
            test_plan_instance = test_plan(
                test_context=self.test_context,
                pbar=self.pbar,
            )
            test_plan_instance.run(send=send)

        self.pbar.close()
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
            result.log()
            self.pbar.update(1)

    def summarize(self):
        """Summarizes the results of the test plan

        This method will be called after the test plan has been run and all results have been
        logged to ValidMind. It will summarize the results of the test plan by creating an
        html table with the results of each test. This html table will be displayed in an
        ipython notebook or in a jupyter notebook.
        """
        if len(self.results) == 0:
            return

        html = f"<h2>Results for <i>{self.name}</i> Test Plan:</h2><hr>"

        for result in self.results:
            result_html = result._to_html()
            # wrap the html in a div and indent the div to make it look as part of a section
            # add scrollable class to the div to make it scrollable
            # wrap this div in another div which is expandable and add a button to expand it
            # this is to make the results collapsible (should be collapsed by default)
            html += f"""
            <div class='expandable'>
                <div class='expandable-content'>
                    <div class='result'>
                        {result_html}
                    </div>
                </div>
            </div>
            """

        # add css to make the expandable div have a border and a nice background color
        # to set it apart from the rest of the notebook
        html += """
        <style>
            .expandable {
                margin: 10px 0;
            }
            .result {
                padding: 10px;
                background-color: #f1f1f1;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        </style>
        """

        # html += """
        # <style>
        #     .expandable {
        #         margin: 10px 0;
        #     }
        #     .expandable-button {
        #         background-color: #eee;
        #         color: #444;
        #         cursor: pointer;
        #         padding: 18px;
        #         width: 100%;
        #         border: none;
        #         text-align: left;
        #         outline: none;
        #         font-size: 15px;
        #         transition: 0.4s;
        #     }
        #     .expandable-button.active, .expandable-button:hover {
        #         background-color: #ccc;
        #     }
        #     .expandable-content {
        #         padding: 0 18px;
        #         background-color: #f1f1f1;
        #     }
        #     .expandable-content.active {
        #         display: block;
        #     }
        #     .result {
        #         margin-left: 20px;
        #         overflow: auto;
        #     }
        # </style>
        # <script>
        #     var expandableButtons = document.getElementsByClassName('expandable-button');
        #     for (var i = 0; i < expandableButtons.length; i++) {
        #         expandableButtons[i].addEventListener('click', function() {
        #             this.classList.toggle('active');
        #             var content = this.nextElementSibling;
        #             if (content.style.display === 'block') {
        #                 content.style.display = 'none';
        #             } else {
        #                 content.style.display = 'block';
        #             }
        #         });
        #     }
        # </script>
        # """

        display(HTML(html))
