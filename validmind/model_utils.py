"""
Utilities for inspecting client models
"""
import sys


def get_xgboost_version():
    if "xgboost" in sys.modules:
        return sys.modules["xgboost"].__version__

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


def get_info_from_model_instance(model):
    """
    Attempts to extract all model info from a model object instance
    """
    model_class = model.__class__.__name__

    # Only supports xgboot classifiers at the moment
    if model_class == "XGBClassifier":
        architecture = "Extreme Gradient Boosting"
        task = "classification"
        subtask = get_xgboost_objective(model)
        framework = "XGBoost"
        framework_version = get_xgboost_version()

    return {
        "architecture": architecture,
        "task": task,
        "subtask": subtask,
        "framework": framework,
        "framework_version": framework_version,
    }


def get_params_from_model_instance(model):
    """
    Attempts to extract model hyperparameters from a model object instance
    """
    model_class = model.__class__.__name__

    # Only supports xgboot classifiers at the moment
    if model_class == "XGBClassifier":
        params = model.get_xgb_params()

    return params
