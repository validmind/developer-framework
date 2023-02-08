"""
TestPlan class
"""
from dataclasses import dataclass
from tqdm import tqdm
from typing import ClassVar, List


from ..api_client import log_test_result
from ..vm_models import Dataset, Model, TestContext

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
    results: ClassVar[
        List[object]
    ] = []  # Results can hold  Metric, Figure, TestResults

    # Instance Variables
    config: dict() = None
    dataset: Dataset = None
    model: Model = None
    train_ds: Dataset = None
    test_ds: Dataset = None

    def __post_init__(self):
        """
        :param config: The test plan configuration
        :param dataset: The dataset to run the tests on
        :param model: The model to run the tests on
        :param tests: The list of tests to run
        :param dict kwargs: Additional keyword arguments
        """
        # self.config = config
        # self.name = name
        # self.tests = tests

        # # Single dataset for dataset-only tests
        # self.dataset = dataset

        # # Model and corresponding datasets for model related tests
        # self.model = model
        # self.train_ds = train_ds
        # self.test_ds = test_ds

        # self.test_plans = test_plans
        # self.results = results
        print("validate_context")
        self.validate_context()

    def validate_context(self):
        """
        Validates that the context elements are present
        in the instance so that the test plan can be run
        """
        for element in self.required_context:
            print("element", element)
            print("self.element", getattr(self, element))
            if not hasattr(self, element):
                raise ValueError(
                    f"Test plan '{self.name}' requires '{element}' to be present in the test context"
                )
            elif getattr(self, element) is None:
                raise ValueError(
                    f"Test plan '{self.name}' requires '{element}' to be present in the test context"
                )

    def run(self, send=True):
        """
        Runs the test plan
        """
        print(f"Running test plan '{self.name}'...")
        # Empty the results cache on every run
        self.results = []
        test_context = TestContext(
            dataset=self.dataset,
            model=self.model,
            train_ds=self.train_ds,
            test_ds=self.test_ds,
        )

        for test in tqdm(self.tests):
            test_instance = test(test_context)
            result = test_instance.run()

            if result:
                self.results.append(result)

        if send:
            self.log_results()

    def log_results(self):
        print(f"Sending results of test plan execution '{self.name}' to ValidMind...")

        for result in self.results:
            result_class = result.__class__.__name__
            if result_class == "TestResults":
                log_test_result(result)
            else:
                raise ValueError("Only TestResults are supported at the moment")
