"""
TestPlan class
"""
from tqdm import tqdm
from typing import List


from ..api_client import log_test_result
from ..vm_models import Dataset, Model


class TestPlan:
    """
    Base class for test plans. Test plans are used to define any
    arbitrary grouping of tests that will be run on a dataset or model.
    """

    def __init__(
        self,
        name: str = None,
        config: dict() = None,
        dataset: Dataset = None,
        model: Model = None,
        tests: List[object] = [],
        results: List[object] = [],  # Results can hold  Metric, Figure, TestResults
    ):
        """
        :param config: The test plan configuration
        :param dataset: The dataset to run the tests on
        :param model: The model to run the tests on
        :param tests: The list of tests to run
        :param dict kwargs: Additional keyword arguments
        """
        self.config = config
        self.name = name
        self.tests = tests
        self.dataset = dataset
        self.model = model
        self.results = results

    def run(self, send=True):
        """
        Runs the test plan
        """
        print(f"Running test plan '{self.name}'...")
        # Empty the results cache on every run
        self.results = []

        for test in tqdm(self.tests):
            test_instance = test(dataset=self.dataset, model=self.model)
            self.results.append(test_instance.run())

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
