"""
Test plan for tabular datasets

Ideal setup is to have the API client to read a
custom test plan from the project's configuration
"""

from ..vm_models import TestPlan
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


class SKLearnClassifierMetricsTestPlan(TestPlan):
    """
    Test plan for sklearn classifier metrics
    """

    name = "sklearn_classifier_metrics"
    required_context = ["model", "train_ds", "test_ds"]
    tests = [
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
