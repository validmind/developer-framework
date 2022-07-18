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
)


def accuracy_score(y_true, y_pred=None, rounded_y_pred=None):
    """
    Compute accuracy score metric from sklearn.
    """
    return {
        "type": "evaluation",
        "scope": "test",
        "key": "accuracy",
        "value": [metrics.accuracy_score(y_true, rounded_y_pred)],
    }


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


def f1_score(y_true, y_pred=None, rounded_y_pred=None):
    """
    Compute f1 score metric from sklearn.
    """
    return {
        "type": "evaluation",
        "scope": "test",
        "key": "f1_score",
        "value": [metrics.f1_score(y_true, rounded_y_pred)],
    }


def get_x_and_y(df, target_column):
    """
    Get the X and Y dataframes from the input dataset.
    """
    x = df.drop(target_column, axis=1)
    y = df[target_column]
    return x, y


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


def roc_auc_score(y_true, y_pred=None, rounded_y_pred=None):
    """
    Compute ROC AUC score metric from sklearn.
    """
    return {
        "type": "evaluation",
        "scope": "test",
        "key": "roc_auc",
        "value": [metrics.roc_auc_score(y_true, rounded_y_pred)],
    }


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


def _generate_shap_plot(type_, shap_values, x_test):
    # preserve styles
    mpl.rcParams["grid.color"] = "#CCC"
    ax = plt.axes()
    ax.set_facecolor("white")

    if type_ == "summary":
        shap.summary_plot(shap_values, x_test, show=False)
    elif type_ == "mean":
        shap.summary_plot(
            shap_values, x_test, plot_type="bar", color="#DE257E", show=False
        )
    else:
        raise ValueError(f"unknown shap plot type '{type_}'")

    figure = plt.gcf()
    # avoid displaying on notebooks and clears the canvas for the next plot
    plt.close()

    return {
        "figure": figure,
        "key": f"shap:{type_}",
        "metadata": {"type": type_},
    }


def shap_global_importance(model, x_test, generate_plots=True):
    """
    Compute shap global importance (SHAP).
    :param model:
    :param x_test:
    :param generate_plots: when True, the returning dict contains the key "plots" with
    dict of the figure, key and metadata for the plot.
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(x_test)

    results = {
        "type": "evaluation",
        "scope": "test",
        "key": "shap",
        "value": shap_values.tolist(),
    }

    if generate_plots:
        results["plots"] = [
            _generate_shap_plot("mean", shap_values, x_test),
            _generate_shap_plot("summary", shap_values, x_test),
        ]

    return results
