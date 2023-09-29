# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Test plan for sklearn classifier models

Ideal setup is to have the API client to read a
custom test plan from the project's configuration
"""

from validmind.vm_models import TestPlan


class SummarizationMetrics(TestPlan):
    """
    Test plan for Summarization metrics
    """

    name = "summarization_metrics"
    tests = [
        "validmind.model_validation.RougeMetrics",
        "validmind.model_validation.TokenDisparity",
        "validmind.model_validation.BleuScore",
        "validmind.model_validation.BertScore",
        "validmind.model_validation.ContextualRecall",
        "validmind.model_validation.ToxicityHistogram",
    ]
