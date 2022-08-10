"""
Dataset class wrapper
"""
from dataclasses import dataclass, field, fields


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

    fields: list  # TODO - deprecate naming in favor of features
    sample: list
    shape: dict
    correlations: dict = None
    dataset_type: str = None
    dataset_options: dict = None
    statistics: dict = None
    targets: dict = None
    __feature_lookup: dict = field(default_factory=dict)

    def get_feature_by_id(self, feature_id):
        """
        Returns the feature with the given id. We also build a lazy
        lookup cache in case the same feature is requested multiple times.
        """
        if feature_id not in self.__feature_lookup:
            for feature in self.fields:
                if feature["id"] == feature_id:
                    self.__feature_lookup[feature_id] = feature
                    return feature
            raise ValueError(f"Feature with id {feature_id} does not exist")

        return self.__feature_lookup[feature_id]

    def get_feature_type(self, feature_id):
        """
        Returns the type of the feature with the given id
        """
        feature = self.get_feature_by_id(feature_id)
        return feature["type"]

    def serialize(self):
        """
        Serializes the model to a dictionary so it can be sent to the API
        """
        dataset_dict = {
            "correlations": self.correlations,
            "fields": self.fields,
            "sample": self.sample,
            "shape": self.shape,
            "statistics": self.statistics,
            "type": self.dataset_type,
        }

        # Dataset with no targets can be logged
        if self.targets:
            dataset_dict["targets"] = self.targets.__dict__

        return dataset_dict

    @classmethod
    def create_from_dict(cls, dict_):
        class_fields = {f.name for f in fields(cls)}
        return Dataset(**{k: v for k, v in dict_.items() if k in class_fields})
