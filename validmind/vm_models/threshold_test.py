"""
(Threshold)Test class wrapper. Our API exposes the concept of of a
Test (as test_results) but we'll refer to it as a ThresholdTest to
avoid confusion with the "tests" in the general data science/modeling sense.

TODO: Test definitions should be supported in the API too
"""
import pandas as pd

from dataclasses import dataclass
from typing import ClassVar, List, Union

from .dataset import Dataset
from .test_result import TestResult, TestResults


@dataclass
class ThresholdTest:
    """
    A threshold test is a combination of a metric/plot we track and a
    corresponding set of parameters and thresholds values that allow
    us to determine whether the metric/plot passes or fails.
    """

    # Class Variables
    category: ClassVar[str] = ""
    name: ClassVar[str] = ""
    default_params: ClassVar[dict] = {}

    # Instance Variables
    dataset: Union[pd.DataFrame, Dataset] = None
    params: dict = None
    model: object = None
    test_results: TestResults = None

    def __post_init__(self):
        """
        Set default params if not provided
        """
        if self.params is None:
            self.params = self.default_params

    @property
    def df(self):
        """
        Returns a Pandas DataFrame for the dataset, first checking if
        we passed in a Dataset or a DataFrame
        """
        if self.dataset is None:
            raise ValueError("dataset must be set")
        elif isinstance(self.dataset, Dataset):
            return self.dataset.raw_dataset
        elif isinstance(self.dataset, pd.DataFrame):
            return self.dataset
        else:
            raise ValueError(
                "dataset must be a Pandas DataFrame or a validmind Dataset object"
            )

    def run(self, *args, **kwargs):
        """
        Run the test and cache its results
        """
        raise NotImplementedError

    def cache_results(self, results: List[TestResult], passed: bool):
        """
        Cache the individual results of the threshold test as a list of TestResult objects
        """
        self.test_results = TestResults(
            category=self.category,
            test_name=self.name,
            params=self.params,
            passed=passed,
            results=results,
        )
