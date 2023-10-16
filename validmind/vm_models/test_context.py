# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
TestContext
"""
from dataclasses import dataclass
from typing import ClassVar, List

import pandas as pd

from ..errors import MissingRequiredTestContextError, TestContextInvalidDatasetError
from .dataset import VMDataset
from .model import VMModel

# More human readable context names for error messages
CONTEXT_NAMES = {
    "dataset": "Dataset",
    "model": "Model",
    "models": "Models",
    "model.train_ds": "Model Training Dataset",
    "model.test_ds": "Model Testing Dataset",
    "model.validation_ds": "Model Validation Dataset",
    "train_ds": "Training Dataset",
    "test_ds": "Testing Dataset",
    "validation_ds": "Validation Dataset",
}


@dataclass
class TestContext:
    """
    Holds context that can be used by tests to run.
    Allows us to store data that needs to be reused
    across different tests/metrics such as shared dataset metrics, etc.
    """

    # Single dataset for dataset-only tests
    dataset: VMDataset = None

    # Model and corresponding datasets for model related tests
    model: VMModel = None

    # Multiple models for model comparison tests
    models: List[VMModel] = None

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


@dataclass
class TestContextUtils:
    """
    Utility methods for classes that receive a TestContext

    TODO: more validation
    """

    # Test Context
    test_context: TestContext
    required_inputs: ClassVar[List[str]]

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
            raise TestContextInvalidDatasetError("dataset must be set")

        if isinstance(self.dataset, VMDataset):
            return self.dataset.raw_dataset
        elif isinstance(self.dataset, pd.DataFrame):
            return self.dataset

        raise TestContextInvalidDatasetError(
            "dataset must be a Pandas DataFrame or a validmind Dataset object"
        )

    def validate_context(self):
        """
        Validates that the context elements are present
        in the instance so that the test suite can be run
        """

        def recursive_attr_check(obj, attr_chain):
            attrs = attr_chain.split(".")
            if not hasattr(obj, attrs[0]) or getattr(obj, attrs[0]) is None:
                return False
            return len(attrs) == 1 or recursive_attr_check(
                getattr(obj, attrs[0]),
                ".".join(attrs[1:]),
            )

        required_inputs = self.required_inputs or []
        for element in required_inputs:
            if not recursive_attr_check(self, element):
                context_name = CONTEXT_NAMES.get(element, element)
                raise MissingRequiredTestContextError(
                    f"{context_name} '{element}' is a required input and must be passed "
                    "as a keyword argument to the test suite"
                )
