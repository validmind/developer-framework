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
class Specificity(ThresholdTest):
    """
    Evaluates and scores the specificity of prompts provided to a Large Language Model (LLM), based on clarity, detail,
    and relevance.

    ### Purpose

    The Specificity Test evaluates the clarity, precision, and effectiveness of the prompts provided to a Language
    Model (LLM). It aims to ensure that the instructions embedded in a prompt are indisputably clear and relevant,
    thereby helping to remove ambiguity and steer the LLM towards desired outputs. This level of specificity
    significantly affects the accuracy and relevance of LLM outputs.

    ### Test Mechanism

    The Specificity Test employs an LLM to grade each prompt based on clarity, detail, and relevance parameters within
    a specificity scale that extends from 1 to 10. On this scale, prompts scoring equal to or more than a predefined
    threshold (set to 7 by default) pass the evaluation, while those scoring below this threshold fail it. Users can
    adjust this threshold as per their requirements.

    ### Signs of High Risk

    - Prompts scoring consistently below the established threshold
    - Vague or ambiguous prompts that do not provide clear direction to the LLM
    - Overly verbose prompts that may confuse the LLM instead of providing clear guidance

    ### Strengths

    - Enables precise and clear communication with the LLM to achieve desired outputs
    - Serves as a crucial means to measure the effectiveness of prompts
    - Highly customizable, allowing users to set their threshold based on specific use cases

    ### Limitations

    - This test doesn't consider the content comprehension capability of the LLM
    - High specificity score doesn't guarantee a high-quality response from the LLM, as the model's performance is also
    dependent on various other factors
    - Striking a balance between specificity and verbosity can be challenging, as overly detailed prompts might confuse
    or mislead the model
    """

    name = "specificity"
    required_inputs = ["model.prompt"]
    default_params = {"min_threshold": 7}
    tasks = ["text_classification", "text_summarization"]
    tags = ["llm", "zero_shot", "few_shot"]

    system_prompt = """
You are a prompt evaluation AI. You are aware of all prompt engineering best practices and can score prompts based on how well they satisfy different metrics. You analyse the prompts step-by-step based on provided documentation and provide a score and an explanation for how you produced that score.

Consider the following documentation regarding specificity in prompts and utilize it to grade the user-submitted prompt:
```
Prompts that are detailed and descriptive often yield better and more accurate results from an LLM. Rather than relying on specific keywords or tokens, it's crucial to have a well-structured and descriptive prompt. Including relevant examples within the prompt can be particularly effective, guiding the LLM to produce outputs in desired formats. However, it's essential to strike a balance. While prompts need to be detailed, they shouldn't be overloaded with unnecessary information. The emphasis should always be on relevancy and conciseness, considering there are limitations to how long a prompt can be.

Example:
Imagine wanting an LLM to extract specific details from a given text. A vague prompt might yield varied results. However, with a prompt like, "Extract the names of all characters and the cities they visited from the text", the LLM is guided more precisely towards the desired information extraction.
```

Score the specificity of the user-submitted prompt. Return a score from 1 to 10 where 10 is a perfect score. Also provide a short explanation for your score

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
                        title="Specificity Test for LLM Prompt",
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
