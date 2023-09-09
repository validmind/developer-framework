# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Test plan for LLMs
"""

from validmind.vm_models import TestPlan


class PromptValidation(TestPlan):
    """
    Test plan for prompt validation
    """

    name = "prompt_validation"
    tests = [
        "validmind.prompt_validation.Bias",
        "validmind.prompt_validation.Clarity",
        "validmind.prompt_validation.Conciseness",
        "validmind.prompt_validation.Delimitation",
        "validmind.prompt_validation.NegativeInstruction",
        "validmind.prompt_validation.Robustness",
        "validmind.prompt_validation.Specificity",
    ]
