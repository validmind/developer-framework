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
class Clarity(ThresholdTest, AIPoweredTest):
    """
    Test that the prompt is clear
    """

    category = "prompt_validation"
    name = "clarity"
    required_inputs = ["prompt"]
    default_params = {"min_threshold": 7}

    system_prompt = """
You are a prompt evaluation AI. You are aware of all prompt engineering best practices and can score prompts based on how well they satisfy different metrics. You also can provide general feedback for the prompt.

Score the clarity of the following prompt. Return a score from 0 to 10 where 0 is not clear at all and 10 is very clear. Also provide a short explanation for your score.'

Example Response:

Score: 2
Explanation: This prompt is not very clear. It leaves a lot of room for interpretation on the part of the model and will most likely result in poor responses. To improve this prompt, add more details about what you want the model to do.

(Note: this example is itself not very clear. In your response, you should be more specific about what details to add.)
""".strip()
    user_prompt = '''
Prompt:
"""
{prompt_to_test}
"""
'''.strip()

    def summary(self, results: List[TestResult], all_passed: bool):
        result = results[0]
        results_table = [
            {
                "Score": result.values["score"],
                "Threshold": result.values["threshold"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pd.DataFrame(results_table),
                    metadata=ResultTableMetadata(
                        title="Clarity Test on Prompt",
                    ),
                )
            ]
        )

    def run(self):
        response = self.call_model(
            system_prompt=self.system_prompt,
            user_prompt=self.user_prompt.format(prompt_to_test=self.prompt),
        )
        score = self.get_score(response)

        passed = score > self.params["min_threshold"]
        results = [
            TestResult(
                passed=passed,
                values={
                    "score": score,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=passed)
