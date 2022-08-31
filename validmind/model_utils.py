"""
Utilities for inspecting client models
"""
import sys

from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from .metrics.custom_metrics import csi, psi
from .models import Metric

DEFAULT_REGRESSION_METRICS = [
    "mae",
    "mse",
    "r2",
]

XGBOOST_EVAL_METRICS = {
    "binary": ["error", "logloss", "auc"],
    "multiclass": ["merror", "mlogloss", "auc"],
    "regression": [
        "mean_squared_error"
    ],  # TBD - how to compute more than one metric for regression?
}

SUPPORTED_MODEL_TYPES = ["XGBClassifier", "XGBRegressor", "LinearRegression"]


def get_xgboost_version():
    if "xgboost" in sys.modules:
        return sys.modules["xgboost"].__version__

    return "n/a"


def get_sklearn_version():
    if "sklearn" in sys.modules:
        return sys.modules["sklearn"].__version__

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


def _get_common_metrics(model, x_train, y_train, x_val, y_val):
    """
    Computes metrics that are common to any type of model being trained
    """
    metrics = []

    pfi_values = permutation_importance(
        model, x_train, y_train, random_state=0, n_jobs=-2
    )
    pfi = {}
    for i, column in enumerate(x_train.columns):
        pfi[column] = [pfi_values["importances_mean"][i]], [
            pfi_values["importances_std"][i]
        ]

    metrics.append(
        Metric(
            type="training",
            scope="training_dataset",
            key="pfi",
            value=pfi,
        )
    )

    # Check if model is a classification or regression model by
    # checking if it has a predict_proba method
    predict_fn = getattr(model, "predict_proba", None)
    if callable(predict_fn):
        y_train_predict = model.predict_proba(x_train)[:, 1]
        y_val_predict = model.predict_proba(x_val)[:, 1]
    else:
        y_train_predict = model.predict(x_train)
        y_val_predict = model.predict(x_val)

    metrics.append(
        Metric(
            type="training",
            scope="training:validation",
            key="psi",
            value=psi(y_train_predict, y_val_predict, as_dict=True),
        )
    )

    metrics.append(
        Metric(
            type="training",
            scope="training:validation",
            key="csi",
            value=csi(x_train, x_val),
        )
    )

    return metrics


def _get_metrics_from_evals_result(model, xgboost_metrics):
    """
    Generic function to extra a given list of metrics
    from an XGBoost evals_result object
    """
    evals_result = model.evals_result_
    vm_metrics = []

    # When passing eval_metrics to xgboost, we expect validation_0 to be
    # the training dataset metrics and validation_1 to be validation dataset metrics
    if "validation_0" in evals_result:
        for metric_name in xgboost_metrics:
            if metric_name in evals_result["validation_0"]:
                vm_metrics.append(
                    Metric(
                        type="training",
                        scope="training_dataset",
                        key=metric_name,
                        value=evals_result["validation_0"][metric_name],
                    )
                )
    if "validation_1" in evals_result:
        for metric_name in xgboost_metrics:
            if metric_name in evals_result["validation_1"]:
                vm_metrics.append(
                    Metric(
                        type="training",
                        scope="validation_dataset",
                        key=metric_name,
                        value=evals_result["validation_1"][metric_name],
                    )
                )

    return vm_metrics


def get_xgb_classification_metrics(model, x_train, y_train, x_val, y_val):
    """
    Converts XGBoost evals_result to our standard metrics format
    """
    num_class = y_train.nunique()
    predict_problem = "binary" if num_class == 2 else "multi-class"
    xgboost_metrics = XGBOOST_EVAL_METRICS[predict_problem]

    vm_metrics = _get_metrics_from_evals_result(model, xgboost_metrics)
    vm_metrics.extend(_get_common_metrics(model, x_train, y_train, x_val, y_val))

    return vm_metrics


def get_xgb_regression_metrics(model, x_train, y_train, x_val, y_val):
    """
    Converts XGBoost evals_result to our standard metrics format
    """
    xgboost_metrics = XGBOOST_EVAL_METRICS["regression"]

    vm_metrics = _get_metrics_from_evals_result(model, xgboost_metrics)
    # Our xgb model is sklearn compatible, so we can use sklearn's metrics
    vm_metrics.extend(
        get_sklearn_regression_metrics(model, x_train, y_train, x_val, y_val)
    )

    return vm_metrics


def get_sklearn_regression_metrics(model, x_train, y_train, x_val, y_val):
    """
    Attempts to extract model training metrics from a model object instance
    """
    # TODO: support overriding metrics
    metric_names = DEFAULT_REGRESSION_METRICS

    vm_metrics = []

    # Log training and validation dataset metrics separately
    dataset_tuples = (
        (x_train, y_train, "training_dataset"),
        (x_val, y_val, "validation_dataset"),
    )

    for x, y, dataset_scope in dataset_tuples:
        y_pred = model.predict(x)

        for metric_name in metric_names:
            if metric_name == "mae":
                metric_value = mean_absolute_error(y, y_pred)
            elif metric_name == "mse":
                metric_value = mean_squared_error(y, y_pred)
            elif metric_name == "r2":
                metric_value = r2_score(y, y_pred)

            vm_metrics.append(
                Metric(
                    type="training",
                    scope=dataset_scope,
                    key=metric_name,
                    value=[metric_value],
                )
            )

    # Linear model coefficients
    coef = model.coef_
    coefficients = {
        feature_name: coef[i] for i, feature_name in enumerate(x_train.columns)
    }
    coefficients["intercept"] = model.intercept_

    vm_metrics.append(
        Metric(
            type="training",
            scope="training_dataset",
            key="coefficients",
            value=coefficients,
        )
    )

    vm_metrics.extend(_get_common_metrics(model, x_train, y_train, x_val, y_val))

    return vm_metrics


def get_info_from_model_instance(model):
    """
    Attempts to extract all model info from a model object instance
    """
    model_class = model.__class__.__name__

    if model_class not in SUPPORTED_MODEL_TYPES:
        raise ValueError(
            "Model type {} is not supported at the moment.".format(model_class)
        )

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
    elif model_class == "LinearRegression":
        architecture = "Ordinary least squares Linear Regression"
        task = "regression"
        subtask = "regression"
        framework = "Scikit-learn"
        framework_version = get_sklearn_version()

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

    if model_class not in SUPPORTED_MODEL_TYPES:
        raise ValueError(
            "Model type {} is not supported at the moment.".format(model_class)
        )

    # Only supports xgboot classifiers at the moment
    if model_class == "XGBClassifier" or model_class == "XGBRegressor":
        params = model.get_xgb_params()
    # SKLearn models at the moment
    else:
        params = model.get_params()

    return params


def get_training_metrics(model, x_train, y_train, x_val=None, y_val=None):
    """
    Attempts to extract model training metrics from a model object instance
    """
    model_class = model.__class__.__name__

    if model_class not in SUPPORTED_MODEL_TYPES:
        raise ValueError(
            "Model type {} is not supported at the moment.".format(model_class)
        )

    # Only supports xgboot classifiers at the moment
    if model_class == "XGBClassifier":
        metrics = get_xgb_classification_metrics(model, x_train, y_train, x_val, y_val)
    elif model_class == "XGBRegressor":
        metrics = get_xgb_regression_metrics(model, x_train, y_train, x_val, y_val)
    elif model_class == "LinearRegression":
        metrics = get_sklearn_regression_metrics(model, x_train, y_train, x_val, y_val)

    return metrics
