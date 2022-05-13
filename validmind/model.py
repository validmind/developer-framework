"""
Model class wrapper
"""
from dataclasses import dataclass, fields


@dataclass()
class ModelAttributes:
    """
    Model attributes definition
    """

    architecture: str = None
    framework: str = None
    framework_version: str = None


@dataclass()
class Model:
    """
    Model class wrapper
    """

    attributes: ModelAttributes
    task: str = None
    subtask: str = None
    params: dict = None
    model_id: str = "main"

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

    @classmethod
    def create_from_dict(cls, dict_):
        class_fields = {f.name for f in fields(cls)}
        return Model(**{k: v for k, v in dict_.items() if k in class_fields})
