# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import re

from validmind.ai.utils import get_client_and_model
from validmind.client_config import client_config

missing_prompt_message = """
Cannot run prompt validation tests on a model with no prompt.
You can set a prompt when creating a vm_model object like this:
my_vm_model = vm.init_model(
    predict_fn=call_model,
    prompt=Prompt(
        template="<your-prompt-here>",
        variables=[],
    ),
    input_id="my_llm_model",
)
"""


def call_model(
    system_prompt: str, user_prompt: str, temperature: float = 0.0, seed: int = 42
):
    """Call LLM with the given prompts and return the response"""
    if not client_config.can_generate_llm_test_descriptions():
        raise ValueError(
            "LLM based descriptions are not enabled for your organization."
        )

    client, model = get_client_and_model()

    return (
        client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            seed=seed,
        )
        .choices[0]
        .message.content
    )


def get_score(response: str):
    """Get just the score from the response string
    TODO: use json response mode instead of this

    e.g. "Score: 8\nExplanation: <some-explanation>" -> 8
    """
    score = re.search(r"Score: (\d+)", response)

    if not score:
        raise ValueError("Could not find score in response")

    return int(score.group(1))


def get_explanation(response: str):
    """Get just the explanation from the response string
    TODO: use json response mode instead of this

    e.g. "Score: 8\nExplanation: <some-explanation>" -> "<some-explanation>"
    """
    explanation = re.search(r"Explanation: (.+)", response, re.DOTALL)

    if not explanation:
        raise ValueError("Could not find explanation in response")

    return explanation.group(1).strip().strip("`")
