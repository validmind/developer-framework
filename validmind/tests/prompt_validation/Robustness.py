# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

import pandas as pd

from validmind.errors import SkipTestError
from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
)

from .ai_powered_test import AIPoweredTest


@dataclass
class Robustness(ThresholdTest, AIPoweredTest):
    """
    **Purpose:**
    The Robustness Integrity Assessment evaluates the resilience and reliability of prompts
    provided to a Language Learning Model (LLM). The primary objective is to ensure that prompts
    consistently produce accurate and desired outputs, even in diverse or challenging scenarios.

    **Test Mechanism:**
    Prompts are subjected to various conditions, alterations, and contexts to check their stability
    in eliciting consistent responses from the LLM. Factors such as different phrasings,
    inclusion of potential distractors, and varied input complexities are introduced to test the robustness of the prompt.

    **Why Robustness Matters:**
    A robust prompt ensures consistent performance and reduces the likelihood of unexpected or
    off-tangent outputs. This consistency is vital for applications where predictability and
    reliability of the LLM's response are paramount.
    """

    category = "prompt_validation"
    name = "robustness"
    required_inputs = ["model"]

    system_prompt = """
You are a prompt evaluation researcher AI. LLM prompts are used to guide a model to generate specific outputs or solve specific tasks. These prompts can be more or less robust, meaning that they can be more or less susceptible to breaking especially when the output needs to be a specific type.

Consider the prompt that will be submitted and generate 10 test inputs that can be used to evaluate the robustness of the prompt.
The test inputs should be valid inputs but should be designed to try and break the output.
Common strategies to use include contradictions, edge cases, typos, and any method that can force the model to generate an incorrect output.

For example:
Give this prompt, "Analyse the following code and rate its complexity with a score from 1 to 10\n\n{{input_code}}", a good test would be to input something other than valid code and see if the model still generates a score.
""".strip()
    user_prompt = '''
Return 10 test inputs separated by a new line
Do not include quotes around the inputs
Prompt:
"""
{prompt_to_test}
"""
'''.strip()

    def summary(self, results: List[TestResult], all_passed: bool):
        results_table = [
            {
                "Test Input": result.values["input"],
                "Model Output": result.values["output"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pd.DataFrame(results_table),
                    metadata=ResultTableMetadata(
                        title="Robustness Test on Prompt",
                    ),
                )
            ]
        )

    def run(self):
        response = self.call_model(
            system_prompt=self.system_prompt,
            user_prompt=self.user_prompt.format(prompt_to_test=self.model.prompt),
        )

        results = []
        target_class_labels = self.model.test_ds.target_classes()

        # Guard against too many classes (maybe not a classification model)
        if len(target_class_labels) > 10:
            raise SkipTestError(
                "Too many target classes to test robustness. Skipping test."
            )

        for test_input in response.split("\n"):
            test_input_df = pd.DataFrame(
                [test_input], columns=[self.model.test_ds.text_column]
            )
            result = self.model.predict(test_input_df)[0]

            fail = False
            if result not in target_class_labels:
                fail = True

            results.append(
                TestResult(
                    passed=not fail,
                    values={
                        "input": test_input,
                        "output": result,
                    },
                )
            )

        return self.cache_results(
            results, passed=all([result.passed for result in results])
        )
