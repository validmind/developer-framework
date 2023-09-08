# Copyright © 2023 ValidMind Inc. All rights reserved.

import re

import openai


class AIPoweredTest:
    """
    Base class for tests powered by an LLM
    """

    model_name = "gpt-4"

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

        e.g. "Explanation: <some-explanation>\nScore: 8" ->
        """
        score = re.search(r"Score: (\d+)", response)

        if not score:
            raise ValueError("Could not find score in response")

        return int(score.group(1))

    def get_explanation(self, response: str):
        """
        Get just the explanation from the response string

        e.g. "Explanation: <some-explanation>\nScore: 8" -> "<some-explanation>"
        """
        explanation = re.search(r"Explanation: (.*)", response)

        if not explanation:
            raise ValueError("Could not find explanation in response")

        return explanation.group(1)
