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
class Delimitation(ThresholdTest, AIPoweredTest):
    """
    **Purpose:**
    The Delimitation Test ensures that prompts provided to the Language Learning Model
    (LLM) use delimiters correctly to distinctly mark sections of the input. Properly delimited
    prompts simplify the LLM's interpretation process, ensuring accurate and precise responses.

    **Test Mechanism:**
    Using an LLM, prompts are checked for their appropriate use of delimiters such as triple
    quotation marks, XML tags, and section titles. Each prompt receives a score from 1 to 10
    based on its delimitation integrity. Prompts scoring at or above a set threshold (default is 7)
    pass the check. This threshold can be modified as needed.

    **Why Proper Delimitation Matters:**
    Delimiters play a crucial role in segmenting and organizing prompts, especially when diverse
    data or multiple tasks are involved. They help in clearly distinguishing between different
    parts of the input, reducing ambiguity for the LLM. As task complexity increases, the correct
    use of delimiters becomes even more critical to ensure the LLM understands the prompt's
    intent.

    **Example:**
    When given a prompt like:

    ```USER: Summarize the text delimited by triple quotes. '''insert text here'''```

    or:

    ```USER: <article> insert first article here </article>
    <article> insert second article here </article>```

    The LLM can more accurately discern sections of the text to be treated differently, thanks to
    the clear delimitation.
    """

    category = "prompt_validation"
    name = "delimitation"
    required_inputs = ["model.prompt"]
    default_params = {"min_threshold": 7}

    system_prompt = """
You are a prompt evaluation AI. You are aware of all prompt engineering best practices and can score prompts based on how well they satisfy different metrics. You analyse the prompts step-by-step based on provided documentation and provide a score and an explanation for how you produced that score.

LLM Prompts that include different sections and user inputs should be properly delimitated. Ideally, the prompt should use triple quotes or backticks or at least single quotes around any user input, reference text or code block etc.
This is to ensure that the prompt is parsed correctly by the model, different pieces of the prompt are understood as separate and any user-provided inputs are not interpreted as part of the prompt.
Identify any issues in the user-submitted prompt and give a score from 1 to 10 based on the number and severity of issues.

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
                        title="Delimination Test for LLM Prompt",
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
