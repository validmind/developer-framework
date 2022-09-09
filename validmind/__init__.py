"""
Exports
"""

from .client import (
    init,
    log_dataset,
    log_metadata,
    log_metrics,
    log_model,
    log_test_results,
    log_training_metrics,
    start_run,
    log_figure,
)

from .models import DatasetTargets, Figure, Metric, Model, ModelAttributes
from .model_evaluation import evaluate_model
from .tests import run_dataset_tests
from .tests.config import TestResult, TestResults

# High Level API Wrappers
# -----------------------
# These functions are wrappers around the lower level functions that map directly
# to an HTTP API call. We'll be slowly separating the Python API from the HTTP API


def analyze_dataset(
    dataset,
    dataset_type,
    dataset_options=None,
    targets=None,
    features=None,
    send=True,
):
    """
    Analyzes a dataset by extracting summary statistics and running data quality tests
    on it. Results are logged to the ValidMind API

    :param pd.DataFrame dataset: We only support Pandas DataFrames at the moment
    :param str dataset_type: The dataset type is necessary for mapping and relating multiple datasets together.
        Can be one of training, validation, test or generic
    :param dict dataset_options: A dictionary of options for the dataset
    :param vm.vm.DatasetTargets targets: A list of target variables
    :param list features: An optional list of extra attributes for any feature
    :param bool send: Whether to post the test results to the API. send=False is useful for testing
    """
    print("Analyzing dataset...")
    vm_dataset = log_dataset(dataset, dataset_type, targets=targets, features=features)

    print("Running data quality tests...")
    results = run_dataset_tests(
        dataset=dataset,
        dataset_type=dataset_type,
        vm_dataset=vm_dataset,
        send=send,
    )

    return results


__all__ = [
    "analyze_dataset",
    "evaluate_model",
    "init",
    "log_dataset",
    "log_metadata",
    "log_metrics",
    "log_model",
    "log_test_results",
    "log_training_metrics",
    "run_dataset_tests",
    "start_run",
    "log_figure",
    "DatasetTargets",
    "Figure",
    "Metric",
    "Model",
    "ModelAttributes",
    "TestResult",
    "TestResults",
]
