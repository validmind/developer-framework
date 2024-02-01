# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import os
import re

from openai import AzureOpenAI, OpenAI


class AIPoweredTest:
    """
    Base class for tests powered by an LLM
    """

    api_key = None
    client = None
    endpoint = None
    model_name = None

    def __init__(self, *args, **kwargs):
        if "OPENAI_API_KEY" in os.environ:
            self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            self.model_name = os.environ.get("VM_OPENAI_MODEL", "gpt-3.5-turbo")

        elif "AZURE_OPENAI_KEY" in os.environ:
            if "AZURE_OPENAI_ENDPOINT" not in os.environ:
                raise ValueError(
                    "AZURE_OPENAI_ENDPOINT must be set to run LLM tests with Azure"
                )

            if "AZURE_OPENAI_MODEL" not in os.environ:
                raise ValueError(
                    "AZURE_OPENAI_MODEL must be set to run LLM tests with Azure"
                )

            self.client = AzureOpenAI(
                azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
                api_key=os.environ.get("AZURE_OPENAI_KEY"),
                api_version=os.environ.get("AZURE_OPENAI_VERSION", "2023-05-15"),
            )
            self.model_name = os.environ.get("AZURE_OPENAI_MODEL")

        else:
            raise ValueError(
                "OPENAI_API_KEY or AZURE_OPENAI_KEY must be set to run LLM tests"
            )

    def call_model(self, user_prompt: str, system_prompt: str = None):
        """
        Call an LLM with the passed prompts and return the response. We're using GPT4 for now.
        """
        return (
            self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            .choices[0]
            .message.content
        )

    def get_score(self, response: str):
        """
        Get just the numeric data in the response string and convert it to an int

        e.g. "Score: 8\nExplanation: <some-explanation>" -> 8
        """
        score = re.search(r"Score: (\d+)", response)

        if not score:
            raise ValueError("Could not find score in response")

        return int(score.group(1))

    def get_explanation(self, response: str):
        """
        Get just the explanation from the response string

        e.g. "Score: 8\nExplanation: <some-explanation>" -> "<some-explanation>"
        """
        explanation = re.search(r"Explanation: (.+)", response, re.DOTALL)

        if not explanation:
            raise ValueError("Could not find explanation in response")

        return explanation.group(1)
