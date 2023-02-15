"""
Test Plans entry point
"""

from .sklearn_classifier import (
    SKLearnClassifierMetrics,
    SKLearnClassifier,
    SKLearnClassifierValidation,
)
from .tabular_datasets import (
    TabularDataset,
    TabularDataQuality,
    TabularDatasetDescription,
)

core_test_plans = {
    "sklearn_classifier_metrics": SKLearnClassifierMetrics,
    "sklearn_classifier_validation": SKLearnClassifierValidation,
    "sklearn_classifier": SKLearnClassifier,
    "tabular_dataset": TabularDataset,
    "tabular_dataset_description": TabularDatasetDescription,
    "tabular_data_quality": TabularDataQuality,
}


def get_by_name(name: str):
    """
    Returns the test plan by name
    """

    if name in core_test_plans:
        return core_test_plans[name]

    raise ValueError(f"Test plan with name: '{name}' not found")


__all__ = ["tabular_datasets"]
