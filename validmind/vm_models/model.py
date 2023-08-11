# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Model class wrapper module
"""
import inspect

from abc import ABC, abstractmethod
from dataclasses import dataclass
from .dataset import VMDataset
from ..errors import MissingPytorchModelPredictError

import importlib


SUPPORTED_LIBRARIES = {
    "catboost": "CatBoostModel",
    "xgboost": "XGBoostModel",
    "sklearn": "SKlearnModel",
    "torch": "PyTorchModel",
    "statsmodels": "StatsModelsModel",
}

R_MODEL_TYPES = [
    "LogisticRegression",
    "LinearRegression",
    "XGBClassifier",
    "XGBRegressor",
]


@dataclass()
class ModelAttributes:
    """
    Model attributes definition
    """

    architecture: str = None
    framework: str = None
    framework_version: str = None


@dataclass
class VMModel(ABC):
    """
    An abstract base class that wraps a trained model instance and its associated data.

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
    def model_library(self, *args, **kwargs):
        """
        Predict method for the model. This is a wrapper around the model's
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

    @abstractmethod
    def is_pytorch_model(self):
        pass


@dataclass
class SKlearnModel(VMModel):
    """
    An SKlearn model class that wraps a trained model instance and its associated data.

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
            self._y_train_predict = self.predict(self.train_ds.x)
        if self.model and self.test_ds:
            self._y_test_predict = self.predict(self.test_ds.x)
        if self.model and self.validation_ds:
            self._y_validation_predict = self.predict(self.validation_ds.x)

    def predict_proba(self, *args, **kwargs):
        """
        predict_proba (for classification) or predict (for regression) method
        """
        if callable(getattr(self.model, "predict_proba", None)):
            return self.model.predict_proba(*args, **kwargs)[:, 1]
        return None

    def predict(self, *args, **kwargs):
        """
        Predict method for the model. This is a wrapper around the model's
        """
        return self.model.predict(*args, **kwargs)

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


@dataclass
class XGBoostModel(SKlearnModel):
    """
    An XGBoost model class that wraps a trained model instance and its associated data.

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
        super().__init__(
            model=model,
            train_ds=train_ds,
            test_ds=test_ds,
            validation_ds=validation_ds,
            attributes=attributes,
        )


@dataclass
class CatBoostModel(SKlearnModel):
    """
    An CatBoost model class that wraps a trained model instance and its associated data.

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
        """
        Initialize CatBoostModel
        """
        super().__init__(
            model=model,
            train_ds=train_ds,
            test_ds=test_ds,
            validation_ds=validation_ds,
            attributes=attributes,
        )


@dataclass
class StatsModelsModel(SKlearnModel):
    """
    An Statsmodels model class that wraps a trained model instance and its associated data.

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


@dataclass
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
            self._y_train_predict = self.predict(self.train_ds.x)
        if self.model and self.test_ds:
            self._y_test_predict = self.predict(self.test_ds.x)
        if self.model and self.validation_ds:
            self._y_validation_predict = self.predict(self.validation_ds.x)

        self._device_type = next(self.model.parameters()).device

    def predict_proba(self, *args, **kwargs):
        """
        Invoke predict_proba from underline model
        """
        if not has_method_with_arguments(self.model, "predict_proba", 1):
            raise MissingPytorchModelPredictError(
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
            raise MissingPytorchModelPredictError(
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

    def is_pytorch_model(self):
        return self.model_library() == "torch"

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


def has_method_with_arguments(cls, method_name, n_args):
    if not hasattr(cls, method_name):
        return False

    method = getattr(cls, method_name)
    if not inspect.ismethod(method) and not inspect.isfunction(method):
        return False

    signature = inspect.signature(method)
    parameters = signature.parameters

    if len(parameters) != n_args:
        return False

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
    module = model.__class__.__module__.split(".")[0]
    if module != "__main__":
        return module
    # pyTorch liabrary
    if is_pytorch_model(model=model):
        return "torch"


def get_model_class(model):
    class_name = SUPPORTED_LIBRARIES.get(model_module(model), None)
    if class_name:
        module = importlib.import_module(__name__)
        return getattr(module, class_name)
    return None
