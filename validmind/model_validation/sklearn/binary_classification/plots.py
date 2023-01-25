"""
Binary classification plotting functions from the sklearn interface
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
