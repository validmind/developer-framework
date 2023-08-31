# Copyright © 2023 ValidMind Inc. All rights reserved.

import sys
from dataclasses import dataclass
from platform import python_version

import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable


def _get_info_from_model_instance(  # noqa C901 '_get_info_from_model_instance' is too complex
    model,
):
    """
    Attempts to extract all model info from a model object instance
    """
    architecture = model.model_name()
    framework = model.model_library()
    framework_version = model.model_library_version()
    language = model.model_language()

    if language is None:
        language = f"Python {python_version()}"

    if framework_version is None:
        try:
            framework_version = sys.modules[framework].__version__
        except (KeyError, AttributeError):
            framework_version = "N/A"

    return {
        "architecture": architecture,
        "framework": framework,
        "framework_version": framework_version,
        "language": language,
    }


@dataclass
class ModelMetadata(Metric):
    """
    Custom class to collect the following metadata for a model:
    - Model architecture
    """

    name = "model_metadata"
    required_inputs = ["model"]

    column_labels = {
        "architecture": "Modeling Technique",
        "framework": "Modeling Framework",
        "framework_version": "Framework Version",
        "language": "Programming Language",
    }

    def summary(self, metric_value):
        df = pd.DataFrame(metric_value.items(), columns=["Attribute", "Value"])
        # Don't serialize the params attribute
        df = df[df["Attribute"] != "params"]
        df["Attribute"] = df["Attribute"].map(self.column_labels)

        return ResultSummary(
            results=[
                ResultTable(data=df.to_dict(orient="records")),
            ]
        )

    def description(self):
        return """
        This section describes attributes of the selected model such as its modeling
        technique, training parameters, and task type. This helps understand the model's
        capabilities and limitations in the context of a modeling framework.
        """

    def run(self):
        """
        Extracts model metadata from a model object instance
        """
        model_info = _get_info_from_model_instance(self.model)

        return self.cache_results(model_info)
