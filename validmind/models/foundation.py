# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd

from validmind.logging import get_logger
from validmind.vm_models.model import ModelAttributes, VMModel

logger = get_logger(__name__)


@dataclass
class Prompt:
    template: str
    variables: list


class FoundationModel(VMModel):
    """FoundationModel class wraps a Foundation LLM endpoint

    This class wraps a predict function that is user-defined and adapts it to works
    with ValidMind's model interface for the purpose of model eval and documentation

    Attributes:
        predict_fn (callable): The predict function that should take a prompt as input
          and return the result from the model
        prompt (Prompt): The prompt object that defines the prompt template and the
          variables (if any)
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
    """

    def __init__(
        self,
        predict_fn: callable,
        prompt: Prompt,  # prompt used for model (for now just a string)
        attributes: ModelAttributes = None,
        input_id: str = None,
    ):
        super().__init__(
            attributes=attributes,
            input_id=input_id,
        )
        self.predict_fn = predict_fn
        self.prompt = prompt

    def _build_prompt(self, x: pd.DataFrame):
        """
        Builds the prompt for the model
        """
        return self.prompt.template.format(
            **{key: x[key] for key in self.prompt.variables}
        )

    def predict(self, X: pd.DataFrame):
        """
        Predict method for the model. This is a wrapper around the model's
        """
        return [self.predict_fn(self._build_prompt(x[1])) for x in X.iterrows()]

    def model_library(self):
        """
        Returns the model library name
        """
        return "FoundationModel"

    def model_class(self):
        """
        Returns the model class name
        """
        return "FoundationModel"

    def model_name(self):
        """
        Returns model name
        """
        return "FoundationModel"
