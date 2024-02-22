# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np
import pandas as pd

from validmind.logging import get_logger
from validmind.vm_models.dataset import VMDataset
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
        train_ds: (VMDataset, optional): The training dataset. Defaults to None.
        test_ds: (VMDataset, optional): The test dataset. Defaults to None.
        validation_ds: (VMDataset, optional): The validation dataset. Defaults to None.
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
    """

    def __init__(
        self,
        predict_fn: callable,
        prompt: Prompt,  # prompt used for model (for now just a string)
        train_ds: VMDataset = None,
        test_ds: VMDataset = None,
        validation_ds: VMDataset = None,
        attributes: ModelAttributes = None,
    ):
        super().__init__(
            train_ds=train_ds,
            test_ds=test_ds,
            validation_ds=validation_ds,
            attributes=attributes,
        )

        self.predict_fn = predict_fn
        self.prompt = prompt

        def predict_and_assign(ds, attr_name):
            if ds:
                if ds.prediction_column:
                    setattr(self, attr_name, ds.y_pred)
                else:
                    logger.info("Running predict()...This may take a while")
                    setattr(self, attr_name, np.array(self.predict(ds.x_df())))

        predict_and_assign(self.train_ds, "_y_train_predict")
        predict_and_assign(self.test_ds, "_y_test_predict")
        predict_and_assign(self.validation_ds, "_y_validation_predict")

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
        return np.array(
            [self.predict_fn(self._build_prompt(x[1])) for x in X.iterrows()]
        )

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
