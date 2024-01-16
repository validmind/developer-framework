# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
TestContext
"""

# TODO: lets think about refactoring this file since it deals with both the `TestContext` and the `TestInput`.
# TestInput was previously used for both storing a global "context" for running tests to be able to
# share data, as well as for storing the inputs to those tests.
# We've since split this into two separate concepts.
# https://app.shortcut.com/validmind/story/2468/allow-arbitrary-test-context
# There is more changes to come around how we handle test inputs, so once we iron out that, we can refactor

from dataclasses import dataclass
from typing import ClassVar, List, Optional

import pandas as pd

from ..errors import MissingRequiredTestInputError, TestInputInvalidDatasetError
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

    # Custom context data that can be set by metrics or tests using this context
    context_data: Optional[dict] = None

    # TODO: here for backwards compatibility, remove this when appropriate
    dataset: VMDataset = None
    model: VMModel = None
    models: List[VMModel] = None

    def set_context_data(self, key, value):
        if self.context_data is None:
            self.context_data = {}

        self.context_data[key] = value

    def get_context_data(self, key):
        if self.context_data is None:
            return None

        return self.context_data.get(key)


@dataclass
class TestInput:
    """Holds models, datasets and other custom inputs for test(s)"""

    # TODO: we need to look into adding metadata for test inputs and logging that

    # Single dataset for dataset-only tests
    dataset: VMDataset = None

    # Model and corresponding datasets for model related tests
    model: VMModel = None

    # Multiple models for model comparison tests
    models: List[VMModel] = None

    # Custom inputs that can store datasets, models etc.
    inputs: dict = None


@dataclass
class TestUtils:
    """Utility methods for classes that receive a TestContext"""

    required_inputs: ClassVar[List[str]]

    test_context: TestContext
    test_input: Optional[TestInput] = None

    def _get_input(self, key):
        """Retrieve an input from the Test Input or, for backwards compatibility,
        the Test Context.

        TODO: remove this backwards compatibility when appropriate
        """
        try:
            _input = getattr(self.test_input, key)
        except AttributeError:
            _input = getattr(self.test_context, key)

        return _input

    @property
    def dataset(self):
        return self._get_input("dataset")

    @property
    def model(self):
        return self._get_input("model")

    @property
    def models(self):
        return self._get_input("models")

    @property
    def inputs(self):
        return self._get_input("inputs")

    @property
    def df(self):
        """
        Returns a Pandas DataFrame for the dataset, first checking if
        we passed in a Dataset or a DataFrame
        """
        if self.dataset is None:
            raise TestInputInvalidDatasetError("dataset must be set")

        if isinstance(self.dataset, VMDataset):
            return self.dataset.raw_dataset
        elif isinstance(self.dataset, pd.DataFrame):
            return self.dataset

        raise TestInputInvalidDatasetError(
            "dataset must be a Pandas DataFrame or a validmind Dataset object"
        )

    def validate_context(self):
        """
        Validates that the context elements are present
        in the instance so that the test suite can be run

        Raises:
            MissingRequiredTestContextError: If a required context element is missing.
        """

        def recursive_attr_check(obj, attr_chain):
            """
            Recursively checks if the given object has the specified attribute chain.

            Args:
                obj: The object to check.
                attr_chain: A string representing the attribute chain, separated by dots.

            Returns:
                True if the object has the attribute chain, False otherwise.
            """
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
                raise MissingRequiredTestInputError(
                    f"{context_name} '{element}' is a required input and must be passed "
                    "as a keyword argument to the test suite"
                )
