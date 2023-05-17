"""
Time Series Test Plans from statsmodels
"""

from ..vm_models import TestPlan
from ..data_validation.metrics import DatasetSplit
from ..model_validation.model_metadata import ModelMetadata
from ..model_validation.statsmodels.metrics import (
    RegressionModelsCoeffs,
    RegressionModelsPerformance,
)


class RegressionModelDescription(TestPlan):
    """
    Test plan for performance metric of regression model of statsmodels library
    """

    name = "regression_model_description"
    required_context = ["model"]
    tests = [DatasetSplit, ModelMetadata]


class RegressionModelsEvaluation(TestPlan):
    """
    Test plan for metrics comparison of regression model of statsmodels library
    """

    name = "regression_models_evaluation"
    required_context = ["models", "model"]
    tests = [
        RegressionModelsCoeffs,
        RegressionModelsPerformance,
    ]
