"""
Model Evaluation Tests. Currently we only support
models that have a sklearn compatible metrics interface
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import shap
from sklearn import metrics
from sklearn.inspection import permutation_importance as pfi_sklearn
from sklearn.metrics import (
    confusion_matrix as cfm_sklearn,
    roc_curve as roc_curve_sklearn,
    precision_recall_curve as prc_sklearn,
    mean_absolute_error as mean_absolute_error_sklearn,
    mean_squared_error as mean_squared_error_sklearn,
    r2_score as r2_score_sklearn,
)

from .config import TestResult, TestResults


def accuracy_score(y_true, y_pred=None, rounded_y_pred=None, config=None):
    """
    Compute accuracy score metric from sklearn.
    """
    score = metrics.accuracy_score(y_true, rounded_y_pred)
    evaluation_metrics = {
        "type": "evaluation",
        "scope": "test",
        "key": "accuracy",
        "value": [score],
    }

    test_params = {
        "min_percent_threshold": config.accuracy_score.min_percent_threshold,
    }

    passed = score > test_params["min_percent_threshold"]

    test_result = TestResults(
        category="model_performance",
        test_name="accuracy_score",
        params=test_params,
        passed=passed,
        results=[
            TestResult(
                passed=passed,
                values={
                    "score": score,
                    "threshold": test_params["min_percent_threshold"],
                },
            )
        ],
    )

    return evaluation_metrics, test_result


def confusion_matrix(y_true, y_pred=None, rounded_y_pred=None):
    """
    Compute confusion matrix values from sklearn.
    """
    y_labels = list(map(lambda x: x.item(), y_true.unique()))
    y_labels.sort()

    tn, fp, fn, tp = cfm_sklearn(y_true, rounded_y_pred, labels=y_labels).ravel()
    return {
        "type": "evaluation",
        "scope": "test",
        "key": "confusion_matrix",
        "value": {
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "tp": tp,
        },
    }


def f1_score(y_true, y_pred=None, rounded_y_pred=None, config=None):
    """
    Compute f1 score metric from sklearn.
    """

    score = metrics.f1_score(y_true, rounded_y_pred)

    evaluation_metrics = {
        "type": "evaluation",
        "scope": "test",
        "key": "f1_score",
        "value": [score],
    }

    test_params = {
        "min_threshold": config.f1_score.min_threshold,
    }

    passed = score > test_params["min_threshold"]

    test_result = TestResults(
        category="model_performance",
        test_name="f1_score",
        params=test_params,
        passed=passed,
        results=[
            TestResult(
                passed=passed,
                values={"score": score, "threshold": test_params["min_threshold"]},
            )
        ],
    )

    return evaluation_metrics, test_result


def mae_score(y_true, y_pred):
    """
    Compute Mean Absolute Error score metric from sklearn.
    """
    return {
        "type": "evaluation",
        "scope": "test",
        "key": "mae",
        "value": [mean_absolute_error_sklearn(y_true, y_pred)],
    }


def mse_score(y_true, y_pred):
    """
    Compute Mean Squared Error score metric from sklearn.
    """
    return {
        "type": "evaluation",
        "scope": "test",
        "key": "mse",
        "value": [mean_squared_error_sklearn(y_true, y_pred)],
    }


def permutation_importance(model, x_test, y_test):
    """
    Compute permutation feature importance (PFI) values from sklearn.
    """
    r = pfi_sklearn(model, x_test, y_test, random_state=0)
    pfi = {}

    for i, column in enumerate(x_test.columns):
        pfi[column] = [r["importances_mean"][i]], [r["importances_std"][i]]

    return {
        "type": "evaluation",
        "scope": "test",
        "key": "pfi",
        "value": pfi,
    }


def precision_recall_curve(y_true, y_pred=None, rounded_y_pred=None):
    """
    Compute precision recall curve values from sklearn.
    """
    precision, recall, pr_thresholds = prc_sklearn(y_true, y_pred)
    return {
        "type": "evaluation",
        "scope": "test",
        "key": "pr_curve",
        "value": {
            "precision": precision,
            "recall": recall,
            "thresholds": pr_thresholds,
        },
    }


def precision_score(y_true, y_pred=None, rounded_y_pred=None):
    """
    Compute precision score metric from sklearn.
    """
    return {
        "type": "evaluation",
        "scope": "test",
        "key": "precision",
        "value": [metrics.precision_score(y_true, rounded_y_pred)],
    }


def recall_score(y_true, y_pred=None, rounded_y_pred=None):
    """
    Compute recall score metric from sklearn.
    """
    return {
        "type": "evaluation",
        "scope": "test",
        "key": "recall",
        "value": [metrics.recall_score(y_true, rounded_y_pred)],
    }


def roc_auc_score(y_true, y_pred=None, rounded_y_pred=None, config=None):
    """
    Compute ROC AUC score metric from sklearn.
    """

    score = metrics.roc_auc_score(y_true, rounded_y_pred)

    evaluation_metrics = {
        "type": "evaluation",
        "scope": "test",
        "key": "roc_auc",
        "value": [score],
    }

    test_params = {
        "min_threshold": config.roc_auc_score.min_threshold,
    }

    passed = score > test_params["min_threshold"]

    test_result = TestResults(
        category="model_performance",
        test_name="roc_auc_score",
        params=test_params,
        passed=passed,
        results=[
            TestResult(
                passed=passed,
                values={"score": score, "threshold": test_params["min_threshold"]},
            )
        ],
    )

    return evaluation_metrics, test_result


def roc_curve(y_true, y_pred=None, rounded_y_pred=None):
    """
    Compute ROC curve values from sklearn.
    """
    fpr, tpr, roc_thresholds = roc_curve_sklearn(y_true, y_pred, drop_intermediate=True)
    return {
        "type": "evaluation",
        "scope": "test",
        "key": "roc_curve",
        "value": {
            "fpr": fpr,
            "tpr": tpr,
            "thresholds": roc_thresholds,
        },
    }


def r2_score(y_true, y_pred):
    """
    Compute R-Squared score metric from sklearn.
    """
    return {
        "type": "evaluation",
        "scope": "test",
        "key": "r2",
        "value": [r2_score_sklearn(y_true, y_pred)],
    }


def _generate_shap_plot(type_, shap_values, x_test):
    """
    Plots two types of SHAP global importance (SHAP).
    :params type: mean, summary
    :params shap_values: a matrix
    :params x_test:
    """
    # preserve styles
    mpl.rcParams["grid.color"] = "#CCC"
    ax = plt.axes()
    ax.set_facecolor("white")

    summary_plot_extra_args = {}
    if type_ == "mean":
        summary_plot_extra_args = {"plot_type": "bar", "color": "#DE257E"}

    shap.summary_plot(shap_values, x_test, show=False, **summary_plot_extra_args)
    figure = plt.gcf()
    # avoid displaying on notebooks and clears the canvas for the next plot
    plt.close()

    return {
        "figure": figure,
        "key": f"shap:{type_}",
        "metadata": {"type": type_},
    }


def shap_global_importance(model, x_test, generate_plots=True, linear=False):
    """
    Compute shap global importance (SHAP).
    :param model:
    :param x_test:
    :param generate_plots: when True, the returning dict contains the key "plots" with
    :param linear: when True, use a LinearExplainer instead
    dict of the figure, key and metadata for the plot.
    """
    explainer = (
        shap.TreeExplainer(model) if not linear else shap.LinearExplainer(model, x_test)
    )
    shap_values = explainer.shap_values(x_test)

    # For models with a single output this returns a numpy.ndarray of SHAP values
    # if type(shap_values) is numpy.ndarray:
    #     result_values = shap_values.tolist()
    # else:
    #     # For models with vector outputs this returns a list of matrices of SHAP values
    #     shap_values = shap_values[0]
    #     result_values = shap_values

    results = {
        "type": "evaluation",
        "scope": "test",
        "key": "shap",
        # "value": result_values,
    }

    if generate_plots:
        results["plots"] = [
            _generate_shap_plot("mean", shap_values, x_test),
            _generate_shap_plot("summary", shap_values, x_test),
        ]

    return results


def trainining_better_than_test():
    """ """
    return True
