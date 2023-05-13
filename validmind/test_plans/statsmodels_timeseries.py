"""
Time Series Test Plans from statsmodels
"""

from ..vm_models import TestPlan
from ..model_validation.statsmodels.metrics import (
    RegressionModelSummary,
    RegressionModelOutsampleComparison,
    RegressionModelInsampleComparison,
)


class RegressionModelPerformance(TestPlan):
    """
    Test plan for performance metric of regression model of statsmodels library
    """

    name = "regression_model_performance"
    required_context = ["model"]
    tests = [RegressionModelSummary]


class RegressionModelsComparison(TestPlan):
    """
    Test plan for metrics comparison of regression model of statsmodels library
    """

    name = "regression_models_comparison"
    required_context = ["models", "model"]
    tests = [RegressionModelInsampleComparison, RegressionModelOutsampleComparison]
