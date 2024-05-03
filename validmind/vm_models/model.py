# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Model class wrapper module
"""
import importlib
import inspect
from abc import ABC, abstractmethod
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
    language: str = None

    @classmethod
    def from_dict(cls, data):
        """
        Creates a ModelAttributes instance from a dictionary
        """
        return cls(
            architecture=data.get("architecture"),
            framework=data.get("framework"),
            framework_version=data.get("framework_version"),
            language=data.get("language"),
        )


class VMModel(ABC):
    """
    An base class that wraps a trained model instance and its associated data.

    Attributes:
        model (object, optional): The trained model instance. Defaults to None.
        input_id (str, optional): The input ID for the model. Defaults to None.
        predict_col (str, optional): The output column name where predictions are stored.
          Defaults to the `input_id` plus `_prediction`.
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
        name (str, optional): The name of the model. Defaults to the class name.
    """

    predict_col: str = None

    def __init__(
        self,
        input_id: str = None,
        model: object = None,
        attributes: ModelAttributes = None,
        predict_col: str = None,
        name: str = None,
        **kwargs,
    ):
        self.model = model
        self.input_id = input_id or f"{id(self)}"
        self.predict_col = (
            predict_col or self.predict_col or f"{self.input_id}_prediction"
        )

        self.language = "Python"
        self.library = self.__class__.__name__
        self.library_version = "N/A"
        self.class_ = self.__class__.__name__

        self.name = name or self.__class__.__name__

        self.attributes = attributes

        # set any additional attributes passed in (likely for subclasses)
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.__post_init__()

    def __post_init__(self):
        """Allows child classes to add their own post-init logic"""
        pass

    def serialize(self):
        """
        Serializes the model to a dictionary so it can be sent to the API
        """
        return {
            "attributes": self.attributes.__dict__,
        }

    def predict_proba(self):
        """Predict probabilties - must be implemented by subclass if needed"""
        raise NotImplementedError

    @abstractmethod
    def predict(self, *args, **kwargs):
        """
        Predict method for the model. This is a wrapper around the model's
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
        return None

    model_class = getattr(
        importlib.import_module("validmind.models"),
        model_class_name,
    )

    return model_class


def is_model_metadata(model):
    """
    Checks if the model is a dictionary containing metadata about a model.
    We want to check if the metadata dictionary contains at least the following keys:

    - architecture
    - language
    """
    if not isinstance(model, dict):
        return False

    if "architecture" not in model:
        return False

    if "language" not in model:
        return False

    return True
