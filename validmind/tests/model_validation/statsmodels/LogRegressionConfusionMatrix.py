# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import plotly.figure_factory as ff
from sklearn import metrics

from validmind.vm_models import Figure, Metric


@dataclass
class LogRegressionConfusionMatrix(Metric):
    """
    Generates a confusion matrix for logistic regression model performance, utilizing thresholded probabilities for
    classification assessments.

    **Purpose**: The Logistic Regression Confusion Matrix is a metric used to measure the performance of a logistic
    regression classification model. This metric is particularly useful for scenarios where a model's predictions are
    formulated by thresholding probabilities. The main advantage of this approach is that it includes true positives,
    true negatives, false positives, and false negatives in its assessment, providing a more comprehensive overview of
    the model's effectiveness in distinguishing between correct and incorrect classifications.

    **Test Mechanism**: The methodology behind the Logistic Regression Confusion Matrix uses the
    `sklearn.metrics.confusion_matrix` function from the Python library to generate a matrix. This matrix is created by
    comparing the model's predicted probabilities, which are initially converted to binary predictions using a
    predetermined cut-off threshold (default is 0.5), against the actual classes. The matrix's design consists of the
    predicted class labels forming the x-axis, and the actual class labels forming the y-axis, with each cell
    containing the record of true positives, true negatives, false positives, and false negatives respectively.

    **Signs of High Risk**:
    - A significant number of false positives and false negatives, indicating that the model is incorrectly classifying
    instances.
    - The counts of true positives and true negatives being substantially lower than projected, positioning this as a
    potential high-risk indicator.

    **Strengths**:
    - Simple, intuitive, and provides a comprehensive understanding of the model's performance.
    - Provides a detailed breakdown of error types, improving transparency.
    - Offers flexible adaptation for diverse prediction scenarios by allowing adjustments to the cut-off threshold, and
    enabling exploration of trade-offs between precision (minimizing false positives) and recall (minimizing false
    negatives).

    **Limitations**:
    - Acceptable performance on majority classes but potential poor performance on minority classes in imbalanced
    datasets, as the confusion matrix may supply misleading results.
    - Lack of insight into the severity of the mistakes and the cost trade-off between different types of
    misclassification.
    - Selection of the cut-off threshold can significantly alter the interpretation, and a poorly chosen threshold may
    lead to erroneous conclusions.
    """

    name = "log_regression_confusion_matrix"
    required_inputs = ["model"]
    metadata = {
        "task_types": ["classification"],
        "tags": ["visualization", "model_performance", "logistic_regression"],
    }

    default_params = {
        "cut_off_threshold": 0.5,  # Add a cut_off_threshold parameter
    }

    def run(self):
        cut_off_threshold = self.default_parameters["cut_off_threshold"]

        # Extract the actual model
        model = self.model[0] if isinstance(self.model, list) else self.model

        y_true = np.array(model.test_ds.y)
        y_labels = np.unique(y_true)
        y_labels.sort()

        y_pred_prob = model.predict(model.test_ds.x)
        y_pred = np.where(y_pred_prob > cut_off_threshold, 1, 0)
        y_true = y_true.astype(y_pred.dtype)

        cm = metrics.confusion_matrix(y_true, y_pred, labels=y_labels)
        tn, fp, fn, tp = cm.ravel()

        # Custom text to display on the heatmap cells
        text = [
            [
                f"<b>True Negatives (TN)</b><br />{tn}",
                f"<b>False Positives (FP)</b><br />{fp}",
            ],
            [
                f"<b>False Negatives (FN)</b><br />{fn}",
                f"<b>True Positives (TP)</b><br />{tp}",
            ],
        ]

        fig = ff.create_annotated_heatmap(
            [[tn, fp], [fn, tp]],
            x=[0, 1],
            y=[0, 1],
            colorscale="Blues",
            annotation_text=text,
        )
        # Reverse the xaxis so that 1 is on the left
        fig["layout"]["xaxis"]["autorange"] = "reversed"

        fig["data"][0][
            "hovertemplate"
        ] = "True Label:%{y}<br>Predicted Label:%{x}<br>Count:%{z}<extra></extra>"

        fig.update_layout(
            xaxis=dict(title="Predicted label", constrain="domain"),
            yaxis=dict(title="True label", scaleanchor="x", scaleratio=1),
            autosize=False,
            width=600,
            height=600,
        )

        return self.cache_results(
            metric_value={
                "tn": tn,
                "fp": fp,
                "fn": fn,
                "tp": tp,
            },
            figures=[
                Figure(
                    for_object=self,
                    key="confusion_matrix",
                    figure=fig,
                )
            ],
        )
