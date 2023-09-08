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
    **Purpose:**
    The Conciseness Assessment is designed to evaluate the brevity and succinctness of prompts
    provided to a Language Learning Model (LLM). A concise prompt strikes a balance between
    offering clear instructions and eliminating redundant or unnecessary information, ensuring that
    the LLM receives relevant input without being overwhelmed.

    **Test Mechanism:**
    Using an LLM, this test puts input prompts through a conciseness analysis where it's graded
    on a scale from 1 to 10. The grade reflects how well the prompt maintains clarity while
    avoiding verbosity. Prompts that achieve a grade equal to or surpassing a predefined threshold
    (default set to 7) are considered successful in being concise. This threshold can be adjusted
    based on specific requirements.

    **Why Conciseness Matters:**
    While detailed prompts can guide an LLM towards accurate results, excessive details can clutter
    the instruction and potentially lead to undesired outputs. Concise prompts are straightforward,
    reducing ambiguity and focusing the LLM's attention on the primary task. This is especially
    important considering there are limitations to the length of prompts that can be fed to an
    LLM.

    **Example:**
    For an LLM tasked with summarizing a document, a verbose prompt might introduce unnecessary
    constraints or biases. A concise, effective prompt like, "Provide a brief summary highlighting
    the main points of the document" ensures that the LLM captures the essence of the content
    without being sidetracked.
    """

    category = "prompt_validation"
    name = "conciseness"
    required_inputs = ["model.prompt"]
    default_params = {"min_threshold": 7}

    system_prompt = """
You are a prompt evaluation AI. You are aware of all prompt engineering best practices and can score prompts based on how well they satisfy different metrics. You analyse the prompts step-by-step based on provided documentation and provide a score and an explanation for how you produced that score.

Consider the following documentation regarding conciseness in prompts and utilize it to grade the user-submitted prompt:
'''
While detailed prompts can guide an LLM towards accurate results, excessive details can clutter the instruction and potentially lead to undesired outputs. Concise prompts are straightforward, reducing ambiguity and focusing the LLM's attention on the primary task. This is especially important considering there are limitations to the length of prompts that can be fed to an LLM.

For an LLM tasked with summarizing a document, a verbose prompt might introduce unnecessary constraints or biases. A concise, effective prompt like:
"Provide a brief summary highlighting the main points of the document"
ensures that the LLM captures the essence of the content without being sidetracked.

For example this prompt:
"The description for this product should be fairly short, a few sentences only, and not too much more."
could be better written like this:
"Use a 3 to 5 sentence paragraph to describe this product."
'''

Score the user-submitted prompt on a scale of 1 to 10, with 10 being the best possible score. Provide an explanation for your score.

Response Format:
```
Score: <score>
Explanation: <explanation>
```
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
                "Explanation": result.values["explanation"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pd.DataFrame(results_table),
                    metadata=ResultTableMetadata(
                        title="Conciseness Test for LLM Prompt",
                    ),
                )
            ]
        )

    def run(self):
        response = self.call_model(
            system_prompt=self.system_prompt,
            user_prompt=self.user_prompt.format(prompt_to_test=self.model.prompt),
        )
        score = self.get_score(response)
        explanation = self.get_explanation(response)

        passed = score > self.params["min_threshold"]
        results = [
            TestResult(
                passed=passed,
                values={
                    "score": score,
                    "explanation": explanation,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=passed)
