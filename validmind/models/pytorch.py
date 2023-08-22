# Copyright © 2023 ValidMind Inc. All rights reserved.
import numpy as np

from validmind.errors import MissingModelPredictFnError
from validmind.vm_models.dataset import VMDataset
from validmind.vm_models.model import (
    ModelAttributes,
    VMModel,
    has_method_with_arguments,
)


class PyTorchModel(VMModel):
    """
    An PyTorch model class that wraps a trained model instance and its associated data.

    Attributes:
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
        model (object, optional): The trained model instance. Defaults to None.
        train_ds (Dataset, optional): The training dataset. Defaults to None.
        test_ds (Dataset, optional): The test dataset. Defaults to None.
        validation_ds (Dataset, optional): The validation dataset. Defaults to None.
        y_train_predict (object, optional): The predicted outputs for the training dataset. Defaults to None.
        y_test_predict (object, optional): The predicted outputs for the test dataset. Defaults to None.
        y_validation_predict (object, optional): The predicted outputs for the validation dataset. Defaults to None.
        device_type(str, optional) The device where model is trained
    """

    def __init__(
        self,
        model: object = None,  # Trained model instance
        train_ds: VMDataset = None,
        test_ds: VMDataset = None,
        validation_ds: VMDataset = None,
        attributes: ModelAttributes = None,
    ):
        super().__init__(
            model=model,
            train_ds=train_ds,
            test_ds=test_ds,
            validation_ds=validation_ds,
            attributes=attributes,
        )
        if self.model and self.train_ds:
            self._y_train_predict = np.array(self.predict(self.train_ds.x))
        if self.model and self.test_ds:
            self._y_test_predict = np.array(self.predict(self.test_ds.x))
        if self.model and self.validation_ds:
            self._y_validation_predict = np.array(self.predict(self.validation_ds.x))

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
