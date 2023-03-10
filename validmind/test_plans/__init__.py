"""
Test Plans entry point
"""
import inspect

import tabulate

from ..data_validation import metrics as data_metrics
from ..data_validation import threshold_tests as data_threshold_tests
from ..model_validation.sklearn import metrics as sklearn_model_metrics
from ..model_validation.sklearn import (
    threshold_tests as sklearn_model_threshold_tests,
)
from .sklearn_classifier import (
    SKLearnClassifierMetrics,
    SKLearnClassifier,
    SKLearnClassifierPerformance,
)
from .tabular_datasets import (
    TabularDataset,
    TabularDataQuality,
    TabularDatasetDescription,
)
from .statsmodels_timeseries import (
    SesonalityTestPlan,
    StationarityTestPlan,
    TimeSeriesTestPlan,
)

core_test_plans = {
    "sklearn_classifier_metrics": SKLearnClassifierMetrics,
    "sklearn_classifier_validation": SKLearnClassifierPerformance,
    "sklearn_classifier": SKLearnClassifier,
    "tabular_dataset": TabularDataset,
    "tabular_dataset_description": TabularDatasetDescription,
    "tabular_data_quality": TabularDataQuality,
    "seasonality_test_plan": SesonalityTestPlan,
    "stationarity_test_plan": StationarityTestPlan,
    "timeseries_test_plan": TimeSeriesTestPlan,
}


def list_plans(pretty: bool = True):
    """
    Returns a list of all available test plans
    """
    if not pretty:
        return list(core_test_plans.keys())

    table = []
    for name, test_plan in core_test_plans.items():
        table.append(
            {
                "ID": name,
                "Name": test_plan.__name__,
                "Description": test_plan.__doc__.strip(),
            }
        )

    return tabulate.tabulate(table, headers="keys", tablefmt="html")


def list_tests(type: str = "all", pretty: bool = True):
    """
    Returns a list of all available tests
    """
    tests = []
    if type == "all" or type == "data":
        tests.extend(
            [
                test
                for _, test in inspect.getmembers(
                    data_metrics,
                    lambda m: inspect.getmodule(m) is data_metrics,
                )
            ]
        )
        tests.extend(
            [
                test
                for _, test in inspect.getmembers(
                    data_threshold_tests,
                    lambda m: inspect.getmodule(m) is data_threshold_tests,
                )
            ]
        )

    if type == "all" or type == "model":
        tests.extend(
            [
                test
                for _, test in inspect.getmembers(
                    sklearn_model_metrics,
                    lambda m: inspect.getmodule(m) is sklearn_model_metrics,
                )
            ]
        )
        tests.extend(
            [
                test
                for _, test in inspect.getmembers(
                    sklearn_model_threshold_tests,
                    lambda m: inspect.getmodule(m) is sklearn_model_threshold_tests,
                )
            ]
        )

    if not pretty:
        return tests

    table = []
    for test in tests:
        if inspect.isclass(test):
            test_type = _get_test_type(test)
            if test_type == "Metric":
                id = test.key
            else:
                id = test.name

            table.append(
                {
                    "Test Type": test_type,
                    "ID": id,
                    "Name": test.__name__,
                    "Description": test.__doc__.strip(),
                }
            )

    return tabulate.tabulate(table, headers="keys", tablefmt="html")


def get_by_name(name: str):
    """
    Returns the test plan by name
    """

    if name in core_test_plans:
        return core_test_plans[name]

    raise ValueError(f"Test plan with name: '{name}' not found")


def _get_test_type(test):
    """
    Returns the test type by inspecting the test class hierarchy
    """
    super_class = inspect.getmro(test)[1].__name__
    if super_class != "Metric" and super_class != "ThresholdTest":
        return "Custom Test"

    return super_class


def describe_plan(plan_id: str):
    """
    Returns a description of the test plan
    """
    plan = get_by_name(plan_id)
    tests = [f"{test.__name__} ({_get_test_type(test)})" for test in plan.tests]
    tests = ", ".join(tests)

    table = [
        ["ID", plan.name],
        ["Name", plan.__name__],
        ["Description", plan.__doc__.strip()],
        ["Required Context", plan.required_context],
        ["Tests", tests],
        ["Test Plans", [test_plan.name for test_plan in plan.test_plans]],
    ]

    return tabulate.tabulate(table, headers=["Attribute", "Value"], tablefmt="html")
