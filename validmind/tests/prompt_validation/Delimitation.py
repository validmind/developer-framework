# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from validmind import tags, tasks
from validmind.errors import MissingRequiredTestInputError

from .ai_powered_test import (
    call_model,
    get_explanation,
    get_score,
    missing_prompt_message,
)

SYSTEM = """
You are a prompt evaluation AI. You are aware of all prompt engineering best practices and can score prompts based on how well they satisfy different metrics. You analyse the prompts step-by-step based on provided documentation and provide a score and an explanation for how you produced that score.

LLM Prompts that include different sections and user inputs should be properly delimitated. Ideally, the prompt should use triple quotes or backticks or at least single quotes around any user input, reference text or code block etc.
This is to ensure that the prompt is parsed correctly by the model, different pieces of the prompt are understood as separate and any user-provided inputs are not interpreted as part of the prompt.
Identify any issues in the user-submitted prompt and give a score from 1 to 10, where 10 is a perfect score, based on the number and severity of issues.

Response Format:
```
Score: <score>
Explanation: <explanation>
```
""".strip()

USER = '''
Prompt:
"""
{prompt_to_test}
"""
'''.strip()


@tags("llm", "zero_shot", "few_shot")
@tasks("text_classification", "text_summarization")
def Delimitation(model, min_threshold=7):
    """
    Evaluates the proper use of delimiters in prompts provided to Large Language Models.
    """
    if not hasattr(model, "prompt"):
        raise MissingRequiredTestInputError(missing_prompt_message)

    response = call_model(
        system_prompt=SYSTEM,
        user_prompt=USER.format(prompt_to_test=model.prompt.template),
    )
    score = get_score(response)
    explanation = get_explanation(response)

    passed = score > min_threshold
    result = [
        {
            "Score": score,
            "Threshold": min_threshold,
            "Explanation": explanation,
            "Pass/Fail": "Pass" if passed else "Fail",
        }
    ]

    return result, passed
