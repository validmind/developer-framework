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


def _get_catboost_version():
    if "catboost" in sys.modules:
        return sys.modules["catboost"].__version__

    return "n/a"


def _get_pytorch_version():
    if "torch" in sys.modules:
        return sys.modules["torch"].__version__

    return "n/a"


def _get_sklearn_version():
    if "sklearn" in sys.modules:
        return sys.modules["sklearn"].__version__

    return "n/a"


def _get_statsmodels_version():
    if "statsmodels" in sys.modules:
        return sys.modules["statsmodels"].__version__

    return "n/a"


def _get_xgboost_objective(model):
    """
    Attempts to extract the model subtask (binary, multi-class, etc.)
    from the model's objective. Only binary classification is supported
    at the moment
    """
    if model.objective == "binary:logistic":
        return "binary"

    return "n/a"


def _get_xgboost_version():
    if "xgboost" in sys.modules:
        return sys.modules["xgboost"].__version__

    return "n/a"


def _get_model_info_from_statsmodels_summary(model):
    """
    Attempts to extract all model info from a statsmodels summary object
    """
    # summary2 is a pandas DataFrame
    summary = model.summary2()
    model_info = summary.tables[0]
    architecture = model_info[1][0]

    return {
        "architecture": architecture,
        "task": "regression",
        "subtask": "regression",
        "framework": "statsmodels",
        "framework_version": _get_statsmodels_version(),
    }


# TODO: refactor
def _get_info_from_model_instance(  # noqa C901 '_get_info_from_model_instance' is too complex
    model,
):
    """
    Attempts to extract all model info from a model object instance
    """
    model_class = Model.model_class(model)
    model_library = Model.model_library(model)

    if model_class == "XGBClassifier":
        architecture = "Extreme Gradient Boosting"
        task = "classification"
        subtask = _get_xgboost_objective(model)
        framework = "XGBoost"
        framework_version = _get_xgboost_version()
    elif model_class == "XGBRegressor":
        architecture = "Extreme Gradient Boosting"
        task = "regression"
        subtask = "regression"
        framework = "XGBoost"
        framework_version = _get_xgboost_version()
    elif model_class == "LogisticRegression":
        architecture = "Logistic Regression"
        task = "classification"
        subtask = "binary"
        framework = "Scikit-learn"
        framework_version = _get_sklearn_version()
    elif model_class == "LinearRegression":
        architecture = "Ordinary least squares Linear Regression"
        task = "regression"
        subtask = "regression"
        framework = "Scikit-learn"
        framework_version = _get_sklearn_version()
    elif model_class == "GLMResultsWrapper":
        architecture = "Generalized Linear Model (GLM)"
        task = "regression"
        subtask = "regression"
        framework = "statsmodels"
        framework_version = _get_statsmodels_version()
    elif model_class == "RandomForestClassifier":
        architecture = "Random Forest"
        task = "classification"
        subtask = "binary"
        framework = "Scikit-learn"
        framework_version = _get_sklearn_version()
    elif model_class == "BinaryResultsWrapper":
        architecture = "Logistic Regression"
        task = "classification"
        subtask = "binary"
        framework = "statsmodels"
        framework_version = _get_statsmodels_version()
    elif model_class == "PyTorchModel":
        architecture = "Neural Network"
        task = "classification"
        subtask = "binary"
        framework = "PyTorch"
        framework_version = _get_pytorch_version()
    elif model_class == "CatBoostClassifier":
        architecture = "Gradient Boosting"
        task = "classification"
        subtask = "binary"
        framework = "CatBoost"
        framework_version = _get_catboost_version()
    elif model_class == "RegressionResultsWrapper":
        return _get_model_info_from_statsmodels_summary(model)
    else:
        raise ValueError(
            f"Model type {model_library}.{model_class} is not supported by this test"
        )

    return {
        "architecture": architecture,
        "task": task,
        "subtask": subtask,
        "framework": framework,
        "framework_version": framework_version,
    }


# def _get_statsmodels_model_params(model):
#     """
#     Extracts the fit() method's parametesr from a
#     statsmodels model object instance

#     TODO: generalize to any statsmodels model
#     """
#     model_instance = model.model
#     family_class = model_instance.family.__class__.__name__
#     link_class = model_instance.family.link.__class__.__name__

#     return {
#         "family": SUPPORTED_STATSMODELS_FAMILIES.get(family_class, family_class),
#         "link": SUPPORTED_STATSMODELS_LINK_FUNCTIONS.get(link_class, link_class),
#         "formula": model_instance.formula,
#         "method": model.method,
#         "cov_type": model.cov_type,
#     }


def _get_params_from_model_instance(model):
    """
    Attempts to extract model hyperparameters from a model object instance
    """

    model_library = Model.model_library(model)

    # Only supports xgboot classifiers at the moment
    if model_library == "xgboost":
        params = model.get_xgb_params()
    elif model_library == "statsmodels":
        # params = _get_statsmodels_model_params(model)
        params = {}
    elif model_library == "sklearn":
        params = model.get_params()
    elif model_library == "pytorch":
        params = {}
    elif model_library == "catboost":
        params = model.get_all_params()
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
        This section describes attributes of the selected model such as its modeling
        technique, training parameters, and task type. This helps understand the model's
        capabilities and limitations in the context of a modeling framework.
        """

    def run(self):
        """
        Extracts model metadata from a model object instance
        """
        trained_model = self.model.model
        model_info = _get_info_from_model_instance(trained_model)
        model_info["language"] = f"Python {python_version()}"
        model_info["params"] = _get_params_from_model_instance(trained_model)

        return self.cache_results(model_info)
