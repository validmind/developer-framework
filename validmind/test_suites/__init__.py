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
from .. import test_plans

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


def _format_dataframe(df):
    df = df.style.set_properties(**{"text-align": "left"}).hide(axis="index")
    df = df.set_table_styles([dict(selector="th", props=[("text-align", "left")])])
    return df


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

    return _format_dataframe(pd.DataFrame(table))


def describe_test_suite(id: str):
    """
    Returns a list of all available test suites
    """

    all_test_suites = _get_all_test_suites()
    table = []
    for name, test_suite in all_test_suites.items():
        if name == id:
            table.append(
                {
                    "ID": name,
                    "Name": test_suite.__name__,
                    "Description": test_suite.__doc__.strip(),
                    "Test Plans": ", ".join(test_suite.test_plans),
                }
            )

    return _format_dataframe(pd.DataFrame(table))


def register_test_suite(suite_id: str, suite: TestSuite):
    """
    Registers a custom test suite
    """
    custom_test_suites[suite_id] = suite
    print(f"Registered test suite: {suite_id}")


def describe_test_suites_plans_tests():
    table = []
    test_suites = list_suites()

    # Test suites
    for _, test_suite in test_suites.data.iterrows():
        # Test plans
        for p in test_suite["Test Plans"].split(","):
            plan = test_plans.describe_plan(p.strip()).data
            # List of tests from test plan
            for t in plan["Tests"]:
                tests = t.split(",")
                # Iterate tests
                for test in tests:
                    test = list(filter(None, test.split(" ")))
                    test_dict = (
                        test_plans.describe_test(test[0])
                        .data.reset_index(drop=True)
                        .to_dict("records")[0]
                    )
                    table.append(
                        {
                            "Test Suite": test_suite["ID"],
                            "Test Plan": p,
                            "Test Type": test_dict["Test Type"],
                            "Test ID": test_dict["ID"],
                            "Test Name": test_dict["Name"],
                            "Test Description": test_dict["Description"],
                        }
                    )

    return _format_dataframe(pd.DataFrame(table))
