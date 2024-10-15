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

USER = '''
Prompt:
"""
{prompt_to_test}
"""
'''.strip()


@tags("llm", "zero_shot", "few_shot")
@tasks("text_classification", "text_summarization")
def Specificity(model, min_threshold=7):
    """
    Evaluates and scores the specificity of prompts provided to a Large Language Model (LLM), based on clarity, detail,
    and relevance.
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
