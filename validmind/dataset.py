"""
Dataset class wrapper
"""
from dataclasses import dataclass, fields


@dataclass()
class DatasetTargets:
    """
    Dataset targets definition
    """

    target_column: str
    class_labels: dict = None


@dataclass()
class Dataset:
    """
    Model class wrapper
    """

    fields: list
    sample: list
    shape: dict
    dataset_type: str = None
    statistics: dict = None
    targets: dict = None

    def serialize(self):
        """
        Serializes the model to a dictionary so it can be sent to the API
        """
        return {
            "fields": self.fields,
            "sample": self.sample,
            "shape": self.shape,
            "statistics": self.statistics,
            "targets": self.targets.__dict__,
            "type": self.dataset_type,
        }

    @classmethod
    def create_from_dict(cls, dict_):
        class_fields = {f.name for f in fields(cls)}
        return Dataset(**{k: v for k, v in dict_.items() if k in class_fields})
