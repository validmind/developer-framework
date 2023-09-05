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
class Conciseness(ThresholdTest, AIPoweredTest):
    """
    Test that the prompt is concise
    """

    category = "prompt_validation"
    name = "conciseness"
    required_inputs = ["prompt"]
    default_params = {"min_threshold": 7}

    system_prompt = """
You are a prompt evaluation AI. You are aware of all prompt engineering best practices and can score prompts based on how well they satisfy different metrics. You also can provide general feedback for the prompt.

Best practices for LLM prompt engineering suggest that prompts should be concise and precise and avoid "fluffy" language.

For example this:
"The description for this product should be fairly short, a few sentences only, and not too much more."
could be better written as:
"Use a 3 to 5 sentence paragraph to describe this product."

With that in mind, score the submitted prompt on a scale of 1 to 10, with 10 being the best possible score. Provide an explanation for your score.

Example Response:

Score: 4
Explanation: The prompt uses many "fluff" words that could potentially confuse the model and reduce the precision of the result. Use more concise language to improve the prompt.
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
                        title="Conciseness Test on Prompt",
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
