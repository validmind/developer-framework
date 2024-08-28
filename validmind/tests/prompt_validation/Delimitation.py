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
class Delimitation(ThresholdTest):
    """
    Evaluates the proper use of delimiters in prompts provided to Large Language Models.

    ### Purpose

    The Delimitation Test aims to assess whether prompts provided to the Language Learning Model (LLM) correctly use
    delimiters to mark different sections of the input. Well-delimited prompts help simplify the interpretation process
    for the LLM, ensuring that the responses are precise and accurate.

    ### Test Mechanism

    The test employs an LLM to examine prompts for appropriate use of delimiters such as triple quotation marks, XML
    tags, and section titles. Each prompt is assigned a score from 1 to 10 based on its delimitation integrity. Prompts
    with scores equal to or above the preset threshold (which is 7 by default, although it can be adjusted as
    necessary) pass the test.

    ### Signs of High Risk

    - Prompts missing, improperly placed, or incorrectly used delimiters, leading to misinterpretation by the LLM.
    - High-risk scenarios with complex prompts involving multiple tasks or diverse data where correct delimitation is
    crucial.
    - Scores below the threshold, indicating a high risk.

    ### Strengths

    - Ensures clarity in demarcating different components of given prompts.
    - Reduces ambiguity in understanding prompts, especially for complex tasks.
    - Provides a quantified insight into the appropriateness of delimiter usage, aiding continuous improvement.

    ### Limitations

    - Only checks for the presence and placement of delimiters, not whether the correct delimiter type is used for the
    specific data or task.
    - May not fully reveal the impacts of poor delimitation on the LLM's final performance.
    - The preset score threshold may not be refined enough for complex tasks and prompts, requiring regular manual
    adjustment.
    """

    name = "delimitation"
    required_inputs = ["model.prompt"]
    default_params = {"min_threshold": 7}
    tasks = ["text_classification", "text_summarization"]
    tags = ["llm", "zero_shot", "few_shot"]

    system_prompt = """
You are a prompt evaluation AI. You are aware of all prompt engineering best practices and can score prompts based on how well they satisfy different metrics. You analyse the prompts step-by-step based on provided documentation and provide a score and an explanation for how you produced that score.

LLM Prompts that include different sections and user inputs should be properly delimitated. Ideally, the prompt should use triple quotes or backticks or at least single quotes around any user input, reference text or code block etc.
This is to ensure that the prompt is parsed correctly by the model, different pieces of the prompt are understood as separate and any user-provided inputs are not interpreted as part of the prompt.
Identify any issues in the user-submitted prompt and give a score from 1 to 10, where 10 is a perfect score, based on the number and severity of issues.

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
                        title="Delimination Test for LLM Prompt",
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
