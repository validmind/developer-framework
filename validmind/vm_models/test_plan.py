"""
TestPlan class
"""
from dataclasses import dataclass
from tqdm import tqdm
from typing import ClassVar, List


from ..api_client import log_metrics, log_test_result
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
    results: ClassVar[
        List[object]
    ] = []  # Results can hold  Metric, Figure, TestResults

    # Instance Variables
    config: dict() = None

    # Single dataset for dataset-only tests
    dataset: Dataset = None

    # Model and corresponding datasets for model related tests
    model: Model = None
    train_ds: Dataset = None
    test_ds: Dataset = None

    def __post_init__(self):
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
            elif getattr(self, element) is None:
                raise ValueError(
                    f"Test plan '{self.name}' requires '{element}' to be present in the test context"
                )

    def run(self, send=True):
        """
        Runs the test plan
        """
        print(f"Running test plan '{self.name}'...")
        self.results = []  # Empty the results cache on every run
        test_context = TestContext(
            dataset=self.dataset,
            model=self.model,
            train_ds=self.train_ds,
            test_ds=self.test_ds,
        )

        for test in tqdm(self.tests):
            test_instance = test(test_context)
            print(f"Running test - {test.test_type} : {test_instance.name}")
            result = test_instance.run()

            if result is None:
                print("Test returned None, skipping...")
                continue

            if not isinstance(result, TestPlanResult):
                raise ValueError(
                    f"Test '{test_instance.name}' must return a TestPlanResult"
                )

            self.results.append(result)

        if send:
            self.log_results()

    def log_results(self):
        print(f"Sending results of test plan execution '{self.name}' to ValidMind...")
        # API accepts metrics as a list, we need to do the same for test results
        metrics = []
        for result in self.results:
            result_class = result.__class__.__name__
            if result.test_results is not None:
                log_test_result(result.test_results)
            elif result.metric is not None:
                metrics.append(result.metric)
            else:
                print(result_class)
                raise ValueError(f"Invalid result type: {result_class}")

        if len(metrics) > 0:
            log_metrics(metrics)
