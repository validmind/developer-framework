# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Default test suites provided by the developer framework.
"""

from ..vm_models import TestSuite


class TabularDataset(TestSuite):
    """
    Test suite for tabular datasets.
    """

    name = "tabular_dataset"

    test_plans = [
        "tabular_dataset_description",
        "tabular_data_quality",
    ]


class ClassifierModelValidation(TestSuite):
    """
    Test suite for binary classification models.
    """

    name = "classifier_model_validation"

    test_plans = [
        "classifier_metrics",
        "classifier_validation",
        "classifier_model_diagnosis",
    ]


class ClassifierFullSuite(TestSuite):
    """
    Full test suite for binary classification models.
    """

    name = "classifier_full_suite"

    test_plans = [
        "tabular_dataset_description",
        "tabular_data_quality",
        "classifier_metrics",
        "classifier_validation",
        "classifier_model_diagnosis",
    ]


class TimeSeriesDataset(TestSuite):
    """
    Test suite for time series datasets.
    """

    name = "time_series_dataset"

    test_plans = [
        "time_series_data_quality",
        "time_series_univariate",
        "time_series_multivariate",
    ]


class TimeSeriesModelValidation(TestSuite):
    """
    Test suite for time series model validation.
    """

    name = "time_series_model_validation"

    test_plans = [
        "regression_model_description",
        "regression_models_evaluation",
        "time_series_forecast",
        "time_series_sensitivity",
    ]


class NLPClassifierFullSuite(TestSuite):
    """
    Full test suite for NLP classification models.
    """

    name = "nlp_classifier_full_suite"

    test_plans = [
        "text_data_quality",
        "classifier_metrics",
        "classifier_validation",
        "classifier_model_diagnosis",
    ]


class LLMClassifierFullSuite(TestSuite):
    """
    Full test suite for LLM classification models.
    """

    name = "llm_classifier_full_suite"

    test_plans = [
        "text_data_quality",
        "classifier_metrics",
        "classifier_validation",
        "prompt_validation",
    ]
