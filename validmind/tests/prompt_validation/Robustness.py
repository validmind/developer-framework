# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from typing import List

import pandas as pd

from validmind.errors import MissingRequiredTestInputError, SkipTestError
from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)

from .ai_powered_test import call_model, missing_prompt_message


@dataclass
class Robustness(ThresholdTest):
    """
    Assesses the robustness of prompts provided to a Large Language Model under varying conditions and contexts.

    ### Purpose

    The Robustness test is meant to evaluate the resilience and reliability of prompts provided to a Language Learning
    Model (LLM). The aim of this test is to guarantee that the prompts consistently generate accurate and expected
    outputs, even in diverse or challenging scenarios.

    ### Test Mechanism

    The Robustness test appraises prompts under various conditions, alterations, and contexts to ascertain their
    stability in producing consistent responses from the LLM. Factors evaluated include different phrasings, inclusion
    of potential distracting elements, and various input complexities. By default, the test generates 10 inputs for a
    prompt but can be adjusted according to test parameters.

    ### Signs of High Risk

    - If the output from the tests diverges extensively from the expected results, this indicates high risk.
    - When the prompt doesn't give a consistent performance across various tests.
    - A high risk is indicated when the prompt is susceptible to breaking, especially when the output is expected to be
    of a specific type.

    ### Strengths

    - The robustness test helps to ensure stable performance of the LLM prompts and lowers the chances of generating
    unexpected or off-target outputs.
    - This test is vital for applications where predictability and reliability of the LLM’s output are crucial.

    ### Limitations

    - Currently, the test only supports single-variable prompts, which restricts its application to more complex models.
    - When there are too many target classes (over 10), the test is skipped, which can leave potential vulnerabilities
    unchecked in complex multi-class models.
    - The test may not account for all potential conditions or alterations that could show up in practical use
    scenarios.
    """

    name = "robustness"
    required_inputs = ["model"]
    default_params = {"num_tests": 10}
    tasks = ["text_classification", "text_summarization"]
    tags = ["llm", "zero_shot", "few_shot"]

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
        if not hasattr(self.inputs.model, "prompt"):
            raise MissingRequiredTestInputError(missing_prompt_message)

        # TODO: add support for multi-variable prompts
        if (
            not self.inputs.model.prompt.variables
            or len(self.inputs.model.prompt.variables) > 1
        ):
            raise SkipTestError(
                "Robustness only supports single-variable prompts for now"
            )

        target_class_labels = self.inputs.dataset.target_classes()
        # Guard against too many classes (maybe not a classification model)
        if len(target_class_labels) > 10:
            raise SkipTestError(
                "Too many target classes to test robustness. Skipping test."
            )

        results = []

        for _ in range(self.params["num_tests"]):
            response = call_model(
                system_prompt=self.system_prompt,
                user_prompt=self.user_prompt.format(
                    variables="\n".join(self.inputs.model.prompt.variables),
                    prompt_to_test=self.inputs.model.prompt.template,
                ),
            )

            test_input_df = pd.DataFrame(
                [response],
                columns=self.inputs.model.prompt.variables,
            )
            result = self.inputs.model.predict(test_input_df)[0]

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
