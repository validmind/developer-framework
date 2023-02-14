"""
Test Plans entry point
"""

from .sklearn_classifier import (
    SKLearnClassifierMetricsTestPlan,
    SKLearnClassifierTestPlan,
    SKLearnClassifierValidationTestPlan,
)
from .tabular_datasets import GenericTabularDatasetTestPlan


def get_by_name(name: str):
    """
    Returns the test plan by name
    """
    if name == "generic_tabular_dataset":
        return GenericTabularDatasetTestPlan
    elif name == "sklearn_classifier_metrics":
        return SKLearnClassifierMetricsTestPlan
    elif name == "sklearn_classifier_validation":
        return SKLearnClassifierValidationTestPlan
    elif name == "sklearn_classifier":
        return SKLearnClassifierTestPlan

    raise ValueError(f"Test plan with name: '{name}' not found")


__all__ = ["tabular_datasets"]
