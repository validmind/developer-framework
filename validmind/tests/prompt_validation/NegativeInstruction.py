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

Consider the following documentation regarding negative instructions in prompts and utilize it to grade the user-submitted prompt:
'''
Best practices for LLM prompt engineering suggest that positive instructions should be preferred over negative instructions. For example, instead of saying "Don't do X", it is better to say "Do Y". This is because the model is more likely to generate the desired output if it is given a positive instruction.
Prompts that are phrased in the affirmative, emphasizing what to do, tend to direct the LLM more clearly than those that focus on what not to do. Negative instructions can lead to ambiguities and undesired model responses. By emphasizing clarity and proactive guidance, we optimize the chances of obtaining relevant and targeted responses from the LLM.
Example:
Consider a scenario involving a chatbot designed to recommend movies. An instruction framed as, "Don't recommend movies that are horror or thriller" might cause the LLM to fixate on the genres mentioned, inadvertently producing undesired results. On the other hand, a positively-framed prompt like, "Recommend family-friendly movies or romantic comedies" provides clear guidance on the desired output.
'''

Based on this best practice, please score the user-submitted prompt on a scale of 1-10, where 10 is a perfect score.
Provide an explanation for your score.

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
def NegativeInstruction(model, min_threshold=7):
    """
    Evaluates and grades the use of affirmative, proactive language over negative instructions in LLM prompts.
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
