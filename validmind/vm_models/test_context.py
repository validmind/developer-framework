"""
TestContext
"""
from dataclasses import dataclass

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
    train_ds: Dataset = None
    test_ds: Dataset = None

    # These variables can be generated dynamically if not passed
    y_train_predict: object = None
    y_test_predict: object = None

    def __post_init__(self):
        if self.model and self.train_ds:
            print("Generating predictions train dataset...")
            self.y_train_predict = self.model.predict(self.train_ds.x)
        if self.model and self.test_ds:
            print("Generating predictions test dataset...")
            self.y_test_predict = self.model.predict(self.test_ds.x)
