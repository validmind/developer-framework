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
