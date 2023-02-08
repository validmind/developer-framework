"""
Class for storing ValidMind metric objects and associated
data for display and reporting purposes
"""
from dataclasses import dataclass
from typing import ClassVar, Optional, Union

import pandas as pd
from pandas import DataFrame

from .dataset import Dataset
from .test_context import TestContext
from ..utils import format_records, format_key_values


@dataclass()
class Metric:
    """
    Metric objects track the schema supported by the ValidMind API
    """

    # Test Context
    test_context: TestContext

    # Class Variables
    type: str = ""  # type of metric: "training", "evaluation", etc.
    scope: str = ""  # scope of metric: "training_dataset", "test_dataset", etc.
    key: str = ""  # unique identifer for metric: "accuracy", "loss", "precision", etc.
    value_formatter: Optional[str] = None  # "records" or "key_values"
    default_params: ClassVar[dict] = {}

    # Instance Variables
    params: dict = None
    value: Union[dict, list, DataFrame] = None

    def __post_init__(self):
        """
        Set default params if not provided
        """
        if self.params is None:
            self.params = self.default_params

    @property
    def dataset(self):
        return self.test_context.dataset

    @property
    def model(self):
        return self.test_context.model

    @property
    def train_ds(self):
        return self.test_context.train_ds

    @property
    def test_ds(self):
        return self.test_context.test_ds

    @property
    def y_train_predict(self):
        return self.test_context.y_train_predict

    @property
    def y_test_predict(self):
        return self.test_context.y_test_predict

    def serialize(self):
        """
        Serializes the Metric to a dictionary so it can be sent to the API
        """
        if self.value_formatter == "records":
            value = format_records(self.value)
        elif self.value_formatter == "key_values":
            value = format_key_values(self.value)
        elif self.value_formatter is not None:
            raise ValueError(
                f"Invalid value_formatter: {self.value_formatter}. "
                "Must be one of 'records' or 'key_values'"
            )
        else:
            value = self.value

        if isinstance(value, DataFrame):
            raise ValueError(
                "A DataFrame value was provided but no value_formatter was specified."
            )

        return {
            "type": self.type,
            "scope": self.scope,
            "key": self.key,
            "value": value,
        }

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
        Run the metric calculation and cache its results
        """
        raise NotImplementedError

    def cache_results(self, metric_value: Union[dict, list, DataFrame]):
        """
        Cache the results of the metric calculation and do any post-processing if needed
        """
        self.value = metric_value
