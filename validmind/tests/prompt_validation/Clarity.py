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
    **Purpose:**
    The Clarity Evaluation is designed to assess whether prompts provided to a Language Learning
    Model (LLM) are unmistakably clear in their instructions. With clear prompts, the LLM is better
    suited to more accurately and effectively interpret and respond to instructions in the prompt

    **Test Mechanism:**
    Using an LLM, prompts are scrutinized for clarity, considering aspects like detail inclusion,
    persona adoption, step-by-step instructions, use of examples, and desired output length.
    Each prompt is graded on a scale from 1 to 10 based on its clarity. Prompts scoring at or above
    a predetermined threshold (default is 7) are marked as clear. This threshold can be adjusted
    via the test parameters.

    **Why Clarity Matters:**
    Clear prompts minimize the room for misinterpretation, allowing the LLM to generate more
    relevant and accurate responses. Ambiguous or vague instructions might leave the model
    guessing, leading to suboptimal outputs.

    **Tactics for Ensuring Clarity that will be referenced during evaluation:**
    1. **Detail Inclusion:** Provide essential details or context to prevent the LLM from making
    assumptions.
    2. **Adopt a Persona:** Use system messages to specify the desired persona for the LLM's
    responses.
    3. **Specify Steps:** For certain tasks, delineate the required steps explicitly, helping the
    model in sequential understanding.
    4. **Provide Examples:** While general instructions are efficient, in some scenarios,
    "few-shot" prompting or style examples can guide the LLM more effectively.
    5. **Determine Output Length:** Define the targeted length of the response, whether in terms of
    paragraphs, bullet points, or other units. While word counts aren't always precise, specifying
    formats like paragraphs can offer more predictable results.
    """

    category = "prompt_validation"
    name = "clarity"
    required_inputs = ["model.prompt"]
    default_params = {"min_threshold": 7}

    system_prompt = """
You are a prompt evaluation AI. You are aware of all prompt engineering best practices and can score prompts based on how well they satisfy different metrics. You analyse the prompts step-by-step based on provided documentation and provide a score and an explanation for how you produced that score.

Consider the following documentation on prompt clarity guidelines when evaluating the prompt:
'''
Clear prompts minimize the room for misinterpretation, allowing the LLM to generate more relevant and accurate responses. Ambiguous or vague instructions might leave the model guessing, leading to suboptimal outputs.

Tactics for Ensuring Clarity that will be referenced during evaluation:
1. Detail Inclusion: Provide essential details or context to prevent the LLM from making assumptions.
2. Adopt a Persona: Use system messages to specify the desired persona for the LLM's responses.
3. Specify Steps: For certain tasks, delineate the required steps explicitly, helping the model in sequential understanding.
4. Provide Examples: While general instructions are efficient, in some scenarios, "few-shot" prompting or style examples can guide the LLM more effectively.
5. Determine Output Length: Define the targeted length of the response, whether in terms of paragraphs, bullet points, or other units. While word counts aren't always precise, specifying formats like paragraphs can offer more predictable results.
'''

Score the clarity of the user-submitted prompt. Return a score from 0 to 10 where 0 is not clear at all and 10 is very clear. Also provide a short explanation for your score.

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
                        title="Clarity Test for LLM Prompt",
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
