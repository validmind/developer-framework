# Copyright © 2023 ValidMind Inc. All rights reserved.


from dataclasses import dataclass

from validmind.vm_models import Metric


@dataclass
class ToxicityHistogram(Metric):
    """
    toxicity Histogram
    """

    name = "toxicity_histogram"
    default_params = {"text_columns": None}

    def description(self):
        return """
        Toxicity detailed description coming soon...!
        """

    def _determine_source(self):
        """
        Determine the source based on the existence of attributes.
        """

        # Checking attributes if they exist
        has_text_columns = (
            hasattr(self, "params") and self.params.get("text_columns") is not None
        )
        has_dataset = hasattr(self, "dataset")
        has_model = hasattr(self, "model.y_test_predict")

        # Conditions based on comments
        if not has_text_columns and not has_dataset and not has_model:
            raise ValueError("Neither text_columns, dataset nor model exist!")

        if not has_dataset and not has_model:
            raise ValueError("Neither dataset nor model exist!")

        # Determine the source
        if has_text_columns:
            return self.params["text_columns"]
        elif has_model:
            return (self.model.y_test_true, self.model.y_test_predict)
        elif has_dataset:
            return self.dataset

    def run(self):
        source = self._determine_source()
        # Use 'source' to compute toxicity
        # For demonstration purposes, just printing it.
        print(source)
