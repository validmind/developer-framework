"""
Test plan for sklearn classifier models

Ideal setup is to have the API client to read a
custom test plan from the project's configuration
"""

from ..vm_models import TestPlan
from ..model_validation.model_metadata import ModelMetadata
from ..model_validation.sklearn.metrics import (
    AccuracyScore,
    ConfusionMatrix,
    F1Score,
    PermutationFeatureImportance,
    PrecisionRecallCurve,
    PrecisionScore,
    RecallScore,
    ROCAUCScore,
    ROCCurve,
    CharacteristicStabilityIndex,
    PopulationStabilityIndex,
    SHAPGlobalImportance,
)
from ..model_validation.sklearn.threshold_tests import (
    MinimumAccuracy,
    MinimumF1Score,
    MinimumROCAUCScore,
    TrainingTestDegradation,
    OverfitDiagnosis,
    WeakspotsDiagnosis,
    RobustnessDiagnosis,
)


class SKLearnClassifierMetrics(TestPlan):
    """
    Test plan for sklearn classifier metrics
    """

    name = "sklearn_classifier_metrics"
    required_context = ["model", "train_ds", "test_ds"]
    tests = [
        ModelMetadata,
        AccuracyScore,
        ConfusionMatrix,
        F1Score,
        PermutationFeatureImportance,
        PrecisionRecallCurve,
        PrecisionScore,
        RecallScore,
        ROCAUCScore,
        ROCCurve,
        CharacteristicStabilityIndex,
        PopulationStabilityIndex,
        SHAPGlobalImportance,
    ]


class SKLearnClassifierPerformance(TestPlan):
    """
    Test plan for sklearn classifier models
    """

    name = "sklearn_classifier_validation"
    required_context = ["model", "train_ds", "test_ds"]
    tests = [
        MinimumAccuracy,
        MinimumF1Score,
        MinimumROCAUCScore,
        TrainingTestDegradation,
    ]


class SKLearnClassifierDiagnosis(TestPlan):
    """
    Test plan for sklearn classifier model diagnosis tests
    """

    name = "sklearn_classifier_model_diagnosis"
    required_context = ["model", "train_ds", "test_ds"]
    tests = [OverfitDiagnosis, WeakspotsDiagnosis, RobustnessDiagnosis]


class SKLearnClassifier(TestPlan):
    """
    Test plan for sklearn classifier models that includes
    both metrics and validation tests
    """

    name = "sklearn_classifier"
    required_context = ["model", "train_ds", "test_ds"]
    test_plans = [
        SKLearnClassifierMetrics,
        SKLearnClassifierPerformance,
        SKLearnClassifierDiagnosis,
    ]
