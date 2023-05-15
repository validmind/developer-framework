"""
Entrypoint for test suites.
"""
import pandas as pd

from .test_suites import (
    BinaryClassifierFullSuite,
    BinaryClassifierModelValidation,
    TabularDataset,
    TimeSeriesDataset,
    TimeSeriesModelValidation,
)
from ..vm_models import TestSuite

core_test_suites = {
    "binary_classifier_full_suite": BinaryClassifierFullSuite,
    "binary_classifier_model_validation": BinaryClassifierModelValidation,
    "tabular_dataset": TabularDataset,
    "time_series_dataset": TimeSeriesDataset,
    "time_series_model_validation": TimeSeriesModelValidation,
}

# These test suites can be added by the user
custom_test_suites = {}


def _get_all_test_suites():
    """
    Returns a dictionary of all test suites.

    Merge the core and custom test suites, with the custom suites
    taking precedence, i.e. allowing overriding of core test suites
    """
    return {**core_test_suites, **custom_test_suites}


def get_by_name(name: str):
    """
    Returns the test suite by name
    """
    all_test_suites = _get_all_test_suites()
    if name in all_test_suites:
        return all_test_suites[name]

    raise ValueError(f"Test suite with name: '{name}' not found")


def list_suites(pretty: bool = True):
    """
    Returns a list of all available test suites
    """

    all_test_suites = _get_all_test_suites()

    if not pretty:
        return list(all_test_suites.keys())

    table = []
    for name, test_suite in all_test_suites.items():
        table.append(
            {
                "ID": name,
                "Name": test_suite.__name__,
                "Description": test_suite.__doc__.strip(),
                "Test Plans": ", ".join(test_suite.test_plans),
            }
        )

    return pd.DataFrame(table).style.hide(axis="index")


def register_test_suite(suite_id: str, suite: TestSuite):
    """
    Registers a custom test suite
    """
    custom_test_suites[suite_id] = suite
    print(f"Registered test suite: {suite_id}")
