from dataclasses import dataclass

from validmind.vm_models import Metric


@dataclass
class DatasetDescription(Metric):
    """
    Collects a set of descriptive statistics for a dataset
    """

    name = "dataset_description"
    required_context = ["dataset"]

    def __post_init__(self):
        self.scope = self.dataset.type

    def run(self):
        # This will populate the "fields" attribute in the dataset object
        self.dataset.describe()
        return self.cache_results(self.dataset.fields)
