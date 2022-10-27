"""
Generic Metrics
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import shap

from sklearn.inspection import permutation_importance as pfi_sklearn

from ..models import Figure, Metric, MetricResult
from .plots import get_pfi_plot


def _generate_shap_plot(type_, shap_values, x_test):
    """
    Plots two types of SHAP global importance (SHAP).
    :params type: mean, summary
    :params shap_values: a matrix
    :params x_test:
    """
    plt.close("all")

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

    return Figure(
        figure=figure,
        key=f"shap:{type_}",
        metadata={"type": type_},
    )


def permutation_importance(
    model, test_set, test_preds, train_set=None, train_preds=None
):
    """
    Compute permutation feature importance (PFI) values from sklearn.
    """
    x_test, y_test = test_set

    r = pfi_sklearn(model, x_test, y_test, random_state=0)
    pfi = {}

    for i, column in enumerate(x_test.columns):
        pfi[column] = [r["importances_mean"][i]], [r["importances_std"][i]]

    return MetricResult(
        api_metric=Metric(
            type="evaluation",
            scope="test",
            key="pfi",
            value=pfi,
        ),
        plots=[get_pfi_plot(pfi)],
    )


def shap_global_importance(model, test_set, test_preds, linear=False):
    """
    Compute shap global importance (SHAP).
    :param model:
    :param x_test:
    :param generate_plots: when True, the returning dict contains the key "plots" with
    :param linear: when True, use a LinearExplainer instead
    dict of the figure, key and metadata for the plot.
    """
    x_test, _ = test_set

    model_class = model.__class__.__name__

    # RandomForestClassifier applies here too
    if model_class == "XGBClassifier":
        explainer = shap.TreeExplainer(model)
    elif (
        model_class == "LogisticRegression"
        or model_class == "XGBRegressor"
        or model_class == "LinearRegression"
    ):
        explainer = shap.LinearExplainer(model, x_test)
    else:
        raise ValueError(f"Model {model_class} not supported for SHAP importance.")

    shap_values = explainer.shap_values(x_test)

    # For models with a single output this returns a numpy.ndarray of SHAP values
    # if type(shap_values) is numpy.ndarray:
    #     result_values = shap_values.tolist()
    # else:
    #     # For models with vector outputs this returns a list of matrices of SHAP values
    #     shap_values = shap_values[0]
    #     result_values = shap_values

    return MetricResult(
        api_metric=Metric(
            type="evaluation",
            scope="test",
            key="shap",
        ),
        api_figures=[
            _generate_shap_plot("mean", shap_values, x_test),
            _generate_shap_plot("summary", shap_values, x_test),
        ],
    )
