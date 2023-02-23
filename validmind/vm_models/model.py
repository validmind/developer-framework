"""
Model class wrapper
"""
from dataclasses import dataclass, fields

SUPPORTED_MODEL_TYPES = [
    "GLMResultsWrapper",
    "XGBClassifier",
    "XGBRegressor",
    "LogisticRegression",
    "LinearRegression",
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
    Model class wrapper
    """

    attributes: ModelAttributes = None
    task: str = None
    subtask: str = None
    params: dict = None
    model_id: str = "main"
    model: object = None  # Trained model instance

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

    def predict(self, *args, **kwargs):
        """
        Predict method for the model. This is a wrapper around the model's
        predict_proba (for classification) or predict (for regression) method

        NOTE: This only works for sklearn or xgboost models at the moment
        """
        predict_fn = getattr(self.model, "predict_proba", None)
        if callable(predict_fn):
            return self.model.predict_proba(*args, **kwargs)[:, 1]
        else:
            return self.model.predict(*args, **kwargs)

    @classmethod
    def is_supported_model(cls, model):
        """
        Checks if the model is supported by the API
        """
        model_class = model.__class__.__name__

        if model_class not in SUPPORTED_MODEL_TYPES:
            return False

        return True

    @classmethod
    def create_from_dict(cls, dict_):
        class_fields = {f.name for f in fields(cls)}
        return Model(**{k: v for k, v in dict_.items() if k in class_fields})
