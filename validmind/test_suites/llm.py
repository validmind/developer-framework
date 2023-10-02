# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Test suites for LLMs
"""

from validmind.vm_models import TestSuite

from .classifier import ClassifierMetrics, ClassifierValidation
from .text_data import TextDataQuality


class PromptValidation(TestSuite):
    """
    Test suite for prompt validation
    """

    suite_id = "prompt_validation"
    tests = [
        "validmind.prompt_validation.Bias",
        "validmind.prompt_validation.Clarity",
        "validmind.prompt_validation.Conciseness",
        "validmind.prompt_validation.Delimitation",
        "validmind.prompt_validation.NegativeInstruction",
        "validmind.prompt_validation.Robustness",
        "validmind.prompt_validation.Specificity",
    ]


class LLMClassifierFullSuite(TestSuite):
    """
    Full test suite for LLM classification models.
    """

    suite_id = "llm_classifier_full_suite"
    tests = [
        {
            "section_id": TextDataQuality.suite_id,
            "section_description": TextDataQuality.__doc__,
            "section_tests": TextDataQuality.tests,
        },
        {
            "section_id": ClassifierMetrics.suite_id,
            "section_description": ClassifierMetrics.__doc__,
            "section_tests": ClassifierMetrics.tests,
        },
        {
            "section_id": ClassifierValidation.suite_id,
            "section_description": ClassifierValidation.__doc__,
            "section_tests": ClassifierValidation.tests,
        },
        {
            "section_id": PromptValidation.suite_id,
            "section_description": PromptValidation.__doc__,
            "section_tests": PromptValidation.tests,
        },
    ]
