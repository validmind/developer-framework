"""
Utilities for inspecting client models
"""
import sys

from sklearn.inspection import permutation_importance

XGBOOST_EVAL_METRICS = {
    "binary": ["error", "logloss", "auc"],
    "multiclass": ["merror", "mlogloss", "auc"],
}


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


def get_xgb_train_metrics(model, x_train, y_train):
    """
    Converts XGBoost evals_result to our standard
    """
    num_class = y_train.nunique()
    predict_problem = "binary" if num_class == 2 else "multi-class"
    xgboost_metrics = XGBOOST_EVAL_METRICS[predict_problem]
    evals_result = model.evals_result_

    metrics = []

    # When passing eval_metrics to xgboost, we expect validation_0 to be
    # the training dataset metrics and validation_1 to be validation dataset metrics
    if "validation_0" in evals_result:
        for metric_name in xgboost_metrics:
            if metric_name in evals_result["validation_0"]:
                metrics.append(
                    {
                        "type": "training",
                        "scope": "training_dataset",
                        "key": metric_name,
                        "value": evals_result["validation_0"][metric_name],
                    }
                )
    if "validation_1" in evals_result:
        for metric_name in xgboost_metrics:
            if metric_name in evals_result["validation_1"]:
                metrics.append(
                    {
                        "type": "training",
                        "scope": "validation_dataset",
                        "key": metric_name,
                        "value": evals_result["validation_1"][metric_name],
                    }
                )

    pfi_values = permutation_importance(
        model, x_train, y_train, random_state=0, n_jobs=-2
    )
    pfi = {}
    for i, column in enumerate(x_train.columns):
        pfi[column] = [pfi_values["importances_mean"][i]], [
            pfi_values["importances_std"][i]
        ]

    metrics.append(
        {
            "type": "training",
            "scope": "training_dataset",
            "key": "pfi",
            "value": pfi,
        }
    )

    return metrics


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
    else:
        raise ValueError("Only XGBoost models are supported at the moment.")

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
    else:
        raise ValueError("Only XGBoost models are supported at the moment.")

    return params


def get_training_metrics(model, x_train, y_train):
    """
    Attempts to extract model training metrics from a model object instance
    """
    model_class = model.__class__.__name__

    # Only supports xgboot classifiers at the moment
    if model_class == "XGBClassifier":
        metrics = get_xgb_train_metrics(model, x_train, y_train)
    else:
        raise ValueError("Only XGBoost models are supported at the moment.")

    return metrics
