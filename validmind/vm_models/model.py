# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Model class wrapper module
"""
import importlib
import inspect
from abc import abstractmethod
from dataclasses import dataclass

from .dataset import VMDataset

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
        model: object = None,
        train_ds: VMDataset = None,
        test_ds: VMDataset = None,
        validation_ds: VMDataset = None,
        attributes: ModelAttributes = None,
    ):
        self._model = model
        self._train_ds = train_ds
        self._test_ds = test_ds
        self._validation_ds = validation_ds
        self._attributes = attributes

        # These variables can be generated dynamically if not passed
        self._y_train_predict = None
        self._y_test_predict = None
        self._y_validation_predict = None

        # The device where model is trained
        self._device_type = None

    @property
    def attributes(self):
        return self._attributes

    @property
    def model(self):
        return self._model

    @property
    def train_ds(self):
        return self._train_ds

    @property
    def test_ds(self):
        return self._test_ds

    @property
    def validation_ds(self):
        return

    @property
    def y_train_true(self):
        """
        This variable can be generated dynamically
        """
        return self.train_ds.y

    @property
    def y_test_true(self):
        """
        This variable can be generated dynamically
        """
        return self.test_ds.y

    @property
    def y_train_predict(self):
        """
        This variable can be generated dynamically
        """
        return self._y_train_predict

    @property
    def y_test_predict(self):
        """
        This variable can be generated dynamically
        """
        return self._y_test_predict

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
