"""
Test Plans entry point
"""

from .tabular_datasets import GenericTabularDatasetTestPlan
from .test_plan import TestPlan


def get_by_name(name: str):
    """
    Returns the test plan by name
    """
    if name == "generic_tabular_dataset":
        return GenericTabularDatasetTestPlan

    raise ValueError(f"Test plan with name: '{name}' not found")


__all__ = ["TestPlan", "tabular_datasets"]
