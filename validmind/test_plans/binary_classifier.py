"""
Test plan for sklearn classifier models

Ideal setup is to have the API client to read a
custom test plan from the project's configuration
"""

from ..vm_models import TestPlan
from ..data_validation.metrics import DatasetSplit
from ..model_validation.model_metadata import ModelMetadata
from ..model_validation.sklearn.metrics import (
    ClassifierInSamplePerformance,
    ClassifierOutOfSamplePerformance,
    ConfusionMatrix,
    PermutationFeatureImportance,
    PrecisionRecallCurve,
    ROCCurve,
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


class BinaryClassifierMetrics(TestPlan):
    """
    Test plan for sklearn classifier metrics
    """

    name = "binary_classifier_metrics"
    required_context = ["model"]
    tests = [
        ModelMetadata,
        DatasetSplit,
        ConfusionMatrix,
        ClassifierInSamplePerformance,
        ClassifierOutOfSamplePerformance,
        PermutationFeatureImportance,
        PrecisionRecallCurve,
        ROCCurve,
        PopulationStabilityIndex,
        SHAPGlobalImportance,
    ]


class BinaryClassifierPerformance(TestPlan):
    """
    Test plan for sklearn classifier models
    """

    name = "binary_classifier_validation"
    required_context = ["model"]
    tests = [
        MinimumAccuracy,
        MinimumF1Score,
        MinimumROCAUCScore,
        TrainingTestDegradation,
    ]


class BinaryClassifierDiagnosis(TestPlan):
    """
    Test plan for sklearn classifier model diagnosis tests
    """

    name = "binary_classifier_model_diagnosis"
    required_context = ["model"]
    tests = [
        OverfitDiagnosis,
        WeakspotsDiagnosis,
        RobustnessDiagnosis,
    ]
