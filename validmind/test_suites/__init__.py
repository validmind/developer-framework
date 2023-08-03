# Copyright © 2023 ValidMind Inc. All rights reserved.

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
from ..logging import get_logger
from ..test_plans import get_by_id as get_test_plan
from ..tests import load_test
from ..utils import format_dataframe
from ..vm_models import TestSuite

logger = get_logger(__name__)

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


def get_by_id(test_suite_id: str):
    """
    Returns the test suite by ID
    """
    try:
        return _get_all_test_suites()[test_suite_id]
    except KeyError:
        raise ValueError(f"Test suite with ID: '{test_suite_id}' not found")


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

    return format_dataframe(pd.DataFrame(table))


def describe_suite(test_suite_id: str, verbose=False):
    """
    Describes a Test Suite by ID

    Args:
        test_suite_id: Test Suite ID
        verbose: If True, describe all plans and tests in the Test Suite

    Returns:
        pandas.DataFrame: A formatted table with the Test Suite description
    """
    test_suite = get_by_id(test_suite_id)

    if not verbose:
        return format_dataframe(
            pd.DataFrame(
                [
                    {
                        "ID": test_suite_id,
                        "Name": test_suite.__name__,
                        "Description": test_suite.__doc__.strip(),
                        "Test Plans": ", ".join(test_suite.test_plans),
                    }
                ]
            )
        )

    df = pd.DataFrame()

    for test_plan_id in test_suite.test_plans:
        test_plan = get_test_plan(test_plan_id)
        for test_id in test_plan.tests:
            test = load_test(test_id)
            row = {
                "Test Suite ID": test_suite_id,
                "Test Suite Name": test_suite.__name__,
                "Test Plan ID": test_plan_id,
                "Test Plan Name": test_plan.__name__,
                "Test ID": test_id,
                "Test Name": test.__name__,
                "Test Type": test.test_type,
            }
            df = pd.concat([df, pd.DataFrame([row])])

    return format_dataframe(df.reset_index(drop=True))


# TODO: remove this... here for backwards compatibility
describe_test_suite = describe_suite


def register_test_suite(suite_id: str, suite: TestSuite):
    """
    Registers a custom test suite
    """
    custom_test_suites[suite_id] = suite
    logger.info(f"Registered test suite: {suite_id}")
