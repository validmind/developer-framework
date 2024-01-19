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

from ..errors import MissingRequiredTestInputError
from ..logging import get_logger
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

logger = get_logger(__name__)


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


class TestInput:
    """Holds models, datasets and other arbitrary inputs for test(s)

    Attributes:
        dataset (VMDataset): Single dataset for dataset-only tests
        model (VMModel): Single model for model-related tests
        models (List[VMModel]): Multiple models for model comparison tests
        ... (any): Any other arbitrary inputs that can be used by tests
    """

    # TODO: we need to look into adding metadata for test inputs and logging that

    def __init__(self, inputs):
        """Initialize with either a dictionary of inputs"""

        for key, value in inputs.items():
            setattr(self, key, value)

    def __getitem__(self, key):
        """Allow accessing inputs via `self.inputs["input_name"]`"""
        return getattr(self, key)

    def __repr__(self):
        """Human-readable string representation of the object."""
        attrs = ",\n    ".join(
            f"{key}={value!r}" for key, value in self.__dict__.items()
        )
        return f"{self.__class__.__name__}(\n    {attrs}\n)"


@dataclass
class TestUtils:
    """Utility methods for classes that receive a TestContext"""

    required_inputs: ClassVar[List[str]]

    context: Optional[TestContext] = None
    inputs: Optional[TestInput] = None

    def _get_legacy_input(self, key):
        """Retrieve an input from the Test Input or, for backwards compatibility,
        the Test Context

        We should remove this once we all tests (including customer tests) are
        using `self.inputs.<input_name>` instead of `self.<input_name>`.
        """
        try:
            _input = getattr(self.inputs, key)
        except AttributeError:
            # in case any code is still manually creating a TestContext instead of
            # a TestInput, we'll still support that for now by checking there
            _input = getattr(self.context, key)

        return _input

    @property
    def dataset(self):
        """[DEPRECATED] Returns the input dataset for the test"""
        logger.warning(
            "Accesing the input dataset using `self.dataset` is deprecated. "
            "Use `self.inputs.dataset` instead."
        )
        return self._get_legacy_input("dataset")

    @property
    def model(self):
        """[DEPRECATED] Returns the input model for the test"""
        logger.warning(
            "Accesing the input model using `self.model` is deprecated. "
            "Use `self.inputs.model` instead."
        )
        return self._get_legacy_input("model")

    @property
    def models(self):
        """[DEPRECATED] Returns the input models for the test"""
        logger.warning(
            "Accesing the input models using `self.models` is deprecated. "
            "Use `self.inputs.models` instead."
        )
        return self._get_legacy_input("models")

    def validate_inputs(self):
        """
        Validates that the required inputs are present in the test input object.

        Raises:
            MissingRequiredTestInputError: If a required context element is missing.
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
            if not recursive_attr_check(self.inputs, element):
                context_name = CONTEXT_NAMES.get(element, element)
                raise MissingRequiredTestInputError(
                    f"{context_name} '{element}' is a required input and must be "
                    "passed as part of the test inputs dictionary."
                )
