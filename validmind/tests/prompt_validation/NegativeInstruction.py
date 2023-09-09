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
class NegativeInstruction(ThresholdTest, AIPoweredTest):
    """
    **Purpose:**
    The Positive Instructional Assessment evaluates prompts provided to a Language Learning Model
    (LLM) to ensure they are framed using affirmative and proactive language. By focusing on what
    should be done rather than what should be avoided, prompts can guide the LLM more effectively
    towards generating appropriate and desired outputs.

    **Test Mechanism:**
    Employing an LLM as an evaluator, each prompt is meticulously analyzed and graded on use of
    positive instructions on a scale from 1 to 10. The grade indicates how well the prompt employs
    affirmative language while avoiding negative or prohibitive instructions. Prompts that achieve a
    grade equal to or exceeding a predetermined threshold (default set to 7) are recognized as
    adhering to positive instruction best practices. This threshold can be adjusted via the test
    parameters.

    **Why Positive Instructions Matter:**
    Prompts that are phrased in the affirmative, emphasizing what to do, tend to direct the LLM
    more clearly than those that focus on what not to do. Negative instructions can lead to
    ambiguities and undesired model responses. By emphasizing clarity and proactive guidance, we
    optimize the chances of obtaining relevant and targeted responses from the LLM.

    **Example:**
    Consider a scenario involving a chatbot designed to recommend movies. An instruction framed as,
    "Don't recommend movies that are horror or thriller" might cause the LLM to fixate on the
    genres mentioned, inadvertently producing undesired results. On the other hand, a
    positively-framed prompt like, "Recommend family-friendly movies or romantic comedies" provides
    clear guidance on the desired output.
    """

    category = "prompt_validation"
    name = "negative_instruction"
    required_inputs = ["model.prompt"]
    default_params = {"min_threshold": 7}

    system_prompt = """
You are a prompt evaluation AI. You are aware of all prompt engineering best practices and can score prompts based on how well they satisfy different metrics. You analyse the prompts step-by-step based on provided documentation and provide a score and an explanation for how you produced that score.

Consider the following documentation regarding negative instructions in prompts and utilize it to grade the user-submitted prompt:
'''
Best practices for LLM prompt engineering suggest that positive instructions should be preferred over negative instructions. For example, instead of saying "Don't do X", it is better to say "Do Y". This is because the model is more likely to generate the desired output if it is given a positive instruction.
Prompts that are phrased in the affirmative, emphasizing what to do, tend to direct the LLM more clearly than those that focus on what not to do. Negative instructions can lead to ambiguities and undesired model responses. By emphasizing clarity and proactive guidance, we optimize the chances of obtaining relevant and targeted responses from the LLM.
Example:
Consider a scenario involving a chatbot designed to recommend movies. An instruction framed as, "Don't recommend movies that are horror or thriller" might cause the LLM to fixate on the genres mentioned, inadvertently producing undesired results. On the other hand, a positively-framed prompt like, "Recommend family-friendly movies or romantic comedies" provides clear guidance on the desired output.
'''

Based on this best practice, please score the user-submitted prompt on a scale of 1-10, with 10 being the best score and 1 being the worst score.
Provide an explanation for your score.

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
                        title="Negative Instruction Test on Prompt",
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
