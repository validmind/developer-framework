import sys

from dataclasses import dataclass
from platform import python_version

import pandas as pd

from ..vm_models import Metric, Model, ResultSummary, ResultTable

SUPPORTED_STATSMODELS_FAMILIES = {
    "statsmodels.genmod.families.family.Poisson": "poisson",
    "statsmodels.genmod.families.family.Gaussian": "gaussian",
}

SUPPORTED_STATSMODELS_LINK_FUNCTIONS = {
    "statsmodels.genmod.families.links.log": "log",
    "statsmodels.genmod.families.links.identity": "identity",
}


def get_pytorch_version():
    if "torch" in sys.modules:
        return sys.modules["torch"].__version__

    return "n/a"


def get_sklearn_version():
    if "sklearn" in sys.modules:
        return sys.modules["sklearn"].__version__

    return "n/a"


def get_statsmodels_version():
    if "statsmodels" in sys.modules:
        return sys.modules["statsmodels"].__version__

    return "n/a"


def get_xgboost_objective(model):
    """
    Attempts to extract the model subtask (binary, multi-class, etc.)
    from the model's objective. Only binary classification is supported
    at the moment
    """
    if model.objective == "binary:logistic":
        return "binary"

    return "n/a"


def get_xgboost_version():
    if "xgboost" in sys.modules:
        return sys.modules["xgboost"].__version__

    return "n/a"


def get_info_from_model_instance(model):
    """
    Attempts to extract all model info from a model object instance
    """
    model_class = Model.model_class(model)

    # TODO: refactor
    if model_class == "XGBClassifier":
        architecture = "Extreme Gradient Boosting"
        task = "classification"
        subtask = get_xgboost_objective(model)
        framework = "XGBoost"
        framework_version = get_xgboost_version()
    elif model_class == "XGBRegressor":
        architecture = "Extreme Gradient Boosting"
        task = "regression"
        subtask = "regression"
        framework = "XGBoost"
        framework_version = get_xgboost_version()
    elif model_class == "LogisticRegression":
        architecture = "Logistic Regression"
        task = "classification"
        subtask = "binary"
        framework = "Scikit-learn"
        framework_version = get_sklearn_version()
    elif model_class == "LinearRegression":
        architecture = "Ordinary least squares Linear Regression"
        task = "regression"
        subtask = "regression"
        framework = "Scikit-learn"
        framework_version = get_sklearn_version()
    elif model_class == "GLMResultsWrapper":
        architecture = "Generalized Linear Model (GLM)"
        task = "regression"
        subtask = "regression"
        framework = "statsmodels"
        framework_version = get_statsmodels_version()
    elif model_class == "RandomForestClassifier":
        architecture = "Random Forest"
        task = "classification"
        subtask = "binary"
        framework = "Scikit-learn"
        framework_version = get_sklearn_version()
    elif model_class == "BinaryResultsWrapper":
        architecture = "Logistic Regression"
        task = "classification"
        subtask = "binary"
        framework = "statsmodels"
        framework_version = get_statsmodels_version()
    elif model_class == "PyTorchModel":
        architecture = "Neural Network"
        task = "classification"
        subtask = "binary"
        framework = "PyTorch"
        framework_version = get_pytorch_version()
    else:
        raise ValueError(f"Model class {model_class} is not supported by this test")

    return {
        "architecture": architecture,
        "task": task,
        "subtask": subtask,
        "framework": framework,
        "framework_version": framework_version,
    }


def get_statsmodels_model_params(model):
    """
    Extracts the fit() method's parametesr from a
    statsmodels model object instance

    # TODO: generalizer to any statsmodels model
    """
    model_instance = model.model
    family_class = model_instance.family.__class__.__name__
    link_class = model_instance.family.link.__class__.__name__

    return {
        "family": SUPPORTED_STATSMODELS_FAMILIES.get(family_class, family_class),
        "link": SUPPORTED_STATSMODELS_LINK_FUNCTIONS.get(link_class, link_class),
        "formula": model_instance.formula,
        "method": model.method,
        "cov_type": model.cov_type,
    }


def get_params_from_model_instance(model):
    """
    Attempts to extract model hyperparameters from a model object instance
    """

    model_library = Model.model_library(model)

    # Only supports xgboot classifiers at the moment
    if model_library == "xgboost":
        params = model.get_xgb_params()
    elif model_library == "statsmodels":
        # params = get_statsmodels_model_params(model)
        params = {}
    elif model_library == "sklearn":
        params = model.get_params()
    elif model_library == "pytorch":
        params = {}
    else:
        raise ValueError(f"Model library {model_library} is not supported by this test")

    return params


@dataclass
class ModelMetadata(Metric):
    """
    Custom class to collect the following metadata for a model:
    - Model architecture
    - Model hyperparameters
    - Model task type
    """

    name = "model_metadata"
    required_context = ["model"]

    column_labels = {
        "architecture": "Modeling Technique",
        "framework": "Modeling Framework",
        "framework_version": "Framework Version",
        "language": "Programming Language",
        "subtask": "Modeling Subtask",
        "task": "Modeling Task",
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
        The model metadata test collects attributes about the model such as
        the model architecture, training parameters, and task type. This helps
        understand the model's capabilities and limitations in the context of
        a modeling framework.
        """.strip()

    def run(self):
        """
        Extracts model metadata from a model object instance
        """
        trained_model = self.model.model
        model_info = get_info_from_model_instance(trained_model)
        model_info["language"] = f"Python {python_version()}"
        model_info["params"] = get_params_from_model_instance(trained_model)

        return self.cache_results(model_info)
