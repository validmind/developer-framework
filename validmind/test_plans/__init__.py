"""
Test Plans entry point
"""
import inspect

import pandas as pd

from ..vm_models import Metric, TestPlan, ThresholdTest
from .binary_classifier import (
    BinaryClassifierMetrics,
    BinaryClassifierPerformance,
    BinaryClassifierDiagnosis,
)
from .tabular_datasets import (
    TabularDataQuality,
    TabularDatasetDescription,
    TimeSeriesDataQuality,
)
from .statsmodels_timeseries import (
    RegressionModelDescription,
    RegressionModelsEvaluation,
)
from .time_series import (
    TimeSeriesUnivariate,
    TimeSeriesMultivariate,
    TimeSeriesForecast,
    TimeSeriesSensitivity,
)

core_test_plans = {
    "binary_classifier_metrics": BinaryClassifierMetrics,
    "binary_classifier_validation": BinaryClassifierPerformance,
    "binary_classifier_model_diagnosis": BinaryClassifierDiagnosis,
    "tabular_dataset_description": TabularDatasetDescription,
    "tabular_data_quality": TabularDataQuality,
    "time_series_data_quality": TimeSeriesDataQuality,
    "time_series_univariate": TimeSeriesUnivariate,
    "time_series_multivariate": TimeSeriesMultivariate,
    "time_series_forecast": TimeSeriesForecast,
    "time_series_sensitivity": TimeSeriesSensitivity,
    "regression_model_description": RegressionModelDescription,
    "regression_models_evaluation": RegressionModelsEvaluation,
}

# These test plans can be added by the user
custom_test_plans = {}


def _get_all_test_plans():
    """
    Returns a dictionary of all test plans.

    Merge the core and custom test plans, with the custom plans
    taking precedence, i.e. allowing overriding of core test plans
    """
    return {**core_test_plans, **custom_test_plans}


def _get_test_plan_tests(test_plan):
    """
    Returns a list of all tests in a test plan. A test plan
    can have many test plans as well.
    """
    tests = set()
    for test in test_plan.tests:
        tests.add(test)

    for test_plan in test_plan.test_plans:
        tests.update(_get_test_plan_tests(test_plan))

    return tests


def _get_test_type(test):
    """
    Returns the test type by inspecting the test class hierarchy
    """
    if issubclass(test, Metric):
        return "Metric"
    elif issubclass(test, ThresholdTest):
        return "ThresholdTest"


def list_plans(pretty: bool = True):
    """
    Returns a list of all available test plans
    """

    all_test_plans = _get_all_test_plans()

    if not pretty:
        return list(all_test_plans.keys())

    table = []
    for name, test_plan in all_test_plans.items():
        table.append(
            {
                "ID": name,
                "Name": test_plan.__name__,
                "Description": test_plan.__doc__.strip(),
            }
        )

    return pd.DataFrame(table).style.hide(axis="index")


def list_tests(test_type: str = "all", pretty: bool = True):
    """
    Returns a list of all available tests.
    """
    all_test_plans = _get_all_test_plans()
    tests = set()
    for test_plan in all_test_plans.values():
        tests.update(_get_test_plan_tests(test_plan))

    # Sort by test type and then by name
    tests = sorted(tests, key=lambda test: f"{_get_test_type(test)} {test.__name__}")

    if not pretty:
        return tests

    table = []
    for test in tests:
        if inspect.isclass(test):
            test_type = _get_test_type(test)
            table.append(
                {
                    "Test Type": test_type,
                    "ID": test.name,
                    "Name": test.__name__,
                    "Description": test.__doc__.strip(),
                }
            )

    return pd.DataFrame(table).style.hide(axis="index")


def get_by_name(name: str):
    """
    Returns the test plan by name
    """
    all_test_plans = _get_all_test_plans()
    if name in all_test_plans:
        return all_test_plans[name]

    raise ValueError(f"Test plan with name: '{name}' not found")


def describe_plan(plan_id: str):
    """
    Returns a description of the test plan
    """
    plan = get_by_name(plan_id)
    tests = [f"{test.__name__} ({_get_test_type(test)})" for test in plan.tests]
    tests = ", ".join(tests)

    table = {
        "ID": plan.name,
        "Name": plan.__name__,
        "Description": plan.__doc__.strip(),
        "Required Context": plan.required_context,
        "Tests": tests,
    }

    return pd.DataFrame(table).style.hide(axis="index")


def register_test_plan(plan_id: str, plan: TestPlan):
    """
    Registers a custom test plan
    """
    custom_test_plans[plan_id] = plan
    print(f"Registered test plan: {plan_id}")


def describe_test(name: str):
    """
    Returns the test by name
    """
    all_test_plans = _get_all_test_plans()
    tests = set()
    for test_plan in all_test_plans.values():
        tests.update(_get_test_plan_tests(test_plan))

    # Sort by test type and then by name
    tests = sorted(tests, key=lambda test: f"{_get_test_type(test)} {test.__name__}")
    table = []
    for test in tests:
        if inspect.isclass(test):
            test_type = _get_test_type(test)

            if test.__name__ == name:
                table.append(
                    {
                        "Test Type": test_type,
                        "ID": test.name,
                        "Name": test.__name__,
                        "Description": test.__doc__.strip(),
                    }
                )

    return pd.DataFrame(table).style.hide(axis="index")
