# Saved from __main__.confusion_matrix
# Original Test ID: my_custom_metrics.ConfusionMatrix
# New Test ID: <test_provider_namespace>.ConfusionMatrix

import matplotlib.pyplot as plt
from sklearn import metrics


def ConfusionMatrix(dataset, model):
    """The confusion matrix is a table that is often used to describe the performance of a classification model on a set of data for which the true values are known.

    The confusion matrix is a 2x2 table that contains 4 values:

    - True Positive (TP): the number of correct positive predictions
    - True Negative (TN): the number of correct negative predictions
    - False Positive (FP): the number of incorrect positive predictions
    - False Negative (FN): the number of incorrect negative predictions

    The confusion matrix can be used to assess the holistic performance of a classification model by showing the accuracy, precision, recall, and F1 score of the model on a single figure.
    """
    confusion_matrix = metrics.confusion_matrix(dataset.y, dataset.y_pred(model))

    cm_display = metrics.ConfusionMatrixDisplay(
        confusion_matrix=confusion_matrix, display_labels=[False, True]
    )
    cm_display.plot()

    plt.close()  # close the plot to avoid displaying it

    return cm_display.figure_  # return the figure object itself
