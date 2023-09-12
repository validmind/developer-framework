# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

import pandas as pd

from validmind.errors import SkipTestError
from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
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
    in eliciting consistent responses from the LLM. Factors such as different phrasings,
    inclusion of potential distractors, and varied input complexities are introduced to test the robustness of the prompt.

    **Why Robustness Matters:**
    A robust prompt ensures consistent performance and reduces the likelihood of unexpected or
    off-tangent outputs. This consistency is vital for applications where predictability and
    reliability of the LLM's response are paramount.
    """

    category = "prompt_validation"
    name = "robustness"
    required_inputs = ["model"]

    system_prompt = """
You are a prompt evaluation researcher AI who is tasked with testing the robustness of LLM prompts.

Consider the following guidelines:
```
LLM prompts are used to guide a model to generate specific outputs or solve specific tasks. These prompts can be more or less robust, meaning that they can be more or less susceptible to breaking especially when the output needs to be a specific type.
A robust prompt ensures consistent performance and reduces the likelihood of unexpected or off-tangent outputs. This consistency is vital for applications where predictability and reliability of the LLM's response are paramount.
```

Consider the user-submitted prompt template and generate 10 inputs for each variable used in the prompt to test the robustness of the prompt.
The inputs should be valid inputs but should be designed to try and break the output.
Common strategies to use include contradictions, edge cases, typos, and any method that can force the model to generate an incorrect output.

For example:
Give this prompt, "Analyse the following sentence and output its sentiment\n{input}", a good test would be to generate confusing inputs like "This sentence is positive" or "This sentence is negative" to see if the model can still output the correct sentiment.
Another good test would be to generate a nonsensical string that is not a sentence.
Be creative and think step-by-step how you would break the prompt.
""".strip()
    user_prompt = '''
For the following prompt template where variables are denoted by python's f-string syntax:
"""
{prompt_to_test}
"""
Return 10 inputs separated by a new line where each input contains a value for every variable in the prompt template. See the example below for a prompt template with 1 variables `var1` and `var2`:
```
var1:<value-designed-to-break-the-prompt>|var2:<value-designed-to-break-the-prompt>
... repeat 9 more times
```
As you can see, each variable-value pair is separated by a pipe (|) and the variable is separated from the value by a colon (:).
Respond only with the above and do not include any extra text or explanation.
'''.strip()

    def summary(self, results: List[TestResult], all_passed: bool):
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
        if len(self.model.prompt.variables) > 1:
            raise SkipTestError(
                "Robustness only supports single-variable prompts for now"
            )

        response = self.call_model(
            system_prompt=self.system_prompt,
            user_prompt=self.user_prompt.format(
                variables="\n".join(self.model.prompt.variables),
                prompt_to_test=self.model.prompt.template,
            ),
        )

        results = []
        target_class_labels = self.model.test_ds.target_classes()

        # Guard against too many classes (maybe not a classification model)
        if len(target_class_labels) > 10:
            raise SkipTestError(
                "Too many target classes to test robustness. Skipping test."
            )

        print(response)
        for test_input in response.split("\n"):
            values = {}
            for variable_value in test_input.split("|"):
                variable = variable_value.split(":")[0]
                if variable not in self.model.prompt.variables:
                    raise SkipTestError(
                        f"Variable {variable} is not in the prompt. Skipping test."
                    )
                values[variable] = variable_value.split(":")[1]

            test_input_df = pd.DataFrame(values, index=[0])
            result = self.model.predict(test_input_df)[0]

            fail = False
            if result not in target_class_labels:
                fail = True

            results.append(
                TestResult(
                    passed=not fail,
                    values={
                        "input": test_input,
                        "output": result,
                    },
                )
            )

        return self.cache_results(
            results, passed=all([result.passed for result in results])
        )
