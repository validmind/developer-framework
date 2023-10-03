# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

import pandas as pd

from validmind.errors import SkipTestError
from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)

from .ai_powered_test import AIPoweredTest


@dataclass
class Robustness(ThresholdTest, AIPoweredTest):
    """
    **Purpose:**
    The Robustness Integrity Assessment evaluates the resilience and reliability of prompts
    provided to a Language Learning Model (LLM). The primary objective is to ensure that prompts
    consistently produce accurate and desired outputs, even in diverse or challenging scenarios.

    **Test Mechanism:**
    Prompts are subjected to various conditions, alterations, and contexts to check their stability
    in eliciting consistent responses from the LLM. Factors such as different phrasings, inclusion
    of potential distractors, and varied input complexities are introduced to test the robustness
    of the prompt. By default, the test generates 10 inputs for the prompt but this can be adjusted
    via the test parameters.

    **Why Robustness Matters:**
    A robust prompt ensures consistent performance and reduces the likelihood of unexpected or
    off-tangent outputs. This consistency is vital for applications where predictability and
    reliability of the LLM's response are paramount.
    """

    category = "prompt_validation"
    name = "robustness"
    required_inputs = ["model"]
    default_params = {"num_tests": 10}
    metadata = {
        "task_types": ["text_classification", "text_summarization"],
        "tags": ["llm", "zero_shot", "few_shot"],
    }

    system_prompt = '''
You are a prompt evaluation researcher AI who is tasked with testing the robustness of LLM prompts.

Consider the following guidelines:
```
LLM prompts are used to guide a model to generate specific outputs or solve specific tasks. These prompts can be more or less robust, meaning that they can be more or less susceptible to breaking especially when the output needs to be a specific type.
A robust prompt ensures consistent performance and reduces the likelihood of unexpected or off-tangent outputs. This consistency is vital for applications where predictability and reliability of the LLM's response are paramount.
```

Consider the user-submitted prompt template and generate an input for the variable in the template (denoted by brackets) that tests the robustness of the prompt.
Contradictions, edge cases, typos, bad phrasing, distracting, complex or out-of-place words and phrases are just some of the strategies you can use when generating inputs.
Be creative and think step-by-step how you would break the prompt. Then generate an input for the user-submitted prompt template that would break the prompt.
Respond only with the value to be inserted into the prompt template and do not include quotes, explanations or any extra text.
Example:
Prompt:
"""
Analyse the following sentence and output its sentiment\n{sentence}
"""
Input:
Nonsense string that has no sentiment
'''.strip()
    user_prompt = '''
Prompt:
"""
{prompt_to_test}
"""
Input:
'''.strip()

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
        results_table = [
            {
                "Test Input": result.values["input"],
                "Model Output": result.values["output"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pd.DataFrame(results_table),
                    metadata=ResultTableMetadata(
                        title="Robustness Test on Prompt",
                    ),
                )
            ]
        )

    def run(self):
        # TODO: add support for multi-variable prompts
        if len(self.model.prompt.variables) > 1:
            raise SkipTestError(
                "Robustness only supports single-variable prompts for now"
            )

        target_class_labels = self.model.test_ds.target_classes()
        # Guard against too many classes (maybe not a classification model)
        if len(target_class_labels) > 10:
            raise SkipTestError(
                "Too many target classes to test robustness. Skipping test."
            )

        results = []

        for _ in range(self.params["num_tests"]):
            response = self.call_model(
                system_prompt=self.system_prompt,
                user_prompt=self.user_prompt.format(
                    variables="\n".join(self.model.prompt.variables),
                    prompt_to_test=self.model.prompt.template,
                ),
            )

            test_input_df = pd.DataFrame(
                [response],
                columns=self.model.prompt.variables,
            )
            result = self.model.predict(test_input_df)[0]

            fail = False
            if result not in target_class_labels:
                fail = True

            results.append(
                ThresholdTestResult(
                    passed=not fail,
                    values={
                        "input": response,
                        "output": result,
                    },
                )
            )

        return self.cache_results(
            results, passed=all([result.passed for result in results])
        )
