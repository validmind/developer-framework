# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Model class wrapper module
"""
import importlib
import inspect
from abc import abstractmethod
from dataclasses import dataclass

SUPPORTED_LIBRARIES = {
    "catboost": "CatBoostModel",
    "xgboost": "XGBoostModel",
    "sklearn": "SKlearnModel",
    "statsmodels": "StatsModelsModel",
    "torch": "PyTorchModel",
    "transformers": "HFModel",
    "custom": "SKlearnModel",
}

R_MODEL_TYPES = [
    "LogisticRegression",
    "LinearRegression",
    "XGBClassifier",
    "XGBRegressor",
]

R_MODEL_METHODS = [
    "glm.fit",
]


@dataclass
class ModelAttributes:
    """
    Model attributes definition
    """

    architecture: str = None
    framework: str = None
    framework_version: str = None


class VMModel:
    """
    An base class that wraps a trained model instance and its associated data.

    Attributes:
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
        model (object, optional): The trained model instance. Defaults to None.
        device_type(str, optional) The device where model is trained
    """

    input_id: str = None

    def __init__(
        self,
        input_id: str = None,
        model: object = None,
        attributes: ModelAttributes = None,
    ):
        self._model = model
        self._input_id = input_id
        self._attributes = attributes

        # The device where model is trained
        self._device_type = None

    @property
    def attributes(self):
        return self._attributes

    @property
    def input_id(self):
        return self._input_id

    @property
    def model(self):
        return self._model

    @property
    def device_type(self):
        """
        The device where model is trained
        """
        return self._device_type

    def serialize(self):
        """
        Serializes the model to a dictionary so it can be sent to the API
        """
        return {
            "attributes": self.attributes.__dict__,
        }

    @abstractmethod
    def predict_proba(self, *args, **kwargs):
        """
        Predict probability for the model.
        This is a wrapper around the model's if available
        """
        pass

    @abstractmethod
    def predict(self, *args, **kwargs):
        """
        Predict method for the model. This is a wrapper around the model's
        """
        pass

    @abstractmethod
    def model_language(self, *args, **kwargs):
        """
        Programming language used to train the model. Assume Python if this
        method is not implemented
        """
        pass

    @abstractmethod
    def model_library(self, *args, **kwargs):
        """
        Model framework library
        """
        pass

    @abstractmethod
    def model_library_version(self, *args, **kwargs):
        """
        Model framework library version
        """
        pass

    @abstractmethod
    def model_class(self, *args, **kwargs):
        """
        Predict method for the model. This is a wrapper around the model's
        """
        pass

    @abstractmethod
    def model_name(self, *args, **kwargs):
        """
        Model name
        """
        pass


def has_method_with_arguments(cls, method_name, n_args):
    if not hasattr(cls, method_name):
        return False

    method = getattr(cls, method_name)
    if not inspect.ismethod(method) and not inspect.isfunction(method):
        return False

    # Need to refine this logic since predict_proba can have
    # any number of arguments
    #
    # signature = inspect.signature(method)
    # parameters = signature.parameters

    # if len(parameters) != n_args:
    #     return False

    return True


def is_pytorch_model(model):
    """
    Checks if the model is a PyTorch model. Need to extend this
    method to check for all ways a PyTorch model can be created
    """
    # if we can't import torch, then it's not a PyTorch model
    try:
        import torch.nn as nn
    except ImportError:
        return False

    # return False
    # TBD. Fix setting PyTorch on Ubuntu
    return isinstance(model, nn.Module)


def model_module(model):
    if is_pytorch_model(model=model):
        return "torch"

    module = model.__class__.__module__.split(".")[0]

    if module == "__main__":
        return "custom"

    return module


def get_model_class(model):
    model_class_name = SUPPORTED_LIBRARIES.get(model_module(model), None)

    if model_class_name is None:
        raise Exception("Model library not supported")

    model_class = getattr(
        importlib.import_module("validmind.models"),
        model_class_name,
    )

    return model_class
