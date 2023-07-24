# This software is proprietary and confidential. Unauthorized copying,
# modification, distribution or use of this software is strictly prohibited.
# Please refer to the LICENSE file in the root directory of this repository
# for more information.
#
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
    required_context = ["dataset"]

    test_plans = [
        "tabular_dataset_description",
        "tabular_data_quality",
    ]


class BinaryClassifierModelValidation(TestSuite):
    """
    Test suite for binary classification models.
    """

    name = "binary_classifier_model_validation"
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

    name = "binary_classifier_full_suite"
    required_context = ["dataset", "model"]

    test_plans = [
        "tabular_dataset_description",
        "tabular_data_quality",
        "binary_classifier_metrics",
        "binary_classifier_validation",
        "binary_classifier_model_diagnosis",
    ]


class TimeSeriesDataset(TestSuite):
    """
    Test suite for time series datasets.
    """

    name = "time_series_dataset"
    required_context = ["dataset"]

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
    required_context = ["model", "models"]

    test_plans = [
        "regression_model_description",
        "regression_models_evaluation",
        "time_series_forecast",
        "time_series_sensitivity",
    ]
