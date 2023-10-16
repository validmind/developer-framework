# Copyright © 2023 ValidMind Inc. All rights reserved.
from validmind.vm_models import TestSuite

from .tabular_datasets import TabularDataQuality, TabularDatasetDescription


class RegressionMetrics(TestSuite):
    """
    Test suite for performance metrics of regression metrics
    """

    suite_id = "regression_metrics"
    tests = [
        "validmind.data_validation.DatasetSplit",
        "validmind.model_validation.ModelMetadata",
        "validmind.model_validation.sklearn.PermutationFeatureImportance",
    ]


class RegressionPerformance(TestSuite):
    """
    Test suite for regression model performance
    """

    suite_id = "regression_performance"
    tests = [
        "validmind.model_validation.sklearn.RegressionErrors",
        "validmind.model_validation.sklearn.RegressionR2Square",
    ]


class RegressionModelsComparison(TestSuite):
    """
    Test suite for regression models performance comparison
    """

    suite_id = "regression_models_comparison"
    tests = [
        "validmind.model_validation.sklearn.RegressionModelsPerformanceComparison",
    ]


class RegressionFullSuite(TestSuite):
    """
    Full test suite for regression models.
    """

    suite_id = "regression_full_suite"
    tests = [
        {
            "section_id": TabularDatasetDescription.suite_id,
            "section_description": TabularDatasetDescription.__doc__,
            "section_tests": TabularDatasetDescription.tests,
        },
        {
            "section_id": TabularDataQuality.suite_id,
            "section_description": TabularDataQuality.__doc__,
            "section_tests": TabularDataQuality.tests,
        },
        {
            "section_id": RegressionMetrics.suite_id,
            "section_description": RegressionMetrics.__doc__,
            "section_tests": RegressionMetrics.tests,
        },
        {
            "section_id": RegressionPerformance.suite_id,
            "section_description": RegressionPerformance.__doc__,
            "section_tests": RegressionPerformance.tests,
        },
        {
            "section_id": RegressionModelsComparison.suite_id,
            "section_description": RegressionModelsComparison.__doc__,
            "section_tests": RegressionModelsComparison.tests,
        },
    ]
