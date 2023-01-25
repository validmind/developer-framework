"""
Generic plotting functions from the sklearn interface
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import shap

from ....vm_models import Figure


def get_pfi_plot(pfi_values):
    plt.close("all")

    pfi_bar_values = []
    for feature, values in pfi_values.items():
        pfi_bar_values.append({"feature": feature, "value": values[0][0]})

    pfi_bar_values = sorted(pfi_bar_values, key=lambda d: d["value"], reverse=True)
    pfi_x_values = [d["value"] for d in pfi_bar_values]
    pfi_y_values = [d["feature"] for d in pfi_bar_values]

    # Plot a bar plot with horizontal bars
    figure, ax = plt.subplots()
    ax.barh(pfi_y_values, pfi_x_values, color="darkorange")
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")
    ax.set_title("Permutation Feature Importance")
    ax.set_yticks(np.arange(len(pfi_y_values)))
    ax.set_yticklabels(pfi_y_values)
    ax.invert_yaxis()

    return figure


def get_shap_plot(type_, shap_values, x_test):
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
