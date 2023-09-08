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
class Bias(ThresholdTest, AIPoweredTest):
    """
    **Purpose:**
    Bias Evaluation is aimed at assessing if and how the distribution and order of exemplars
    (examples) within a few-shot learning prompt affect the Language Learning Model's (LLM)
    output, potentially introducing biases. By examining these influences, we can optimize
    the model's performance and mitigate unintended biases in its responses.

    **Test Mechanism:**

    1. **Distribution of Exemplars:** Check how varying the number of positive vs. negative
    examples in a prompt impacts the LLM's classification of a neutral or ambiguous statement.
    2. **Order of Exemplars:** Examine if the sequence in which positive and negative examples are
    presented can sway the LLM's response.

    For each test case, an LLM is used to grade the input prompt on a scale from 1 to 10, based
    on whether the examples in the prompt may lead to biased responses. A minimum threshold
    must be met in order for the test to pass. By default, this threshold is set to 7, but it
    can be adjusted as needed via the test parameters.
    """

    category = "prompt_validation"
    name = "bias"
    required_inputs = ["model.prompt"]
    default_params = {"min_threshold": 7}

    system_prompt = """
You are a prompt evaluation AI. You are aware of all prompt engineering best practices and can score prompts based on how well they satisfy different best practices. You analyse the prompts step-by-step based on provided documentation and provide a score and an explanation for how you produced that score.

Consider the following best practice documentation:
```
Its been shown that, when passing examples to an LLM via the prompt for the purpose of Sentiment Analysis, a distribution with a majority of positive examples led the LLM to classify ambiguous sentences as "Positive", and vice versa. However, for more straightforward tasks, such as sentiment classification, biases may be harder to induce. The order of presentation also appeared to influence the LLM's outputs, especially when combined with a skewed distribution of exemplars.
Tactics for Avoiding Bias in Prompting:
1. Balanced Distribution: Avoid heavily skewed distributions of examples. Instead, offer amore balanced number of examples for each label.
2. Randomize Order: To prevent order-induced biases, shuffle the sequence of examples ensuring no fixed pattern, such as presenting all positive examples first.
3. Continued Experimentation: Regularly test and tweak prompts, especially for complex tasks where the LLM might not have extensive knowledge. This iterative process helps in identifying potential pitfalls and refining prompting strategies.
Example:
For instance, using 8 positive and 2 negative examples led the LLM to classify an ambiguous sentence "I feel something" as "Positive". However, with a more balanced distribution, the LLM showed unbiased behavior.
```

Score the bias of the user-submitted prompt. Return a score from 0 to 10 where 0 is the worst and 10 is perfect. Also provide a short explanation for your score.

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
                        title="Bias Test on Prompt",
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
