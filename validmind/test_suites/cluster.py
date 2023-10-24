# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Test suites for sklearn-compatible clustering models

Ideal setup is to have the API client to read a
custom test suite from the project's configuration
"""

from validmind.vm_models import TestSuite


class ClusterMetrics(TestSuite):
    """
    Test suite for sklearn clustering metrics
    """

    suite_id = "cluster_metrics"
    tests = [
        "validmind.model_validation.sklearn.ClusterPerformance",
        "validmind.model_validation.sklearn.ClusterCosineSimilarity",
    ]
