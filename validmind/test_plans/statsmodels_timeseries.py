"""
Time Series Test Plans from statsmodels
"""

from validmind.vm_models import TestPlan


class RegressionModelDescription(TestPlan):
    """
    Test plan for performance metric of regression model of statsmodels library
    """

    name = "regression_model_description"
    required_context = ["model"]
    tests = [
        "validmind.data_validation.DatasetSplit",
        "validmind.model_validation.ModelMetadata",
    ]


class RegressionModelsEvaluation(TestPlan):
    """
    Test plan for metrics comparison of regression model of statsmodels library
    """

    name = "regression_models_evaluation"
    required_context = ["models", "model"]
    tests = [
        "validmind.model_validation.statsmodels.RegressionModelsCoeffs",
        "validmind.model_validation.statsmodels.RegressionModelsPerformance",
    ]
