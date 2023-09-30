# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Entrypoint for test suites.
"""
import pandas as pd

from ..logging import get_logger
from ..tests import load_test
from ..utils import format_dataframe
from ..vm_models import TestSuite
from .test_suites import (
    ClassifierFullSuite,
    ClassifierModelValidation,
    LLMClassifierFullSuite,
    NLPClassifierFullSuite,
    TabularDataset,
    TimeSeriesDataset,
    TimeSeriesModelValidation,
)

logger = get_logger(__name__)

core_test_suites = {
    "classifier_full_suite": ClassifierFullSuite,
    "classifier_model_validation": ClassifierModelValidation,
    "llm_classifier_full_suite": LLMClassifierFullSuite,
    "nlp_classifier_full_suite": NLPClassifierFullSuite,
    "tabular_dataset": TabularDataset,
    "time_series_dataset": TimeSeriesDataset,
    "time_series_model_validation": TimeSeriesModelValidation,
    "classifier_metrics": ClassifierMetrics,
    "classifier_validation": ClassifierPerformance,
    "classifier_model_diagnosis": ClassifierDiagnosis,
    "prompt_validation": PromptValidation,
    "tabular_dataset_description": TabularDatasetDescription,
    "tabular_data_quality": TabularDataQuality,
    "time_series_data_quality": TimeSeriesDataQuality,
    "time_series_univariate": TimeSeriesUnivariate,
    "time_series_multivariate": TimeSeriesMultivariate,
    "time_series_forecast": TimeSeriesForecast,
    "time_series_sensitivity": TimeSeriesSensitivity,
    "regression_model_description": RegressionModelDescription,
    "regression_models_evaluation": RegressionModelsEvaluation,
    "text_data_quality": TextDataQuality,
    "summarization_metrics": SummarizationMetrics,
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

    tests = []

    for item in test_suite.tests:
        if isinstance(item, str):
            test = load_test(item)
            tests.append(
                {
                    "Test Suite ID": test_suite_id,
                    "Test Suite Name": test_suite.__name__,
                    "Test Suite Section": "",
                    "Test ID": test_id,
                    "Test Name": test.__name__,
                    "Test Type": test.test_type,
                }
            )
        elif isinstance(item, dict):
            for test_id in item["section_tests"]:
                test = load_test(item)
                tests.append(
                    {
                        "Test Suite ID": test_suite_id,
                        "Test Suite Name": test_suite.__name__,
                        "Test Suite Section": item["section_name"],
                        "Test ID": test_id,
                        "Test Name": test.__name__,
                        "Test Type": test.test_type,
                    }
                )
        else:
            raise ValueError(f"Invalid test suite item: {item}")

    return format_dataframe(pd.DataFrame(tests).reset_index(drop=True))


# TODO: remove this... here for backwards compatibility
describe_test_suite = describe_suite


def register_test_suite(suite_id: str, suite: TestSuite):
    """
    Registers a custom test suite
    """
    custom_test_suites[suite_id] = suite
    logger.info(f"Registered test suite: {suite_id}")
