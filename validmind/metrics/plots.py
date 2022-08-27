"""
Utilities to create plots for metrics that are formatteed for ValidMind
"""
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import ConfusionMatrixDisplay


def get_confusion_matrix_plot(tn, fp, fn, tp):
    """
    Get the confusion matrix plot from the results of the model evaluation test suite
    """
    cfm = np.asarray(
        [
            [tn, fp],
            [fn, tp],
        ]
    )

    cfm_plot = ConfusionMatrixDisplay(confusion_matrix=cfm)

    return cfm_plot


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


def get_pr_curve_plot(precision, recall):
    plt.close("all")
    figure, ax = plt.subplots()

    ax.plot(
        recall,
        precision,
        color="darkorange",
    )
    ax.axis(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.05)

    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision Recall Curve")

    return figure


def get_roc_curve_plot(fpr, tpr, auc):
    plt.close("all")
    figure, ax = plt.subplots()

    ax.plot(
        fpr,
        tpr,
        color="darkorange",
        label="ROC curve (area = %0.2f)" % auc,
    )
    ax.plot([0, 1], [0, 1], color="navy", linestyle="--")
    ax.axis(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.05)

    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("Receiver Operating Characteristic Curve")
    ax.legend(loc="lower right")

    return figure
