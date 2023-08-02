# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Test plan for text datasets

Ideal setup is to have the API client to read a
custom test plan from the project's configuration
"""

from validmind.vm_models import TestPlan


class TextDataQuality(TestPlan):
    """
    Test plan for data quality on text data
    """

    name = "text_data_quality"
    tests = [
        "validmind.data_validation.nlp.ClassImbalance",
        "validmind.data_validation.nlp.Duplicates",
        "validmind.data_validation.nlp.StopWords",
        "validmind.data_validation.nlp.Punctuations",
        "validmind.data_validation.nlp.Mentions",
        "validmind.data_validation.nlp.Hashtags",
        "validmind.data_validation.nlp.CommonWords",
    ]
