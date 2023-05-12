"""
Default test suites provided by the developer framework.
"""

from ..vm_models import TestSuite


class TabularDataset(TestSuite):
    """
    Test suite for tabular datasets.
    """

    required_context = ["dataset"]

    test_plans = [
        "tabular_dataset_description",
        "tabular_data_quality",
    ]


class BinaryClassifierModelValidation(TestSuite):
    """
    Test suite for binary classification models.
    """

    required_context = ["model"]

    test_plans = [
        "binary_classifier_metrics",
        "binary_classifier_validation",
        "binary_classifier_model_diagnosis",
    ]


class BinaryClassifierFullSuite(TestSuite):
    """
    Full test suite for binary classification models.
    """

    required_context = ["dataset", "model"]

    test_plans = [
        "tabular_dataset_description",
        "tabular_data_quality",
        "binary_classifier_metrics",
        "binary_classifier_validation",
        "binary_classifier_model_diagnosis",
    ]
