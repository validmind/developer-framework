# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

import pandas as pd

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
    Test that the prompt is concise
    """

    category = "prompt_validation"
    name = "robustness"
    required_inputs = ["prompt", "model"]

    system_prompt = """
You are a prompt evaluation researcher AI. LLM prompts are used to guide a model to generate specific outputs or solve specific tasks. These prompts can be more or less robust, meaning that they can be more or less susceptible to breaking especially when the output needs to be a sepecific type.

Consider the prompt that will be submitted and generate 10 test inputs that can be used to evaluate the robustness of the prompt.
The test inputs should be valid inputs but should be designed to try and break the output.
Common strategies to use include contradictions, edge cases, typos, etc.

For example:
Give this prompt, "Anlyse the following code and rate its complexity with a score from 1 to 10\n\n{{input_code}}", a good test would be to input something other than valid code and see if the model still generates a score.
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
        result = results[0]
        results_table = [
            {
                "Test Input": result.values["input"],
                "Model Output": result.values["output"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
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

        for test_input in response.split("\n"):
            result = self.model.predict(test_input)

            fail = False
            if result not in self.model.classes:
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
