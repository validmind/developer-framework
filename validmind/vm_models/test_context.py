"""
TestContext
"""
from dataclasses import dataclass
from typing import ClassVar, List

import pandas as pd

from .dataset import Dataset
from .model import Model


@dataclass
class TestContext:
    """
    Holds context that can be used by tests to run.
    Allows us to store data that needs to be reused
    across different tests/metrics such as shared dataset metrics, etc.
    """

    dataset: Dataset = None
    model: Model = None
    models: List[Model] = None

    # Custom context data that can be set by metrics or tests using this context
    context_data: dict = None

    def set_context_data(self, key, value):
        if self.context_data is None:
            self.context_data = {}

        self.context_data[key] = value

    def get_context_data(self, key):
        if self.context_data is None:
            return None

        return self.context_data.get(key)


class TestContextUtils:
    """
    Utility methods for classes that receive a TestContext

    TODO: more validation
    """

    # Test Context
    test_context: TestContext
    required_context: ClassVar[List[str]]

    @property
    def dataset(self):
        return self.test_context.dataset

    @property
    def model(self):
        return self.test_context.model

    @property
    def models(self):
        return self.test_context.models

    @property
    def df(self):
        """
        Returns a Pandas DataFrame for the dataset, first checking if
        we passed in a Dataset or a DataFrame
        """
        if self.dataset is None:
            raise ValueError("dataset must be set")

        if isinstance(self.dataset, Dataset):
            return self.dataset.raw_dataset
        elif isinstance(self.dataset, pd.DataFrame):
            return self.dataset

        raise ValueError(
            "dataset must be a Pandas DataFrame or a validmind Dataset object"
        )

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
