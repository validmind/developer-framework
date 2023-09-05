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
class Escape(ThresholdTest, AIPoweredTest):
    """
    Test that the prompt is escaped properly
    """

    category = "prompt_validation"
    name = "escape"
    required_inputs = ["prompt"]
    default_params = {"min_threshold": 7}

    system_prompt = """
You are a prompt evaluation AI. You are aware of all prompt engineering best practices and can score prompts based on how well they satisfy different metrics. You also can provide general feedback for the prompt.

LLM Prompts that include different sections and user inputs should be properly escaped. Ideally, the prompt should use triple quotes or backticks or at least single quotes around any user input or code block etc.
This is to ensure that the prompt is parsed correctly by the model and that the user input is not interpreted as part of the prompt.
Identify any issues in the submitted prompt and give a score from 1 to® 10 based on the number and severity of issues.

Example Response:

Score: 7
Explanation: The prompt is properly escaped for the most part. However, best practices suggest that the user input should be enclosed in triple quotes or backticks instead of single quotes.
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
                        title="Escape Test on Prompt",
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
