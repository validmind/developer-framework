"""
TestContext
"""
from dataclasses import dataclass
from typing import List
from attr import field

import pandas as pd

from .dataset import Dataset
from .model import Model


@dataclass
class TestContext:
    """
    Holds context that can be used by tests to run.
    Allows us to store data that needs to be reused
    across different tests/metrics such as model predictions,
    shared dataset metrics, etc.
    """

    dataset: Dataset = None
    model: Model = None
    models: List[Model] = field(type=list)
    train_ds: Dataset = None
    test_ds: Dataset = None
    validation_ds: Dataset = None

    # These variables can be generated dynamically if not passed
    y_train_predict: object = None
    y_test_predict: object = None

    # Custom context data that can be set by metrics or tests using this context
    context_data: dict = None

    def __post_init__(self):
        if self.model and self.train_ds:
            self.y_train_predict = self.model.predict(self.train_ds.x)
        if self.model and self.test_ds:
            self.y_test_predict = self.model.predict(self.test_ds.x)

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
    def train_ds(self):
        return self.test_context.train_ds

    @property
    def test_ds(self):
        return self.test_context.test_ds

    @property
    def validation_ds(self):
        return self.test_context.validation_ds

    @property
    def y_train_predict(self):
        return self.test_context.y_train_predict

    @property
    def y_test_predict(self):
        return self.test_context.y_test_predict

    def class_predictions(self, y_predict):
        """
        Converts a set of probability predictions to class predictions

        Args:
            y_predict (np.array, pd.DataFrame): Predictions to convert

        Returns:
            (np.array, pd.DataFrame): Class predictions
        """
        # TODO: parametrize at some point
        return (y_predict > 0.5).astype(int)

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
