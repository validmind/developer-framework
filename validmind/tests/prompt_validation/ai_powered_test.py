# Copyright © 2023 ValidMind Inc. All rights reserved.

import re

import openai


class AIPoweredTest:
    """
    Base class for tests powered by gpt4
    """

    def call_model(self, user_prompt: str, system_prompt: str = None):
        """
        Call GPT4 with the passed prompts and return the response.
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

        e.g. "The score is 8" -> 8, "10" -> 10
        """
        # use regex to get the first number (for now this should work)
        return int(re.search(r"\d+", response).group(0))
