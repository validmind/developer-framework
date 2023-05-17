"""
Model class wrapper
"""
from dataclasses import dataclass, fields
from .dataset import Dataset


# import torch
# import torch.nn as nn

SUPPORTED_MODEL_TYPES = [
    "catboost.CatBoostClassifier",
    "pytorch.PyTorchModel",
    "sklearn.LogisticRegression",
    "sklearn.LinearRegression",
    "sklearn.RandomForestClassifier",
    "statsmodels.GLMResultsWrapper",
    "statsmodels.BinaryResultsWrapper",  # Logistic Regression results
    "statsmodels.RegressionResultsWrapper",
    "xgboost.XGBClassifier",
    "xgboost.XGBRegressor",
]

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
class Model:
    """
    A class that wraps a trained model instance and its associated data.

    Attributes:
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
        task (str, optional): The task that the model is intended to solve. Defaults to None.
        subtask (str, optional): The subtask that the model is intended to solve. Defaults to None.
        params (dict, optional): The parameters of the model. Defaults to None.
        model_id (str): The identifier of the model. Defaults to "main".
        model (object, optional): The trained model instance. Defaults to None.
        train_ds (Dataset, optional): The training dataset. Defaults to None.
        test_ds (Dataset, optional): The test dataset. Defaults to None.
        validation_ds (Dataset, optional): The validation dataset. Defaults to None.
        y_train_predict (object, optional): The predicted outputs for the training dataset. Defaults to None.
        y_test_predict (object, optional): The predicted outputs for the test dataset. Defaults to None.
        y_validation_predict (object, optional): The predicted outputs for the validation dataset. Defaults to None.
    """

    attributes: ModelAttributes = None
    task: str = None
    subtask: str = None
    params: dict = None
    model_id: str = "main"
    model: object = None  # Trained model instance
    train_ds: Dataset = None
    test_ds: Dataset = None
    validation_ds: Dataset = None

    # These variables can be generated dynamically if not passed
    y_train_predict: object = None
    y_test_predict: object = None
    y_validation_predict: object = None

    def __post_init__(self):
        """
        Initializes the predicted outputs of the training, test, and validation datasets.
        """
        if self.model and self.train_ds:
            self.y_train_predict = self.predict(self.train_ds.x)
        if self.model and self.test_ds:
            self.y_test_predict = self.predict(self.test_ds.x)
        if self.model and self.validation_ds:
            self.y_validation_predict = self.predict(self.validation_ds.x)

    def serialize(self):
        """
        Serializes the model to a dictionary so it can be sent to the API
        """
        return {
            "model_id": self.model_id,
            "attributes": self.attributes.__dict__,
            "task": self.task,
            "subtask": self.subtask,
            "params": self.params,
        }

    def class_predictions(self, y_predict):
        """
        Converts a set of probability predictions to class predictions

        Args:
            y_predict (np.array, pd.DataFrame): Predictions to convert

        Returns:
            (np.array, pd.DataFrame): Class predictions
        """
        # TODO: parametrize at some point
        return (y_predict > 0.5).astype(int)

    @staticmethod
    def _is_pytorch_model(model):
        """
        Checks if the model is a PyTorch model. Need to extend this
        method to check for all ways a PyTorch model can be created
        """
        return False
        # TBD. Fix setting PyTorch on Ubuntu
        # return isinstance(model, nn.Module)

    def predict(self, *args, **kwargs):
        """
        Predict method for the model. This is a wrapper around the model's
        predict_proba (for classification) or predict (for regression) method

        NOTE: This only works for sklearn or xgboost models at the moment
        """
        if callable(getattr(self.model, "predict_proba", None)):
            return self.model.predict_proba(*args, **kwargs)[:, 1]
        if Model._is_pytorch_model(self.model):
            return []
            # input_df = args[0]
            # rest_args = args[1:]
            # input_values = torch.tensor(input_df.values, dtype=torch.float32)
            # predictions = self.model(input_values, *rest_args, **kwargs)
            # return predictions.detach().numpy()

        return self.model.predict(*args, **kwargs)

    @staticmethod
    def model_library(model):
        """
        Returns the model library name
        """
        if Model._is_pytorch_model(model):
            return "pytorch"

        return model.__class__.__module__.split(".")[0]

    @staticmethod
    def model_class(model):
        """
        Returns the model class name
        """
        if Model._is_pytorch_model(model):
            return "PyTorchModel"

        return model.__class__.__name__

    @staticmethod
    def is_supported_model(model):
        """
        Checks if the model is supported by the API

        Args:
            model (object): The trained model instance to check

        Returns:
            bool: True if the model is supported, False otherwise
        """
        return (
            f"{Model.model_library(model)}.{Model.model_class(model)}"
            in SUPPORTED_MODEL_TYPES
        )

    @classmethod
    def init_vm_model(cls, model, train_ds, test_ds, validation_ds, attributes):
        """
        Initializes a model instance from the provided data.
        """
        return cls(
            model=model,
            train_ds=train_ds,
            test_ds=test_ds,
            validation_ds=validation_ds,
            attributes=attributes,
        )

    @classmethod
    def create_from_dict(cls, dict_):
        """
        Creates a Model instance from a dictionary

        Args:
            dict_ (dict): The dictionary to create the Model instance from

        Returns:
            Model: The Model instance created from the dictionary
        """
        class_fields = {f.name for f in fields(cls)}
        return Model(**{k: v for k, v in dict_.items() if k in class_fields})
