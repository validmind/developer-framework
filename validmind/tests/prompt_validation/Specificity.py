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
class Specificity(ThresholdTest, AIPoweredTest):
    """
    **Purpose:**
    The Specificity Test aims to assess the clarity, precision, and effectiveness of prompts
    provided to a Language Learning Model (LLM). Ensuring specificity in the prompts given to an
    LLM can significantly influence the accuracy and relevance of its outputs. The goal of this
    test is to ascertain that the instructions in a prompt are unmistakably clear and relevant,
    eliminating ambiguity and steering the LLM toward desired outcomes.

    **Test Mechanism:**
    Utilizing an LLM, each prompt is graded on a specificity scale ranging from 1 to 10. The grade
    reflects how well the prompt adheres to principles of clarity, detail, and relevancy without
    being overly verbose. Prompts that achieve a grade equal to or exceeding a predefined threshold
    (default set to 7) are deemed to pass the evaluation, while those falling below are marked as
    failing. This threshold can be adjusted as needed.

    **Why Specificity Matters:**
    Prompts that are detailed and descriptive often yield better and more accurate results from
    an LLM. Rather than relying on specific keywords or tokens, it's crucial to have a
    well-structured and descriptive prompt. Including relevant examples within the prompt can be
    particularly effective, guiding the LLM to produce outputs in desired formats. However, it's
    essential to strike a balance. While prompts need to be detailed, they shouldn't be overloaded
    with unnecessary information. The emphasis should always be on relevancy and conciseness,
    considering there are limitations to how long a prompt can be.

    **Example:**
    Imagine wanting an LLM to extract specific details from a given text. A vague prompt might
    yield varied results. However, with a prompt like, "Extract the names of all characters and
    the cities they visited from the text", the LLM is guided more precisely towards the desired
    information extraction.
    """

    category = "prompt_validation"
    name = "specificity"
    required_inputs = ["model.prompt"]
    default_params = {"min_threshold": 7}

    system_prompt = """
You are a prompt evaluation AI. You are aware of all prompt engineering best practices and can score prompts based on how well they satisfy different metrics. You analyse the prompts step-by-step based on provided documentation and provide a score and an explanation for how you produced that score.

Consider the following documentation regarding specificity in prompts and utilize it to grade the user-submitted prompt:
```
Prompts that are detailed and descriptive often yield better and more accurate results from an LLM. Rather than relying on specific keywords or tokens, it's crucial to have a well-structured and descriptive prompt. Including relevant examples within the prompt can be particularly effective, guiding the LLM to produce outputs in desired formats. However, it's essential to strike a balance. While prompts need to be detailed, they shouldn't be overloaded with unnecessary information. The emphasis should always be on relevancy and conciseness, considering there are limitations to how long a prompt can be.

Example:
Imagine wanting an LLM to extract specific details from a given text. A vague prompt might yield varied results. However, with a prompt like, "Extract the names of all characters and the cities they visited from the text", the LLM is guided more precisely towards the desired information extraction.
```

Score the specificity of the user-submitted prompt. Return a score from 0 to 10 where 0 is not specific at all and 10 is very specific. Also provide a short explanation for your score

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
                        title="Specificity Test for LLM Prompt",
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
