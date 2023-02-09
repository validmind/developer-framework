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
        CharacteristicStabilityIndex,
        PopulationStabilityIndex,
    ]


# metrics = [
#     precision_score,
#     recall_score,
#     roc_auc_score,
#     roc_curve,
#     precision_recall_curve,
#     shap_global_importance,
# ]
