# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from typing import List

import pandas as pd

from validmind.errors import MissingRequiredTestInputError
from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)

from .ai_powered_test import (
    call_model,
    get_explanation,
    get_score,
    missing_prompt_message,
)


@dataclass
class Conciseness(ThresholdTest):
    """
    Analyzes and grades the conciseness of prompts provided to a Large Language Model.

    ### Purpose

    The Conciseness Assessment is designed to evaluate the brevity and succinctness of prompts provided to a Language
    Learning Model (LLM). A concise prompt strikes a balance between offering clear instructions and eliminating
    redundant or unnecessary information, ensuring that the LLM receives relevant input without being overwhelmed.

    ### Test Mechanism

    Using an LLM, this test conducts a conciseness analysis on input prompts. The analysis grades the prompt on a scale
    from 1 to 10, where the grade reflects how well the prompt delivers clear instructions without being verbose.
    Prompts that score equal to or above a predefined threshold (default set to 7) are deemed successfully concise.
    This threshold can be adjusted to meet specific requirements.

    ### Signs of High Risk

    - Prompts that consistently score below the predefined threshold.
    - Prompts that are overly wordy or contain unnecessary information.
    - Prompts that create confusion or ambiguity due to excess or unnecessary information.

    ### Strengths

    - Ensures clarity and effectiveness of the prompts.
    - Promotes brevity and preciseness in prompts without sacrificing essential information.
    - Useful for models like LLMs, where input prompt length and clarity greatly influence model performance.
    - Provides a quantifiable measure of prompt conciseness.

    ### Limitations

    - The conciseness score is based on an AI's assessment, which might not fully capture human interpretation of
    conciseness.
    - The predefined threshold for conciseness could be subjective and might need adjustment based on application.
    - The test is dependent on the LLM’s understanding of conciseness, which might vary from model to model.
    """

    name = "conciseness"
    required_inputs = ["model.prompt"]
    default_params = {"min_threshold": 7}
    tasks = ["text_classification", "text_summarization"]
    tags = ["llm", "zero_shot", "few_shot"]

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

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
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
        if not hasattr(self.inputs.model, "prompt"):
            raise MissingRequiredTestInputError(missing_prompt_message)

        response = call_model(
            system_prompt=self.system_prompt,
            user_prompt=self.user_prompt.format(
                prompt_to_test=self.inputs.model.prompt.template
            ),
        )
        score = get_score(response)
        explanation = get_explanation(response)

        passed = score > self.params["min_threshold"]
        results = [
            ThresholdTestResult(
                passed=passed,
                values={
                    "score": score,
                    "explanation": explanation,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=passed)
