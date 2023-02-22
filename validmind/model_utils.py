"""
TODO: move this to new test plan based structure.

Utilities for inspecting client models
"""
import numpy as np

from scipy import stats
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from .vm_models import Metric

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


def _get_ols_summary_variable_metrics(model, x_train, y_train):
    """
    Builds an OLS summary table for the model's coefficients, similart
    to statsmodels. We log each metric as a separate ValidMind metric.

    We assumed the trained model is a linear regression model that
    exposes its coefficients as a .coef_ attribute

    https://stackoverflow.com/questions/27928275/find-p-value-significance-in-scikit-learn-linearregression
    """
    metrics = []

    # TODO: all utility functions should access the predicted values scope
    # that is passed to evaluate_model()
    predictions = model.predict(x_train)

    params = np.append(model.intercept_, model.coef_)

    # Add a column of ones for the intercept
    newX = np.append(np.ones((len(x_train), 1)), x_train, axis=1)

    MSE = (sum((y_train - predictions) ** 2)) / (len(newX) - len(newX[0]))

    var_b = MSE * (np.linalg.inv(np.dot(newX.T, newX)).diagonal())
    sd_b = np.sqrt(var_b)
    ts_b = params / sd_b

    p_val = [2 * (1 - stats.t.cdf(np.abs(i), (len(newX) - len(newX[0])))) for i in ts_b]

    # Extract coefficients, std err, t-stats and p-values
    coefficients = {
        feature_name: model.coef_[i] for i, feature_name in enumerate(x_train.columns)
    }
    coefficients["intercept"] = model.intercept_

    std_errors = {
        feature_name: sd_b[i + 1] for i, feature_name in enumerate(x_train.columns)
    }
    std_errors["intercept"] = sd_b[0]

    t_statistics = {
        feature_name: ts_b[i + 1] for i, feature_name in enumerate(x_train.columns)
    }
    t_statistics["intercept"] = ts_b[0]

    p_values = {
        feature_name: p_val[i + 1] for i, feature_name in enumerate(x_train.columns)
    }
    p_values["intercept"] = p_val[0]

    metrics.append(
        Metric(
            type="training",
            scope="training_dataset",
            key="coefficients",
            value=coefficients,
            value_formatter="key_values",
        )
    )

    metrics.append(
        Metric(
            type="training",
            scope="training_dataset",
            key="std_errors",
            value=std_errors,
            value_formatter="key_values",
        )
    )

    metrics.append(
        Metric(
            type="training",
            scope="training_dataset",
            key="t_statistics",
            value=t_statistics,
            value_formatter="key_values",
        )
    )

    metrics.append(
        Metric(
            type="training",
            scope="training_dataset",
            key="p_values",
            value=p_values,
            value_formatter="key_values",
        )
    )

    return metrics


def _get_statsmodels_summary_variable_metrics(model, x_train, y_train):
    """
    Builds an summary table for the model's coefficients for a statsmodels
    model instance. We log each metric as a separate ValidMind metric.

    https://stackoverflow.com/questions/51734180/converting-statsmodels-summary-object-to-pandas-dataframe
    """
    metrics = []

    summary_table = model.summary2().tables[1]
    summary_table_dict = summary_table.to_dict()

    metrics.append(
        Metric(
            type="training",
            scope="training_dataset",
            key="coefficients",
            value=summary_table_dict["Coef."],
            value_formatter="key_values",
        )
    )

    metrics.append(
        Metric(
            type="training",
            scope="training_dataset",
            key="std_errors",
            value=summary_table_dict["Std.Err."],
            value_formatter="key_values",
        )
    )

    metrics.append(
        Metric(
            type="training",
            scope="training_dataset",
            key="t_statistics",
            value=summary_table_dict["z"],
            value_formatter="key_values",
        )
    )

    metrics.append(
        Metric(
            type="training",
            scope="training_dataset",
            key="p_values",
            value=summary_table_dict["P>|z|"],
            value_formatter="key_values",
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

    vm_metrics.extend(_get_ols_summary_variable_metrics(model, x_train, y_train))

    return vm_metrics


def get_statsmodels_regression_metrics(model, x_train, y_train, x_val, y_val):
    """
    Attempts to extract model training metrics from a statsmodels model instance
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

    vm_metrics.extend(
        _get_statsmodels_summary_variable_metrics(model, x_train, y_train)
    )

    return vm_metrics


# def get_training_metrics(model, x_train, y_train, x_val=None, y_val=None):
#     """
#     Attempts to extract model training metrics from a model object instance
#     """
#     model_class = model.__class__.__name__

#     if not Model.is_supported_model(model):
#         raise ValueError(
#             "Model type {} is not supported at the moment.".format(model_class)
#         )

#     # Only supports xgboot classifiers at the moment
#     if model_class == "XGBClassifier":
#         metrics = get_xgb_classification_metrics(model, x_train, y_train, x_val, y_val)
#     elif model_class == "XGBRegressor":
#         metrics = get_xgb_regression_metrics(model, x_train, y_train, x_val, y_val)
#     elif model_class == "LinearRegression":
#         metrics = get_sklearn_regression_metrics(model, x_train, y_train, x_val, y_val)
#     elif model_class == "LogisticRegression":
#         metrics = []
#     elif model_class == "GLMResultsWrapper":
#         print("Refitting model...")
#         refitted = model.model.fit()
#         metrics = get_statsmodels_regression_metrics(
#             refitted, x_train, y_train, x_val, y_val
#         )

#     return metrics
