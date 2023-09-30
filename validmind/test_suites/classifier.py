# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Test suites for sklearn-compatible classifier models

Ideal setup is to have the API client to read a
custom test plan from the project's configuration
"""

from validmind.vm_models import TestSuite


class ClassifierMetrics(TestSuite):
    """
    Test plan for sklearn classifier metrics
    """

    name = "classifier_metrics"
    tests = [
        "validmind.model_validation.ModelMetadata",
        "validmind.data_validation.DatasetSplit",
        "validmind.model_validation.sklearn.ConfusionMatrix",
        "validmind.model_validation.sklearn.ClassifierInSamplePerformance",
        "validmind.model_validation.sklearn.ClassifierOutOfSamplePerformance",
        "validmind.model_validation.sklearn.PermutationFeatureImportance",
        "validmind.model_validation.sklearn.PrecisionRecallCurve",
        "validmind.model_validation.sklearn.ROCCurve",
        "validmind.model_validation.sklearn.PopulationStabilityIndex",
        "validmind.model_validation.sklearn.SHAPGlobalImportance",
    ]


class ClassifierPerformance(TestSuite):
    """
    Test plan for sklearn classifier models
    """

    name = "classifier_validation"
    tests = [
        "validmind.model_validation.sklearn.MinimumAccuracy",
        "validmind.model_validation.sklearn.MinimumF1Score",
        "validmind.model_validation.sklearn.MinimumROCAUCScore",
        "validmind.model_validation.sklearn.TrainingTestDegradation",
        "validmind.model_validation.sklearn.ModelsPerformanceComparison",
    ]


class ClassifierDiagnosis(TestSuite):
    """
    Test plan for sklearn classifier model diagnosis tests
    """

    name = "classifier_model_diagnosis"
    tests = [
        "validmind.model_validation.sklearn.OverfitDiagnosis",
        "validmind.model_validation.sklearn.WeakspotsDiagnosis",
        "validmind.model_validation.sklearn.RobustnessDiagnosis",
    ]


class ClassifierModelValidation(TestSuite):
    """
    Test suite for binary classification models.
    """

    name = "classifier_model_validation"

    test_plans = [
        {
            "section_name": "Classifier Model Metrics",
            "section_description": "Metrics tests for classifier models",
            "section_tests": [
                "validmind.model_validation.ModelMetadata",
                "validmind.data_validation.DatasetSplit",
                "validmind.model_validation.sklearn.ConfusionMatrix",
                "validmind.model_validation.sklearn.ClassifierInSamplePerformance",
                "validmind.model_validation.sklearn.ClassifierOutOfSamplePerformance",
                "validmind.model_validation.sklearn.PermutationFeatureImportance",
                "validmind.model_validation.sklearn.PrecisionRecallCurve",
                "validmind.model_validation.sklearn.ROCCurve",
                "validmind.model_validation.sklearn.PopulationStabilityIndex",
                "validmind.model_validation.sklearn.SHAPGlobalImportance",
            ],
        },
        {
            "section_name": "Classifier Model Validation",
            "section_description": "Validation tests for classifier models",
            "section_tests": [
                "validmind.model_validation.sklearn.MinimumAccuracy",
                "validmind.model_validation.sklearn.MinimumF1Score",
                "validmind.model_validation.sklearn.MinimumROCAUCScore",
                "validmind.model_validation.sklearn.TrainingTestDegradation",
                "validmind.model_validation.sklearn.ModelsPerformanceComparison",
            ],
        },
        {
            "section_name": "Classifier Model Diagnosis",
            "section_description": "Diagnosis tests for classifier models",
            "section_tests": [
                "validmind.model_validation.sklearn.OverfitDiagnosis",
                "validmind.model_validation.sklearn.WeakspotsDiagnosis",
                "validmind.model_validation.sklearn.RobustnessDiagnosis",
            ],
        },
    ]


class ClassifierFullSuite(TestSuite):
    """
    Full test suite for binary classification models.
    """

    name = "classifier_full_suite"

    tests = [
        "tabular_dataset_description",
        "tabular_data_quality",
        {
            "section_name": "Classifier Model Metrics",
            "section_description": "Metrics tests for classifier models",
            "section_tests": [
                "validmind.model_validation.ModelMetadata",
                "validmind.data_validation.DatasetSplit",
                "validmind.model_validation.sklearn.ConfusionMatrix",
                "validmind.model_validation.sklearn.ClassifierInSamplePerformance",
                "validmind.model_validation.sklearn.ClassifierOutOfSamplePerformance",
                "validmind.model_validation.sklearn.PermutationFeatureImportance",
                "validmind.model_validation.sklearn.PrecisionRecallCurve",
                "validmind.model_validation.sklearn.ROCCurve",
                "validmind.model_validation.sklearn.PopulationStabilityIndex",
                "validmind.model_validation.sklearn.SHAPGlobalImportance",
            ],
        },
        {
            "section_name": "Classifier Model Validation",
            "section_description": "Validation tests for classifier models",
            "section_tests": [
                "validmind.model_validation.sklearn.MinimumAccuracy",
                "validmind.model_validation.sklearn.MinimumF1Score",
                "validmind.model_validation.sklearn.MinimumROCAUCScore",
                "validmind.model_validation.sklearn.TrainingTestDegradation",
                "validmind.model_validation.sklearn.ModelsPerformanceComparison",
            ],
        },
        {
            "section_name": "Classifier Model Diagnosis",
            "section_description": "Diagnosis tests for classifier models",
            "section_tests": [
                "validmind.model_validation.sklearn.OverfitDiagnosis",
                "validmind.model_validation.sklearn.WeakspotsDiagnosis",
                "validmind.model_validation.sklearn.RobustnessDiagnosis",
            ],
        },
    ]
