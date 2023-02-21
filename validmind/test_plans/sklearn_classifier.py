"""
Test plan for tabular datasets

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
)
from ..model_validation.sklearn.threshold_tests import (
    AccuracyTest,
    F1ScoreTest,
    ROCAUCScoreTest,
    TrainingTestDegradationTest,
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
    ]


class SKLearnClassifierPerformance(TestPlan):
    """
    Test plan for sklearn classifier models
    """

    name = "sklearn_classifier_validation"
    required_context = ["model", "train_ds", "test_ds"]
    tests = [AccuracyTest, F1ScoreTest, ROCAUCScoreTest, TrainingTestDegradationTest]


class SKLearnClassifier(TestPlan):
    """
    Test plan for sklearn classifier models that includes
    both metrics and validation tests
    """

    name = "sklearn_classifier"
    required_context = ["model", "train_ds", "test_ds"]
    test_plans = [SKLearnClassifierMetrics, SKLearnClassifierPerformance]
