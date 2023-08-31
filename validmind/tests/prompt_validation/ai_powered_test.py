# Copyright © 2023 ValidMind Inc. All rights reserved.
from abc import ABC, abstractmethod

import openai

from validmind.vm_models import ThresholdTest


class BasePromptTest(ThresholdTest, ABC):
    """
    Base class for tests powered by prompt-based language models.
    """

    model_name = "gpt-4"  # Default model

    def call_model(self, system_prompt, test_prompt):
        """
        Call the specified model with the constructed prompts and return the response.
        For now, we assume that all models have a similar API structure.
        """
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": test_prompt},
            ],
        )
        return response.choices[0].message["content"]

    @abstractmethod
    def build_system_prompt(self):
        """
        Build the system prompt. To be implemented by subclasses.
        """
        pass

    @abstractmethod
    def build_test_prompt(self):
        """
        Build the test prompt. To be implemented by subclasses.
        """
        pass

    def summary(self, results, all_passed):
        """
        Generate a summary of the test results.
        """
        result = results[0]
        results_table = [
            {
                "Score": result.values["score"],
                "Threshold": result.values["threshold"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pd.DataFrame(results_table),
                    metadata=ResultTableMetadata(title=f"{self.name} Test"),
                )
            ]
        )
