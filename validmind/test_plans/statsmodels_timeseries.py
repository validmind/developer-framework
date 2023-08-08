# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Time Series Test Plans from statsmodels
"""

from validmind.vm_models import TestPlan


class RegressionModelDescription(TestPlan):
    """
    Test plan for performance metric of regression model of statsmodels library
    """

    name = "regression_model_description"
    tests = [
        "validmind.data_validation.DatasetSplit",
        "validmind.model_validation.ModelMetadata",
    ]


class RegressionModelsEvaluation(TestPlan):
    """
    Test plan for metrics comparison of regression model of statsmodels library
    """

    name = "regression_models_evaluation"
    tests = [
        "validmind.model_validation.statsmodels.RegressionModelsCoeffs",
        "validmind.model_validation.statsmodels.RegressionModelsPerformance",
    ]
