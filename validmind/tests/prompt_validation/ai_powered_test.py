# Copyright © 2023 ValidMind Inc. All rights reserved.

import os
import re

import openai


class AIPoweredTest:
    """
    Base class for tests powered by an LLM
    """

    model_name = "gpt-3.5-turbo"

    def __init__(self, *args, **kwargs):
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY must be set to run AI-powered tests")

        # this should be set already but just set it again in case user loaded dotenv
        # after the module was initialized
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        # allow overriding the model name (if user has access to and wants to use GPT4)
        if os.environ.get("VM_OPENAI_MODEL"):
            self.model_name = os.environ.get("VM_OPENAI_MODEL")

    def call_model(self, user_prompt: str, system_prompt: str = None):
        """
        Call an LLM with the passed prompts and return the response. We're using GPT4 for now.
        """
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message["content"]

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
