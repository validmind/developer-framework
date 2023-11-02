# Copyright © 2023 ValidMind Inc. All rights reserved.

import sys
from dataclasses import dataclass
from platform import python_version

import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable


def _get_info_from_model_instance(  # noqa C901 '_get_info_from_model_instance' is too complex
    model,
):
    """Attempts to extract all model info from a model object instance"""
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
    Extracts and summarizes critical metadata from a machine learning model instance for comprehensive analysis.

    **Purpose:**
    This test is designed to collect and summarize important metadata related to a particular machine learning model.
    Such metadata includes the model's architecture (modeling technique), the version and type of modeling framework
    used, and the programming language the model is written in.

    **Test Mechanism:**
    The mechanism of this test consists of extracting information from the model instance. It tries to extract the
    model information such as the modeling technique used, the modeling framework version, and the programming
    language. It decorates this information into a data frame and returns a summary of the results.

    **Signs of High Risk:**

    - High risk could be determined by a lack of documentation or inscrutable metadata for the model.
    - Unidentifiable language, outdated or unsupported versions of modeling frameworks, or undisclosed model
    architectures reflect risky situations, as they could hinder future reproducibility, support, and debugging of the
    model.

    **Strengths:**

    - The strengths of this test lie in the increased transparency and understanding it brings regarding the model's
    setup.
    - Knowing the model's architecture, the specific modeling framework version used, and the language involved,
    provides multiple benefits: supports better error understanding and debugging, facilitates model reuse, aids
    compliance of software policies, and assists in planning for model obsolescence due to evolving or discontinuing
    software and dependencies.

    **Limitations:**

    - Notably, this test is largely dependent on the compliance and correctness of information provided by the model or
    the model developer.
    - If the model's built-in methods for describing its architecture, framework or language are incorrect or lack
    necessary information, this test will hold limitations.
    - Moreover, it is not designed to directly evaluate the performance or accuracy of the model, rather it provides
    supplementary information which aids in comprehensive analysis.
    """

    name = "model_metadata"
    required_inputs = ["model"]
    metadata = {
        "task_types": [
            "classification",
            "regression",
            "text_classification",
            "text_summarization",
        ],
        "tags": ["model_metadata"],
    }

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

    def run(self):
        """
        Extracts model metadata from a model object instance
        """
        model_info = _get_info_from_model_instance(self.model)

        return self.cache_results(model_info)
