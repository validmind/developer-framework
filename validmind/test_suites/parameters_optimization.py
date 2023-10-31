# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Test suites for sklearn-compatible hyper parameters tunning

Ideal setup is to have the API client to read a
custom test suite from the project's configuration
"""

from validmind.vm_models import TestSuite


class KmeansParametersOptimization(TestSuite):
    """
    Test suite for sklearn hyperparameters optimization
    """

    suite_id = "hyper_parameters_optimization"
    tests = [
        "validmind.model_validation.sklearn.HyperParametersTuning",
        "validmind.model_validation.sklearn.KMeansClustersOptimization",
    ]
