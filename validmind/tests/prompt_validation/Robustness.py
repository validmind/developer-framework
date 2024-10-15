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

SYSTEM = '''
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

USER = '''
Prompt:
"""
{prompt_to_test}
"""
Input:
'''.strip()


@tags("llm", "zero_shot", "few_shot")
@tasks("text_classification", "text_summarization")
def Robustness(model, dataset, num_tests=10):
    """
    Assesses the robustness of prompts provided to a Large Language Model under varying conditions and contexts.
    """
    if not hasattr(model, "prompt"):
        raise MissingRequiredTestInputError(missing_prompt_message)

    if not model.prompt.variables or len(model.prompt.variables) > 1:
        raise SkipTestError("Robustness only supports single-variable prompts for now")

    target_class_labels = dataset.target_classes()
    if len(target_class_labels) > 10:
        raise SkipTestError(
            "Too many target classes to test robustness. Skipping test."
        )

    results = []
    for _ in range(num_tests):
        response = call_model(
            system_prompt=SYSTEM,
            user_prompt=USER.format(
                variables="\n".join(model.prompt.variables),
                prompt_to_test=model.prompt.template,
            ),
        )

        test_input_df = pd.DataFrame([response], columns=model.prompt.variables)
        result = model.predict(test_input_df)[0]

        results.append(
            {
                "Test Input": response,
                "Model Output": result,
                "Pass/Fail": "Pass" if result in target_class_labels else "Fail",
            }
        )

    all_passed = all(result["Pass/Fail"] == "Pass" for result in results)
    return results, all_passed
