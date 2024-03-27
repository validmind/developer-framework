# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd

from validmind.errors import MissingModelPredictFnError
from validmind.logging import get_logger
from validmind.vm_models.model import (
    ModelAttributes,
    VMModel,
    has_method_with_arguments,
)

logger = get_logger(__name__)


@dataclass
class HFModel(VMModel):
    """
    An Hugging Face model class that wraps a trained model instance and its associated data.

    Attributes:
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
        model (object, optional): The trained model instance. Defaults to None.
    """

    def __init__(
        self,
        input_id: str = None,
        model: object = None,  # Trained model instance
        attributes: ModelAttributes = None,
    ):
        super().__init__(
            model=model,
            input_id=input_id,
            attributes=attributes,
        )

    def predict_proba(self, *args, **kwargs):
        """
        Invoke predict_proba from underline model
        """
        if not has_method_with_arguments(self.model, "predict_proba", 1):
            raise MissingModelPredictFnError(
                "Model requires a implementation of predict_proba method with 1 argument"
                + " that is tensor features matrix"
            )

        if callable(getattr(self.model, "predict_proba", None)):
            return self.model.predict_proba(*args, **kwargs)[:, 1]

    def predict(self, data):
        """
        Predict method for the model. This is a wrapper around the HF model's pipeline function
        """
        results = self.model([str(datapoint) for datapoint in data])

        tasks = self.model.__class__.__module__.split(".")

        if "text2text_generation" in tasks:
            return pd.DataFrame(results).summary_text.values
        elif "text_classification" in tasks:
            return pd.DataFrame(results).label.values
        elif tasks[-1] == "feature_extraction":
            # extract [CLS] token embedding for each input and wrap in dataframe
            return pd.DataFrame([embedding[0][0] for embedding in results])
        else:
            return results

    def model_library(self):
        """
        Returns the model library name
        """
        return self.model.__class__.__module__.split(".")[0]

    def model_class(self):
        """
        Returns the model class name
        """
        return self.model.__class__.__name__

    def model_name(self):
        """
        Returns model name
        """
        return type(self.model).__name__

    def is_pytorch_model(self):
        return self.model_library() == "torch"
