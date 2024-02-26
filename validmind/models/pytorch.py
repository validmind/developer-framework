# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from validmind.errors import MissingModelPredictFnError
from validmind.logging import get_logger
from validmind.vm_models.model import (
    ModelAttributes,
    VMModel,
    has_method_with_arguments,
)

logger = get_logger(__name__)


class PyTorchModel(VMModel):
    """
    An PyTorch model class that wraps a trained model instance and its associated data.

    Attributes:
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
        model (object, optional): The trained model instance. Defaults to None.
        device_type(str, optional) The device where model is trained
    """

    def __init__(
        self,
        model: object = None,  # Trained model instance
        input_id: str = None,
        attributes: ModelAttributes = None,
    ):
        super().__init__(
            model=model,
            input_id=input_id,
            attributes=attributes,
        )
        self._device_type = next(self.model.parameters()).device

    def predict_proba(self, *args, **kwargs):
        """
        Invoke predict_proba from underline model
        """
        if not has_method_with_arguments(self.model, "predict_proba", 1):
            raise MissingModelPredictFnError(
                "Model requires a implemention of predict_proba method with 1 argument"
                + " that is tensor features matrix"
            )

        if callable(getattr(self.model, "predict_proba", None)):
            return self.model.predict_proba(*args, **kwargs)[:, 1]

    def predict(self, *args, **kwargs):
        """
        Predict method for the model. This is a wrapper around the model's
        """
        if not has_method_with_arguments(self.model, "predict", 1):
            raise MissingModelPredictFnError(
                "Model requires a implemention of predict method with 1 argument"
                + " that is tensor features matrix"
            )
        import torch

        return self.model.predict(torch.tensor(args[0]).to(self.device_type))

    def model_library(self):
        """
        Returns the model library name
        """
        return "torch"

    def model_class(self):
        """
        Returns the model class name
        """
        return "PyTorchModel"

    def model_name(self):
        """
        Returns model architecture
        """
        return "PyTorch Neural Networks"
