# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np
import plotly.figure_factory as ff
from sklearn import metrics

from validmind.vm_models import Figure, Metric


@dataclass
class ConfusionMatrix(Metric):
    """
    Evaluates and visually represents the classification ML model's predictive performance using a Confusion Matrix
    heatmap.

    **Purpose**: The Confusion Matrix tester is designed to assess the performance of a classification Machine Learning
    model. This performance is evaluated based on how well the model is able to correctly classify True Positives, True
    Negatives, False Positives, and False Negatives - fundamental aspects of model accuracy.

    **Test Mechanism**: The mechanism used involves taking the predicted results (`y_test_predict`) from the
    classification model and comparing them against the actual values (`y_test_true`). A confusion matrix is built
    using the unique labels extracted from `y_test_true`, employing scikit-learn's metrics. The matrix is then visually
    rendered with the help of Plotly's `create_annotated_heatmap` function. A heatmap is created which provides a
    two-dimensional graphical representation of the model's performance, showcasing distributions of True Positives
    (TP), True Negatives (TN), False Positives (FP), and False Negatives (FN).

    **Signs of High Risk**: Indicators of high risk related to the model include:
    - High numbers of False Positives (FP) and False Negatives (FN), depicting that the model is not effectively
    classifying the values.
    - Low numbers of True Positives (TP) and True Negatives (TN), implying that the model is struggling with correctly
    identifying class labels.

    **Strengths**: The Confusion Matrix tester brings numerous strengths:
    - It provides a simplified yet comprehensive visual snapshot of the classification model's predictive performance.
    - It distinctly brings out True Positives (TP), True Negatives (TN), False Positives (FP), and False Negatives
    (FN), thus, making it easier to focus on potential areas of improvement.
    - The matrix is beneficial in dealing with multi-class classification problems as it can provide a simple view of
    complex model performances.
    - It aids in understanding the different types of errors that the model could potentially make, as it provides
    in-depth insights into Type-I and Type-II errors.

    **Limitations**: Despite its various strengths, the Confusion Matrix tester does exhibit some limitations:
    - In cases of unbalanced classes, the effectiveness of the confusion matrix might be lessened. It may wrongly
    interpret the accuracy of a model that is essentially just predicting the majority class.
    - It does not provide a single unified statistic that could evaluate the overall performance of the model.
    Different aspects of the model's performance are evaluated separately instead.
    - It mainly serves as a descriptive tool and does not offer the capability for statistical hypothesis testing.
    - Risks of misinterpretation exist because the matrix doesn't directly provide precision, recall, or F1-score data.
    These metrics have to be computed separately.
    """

    name = "confusion_matrix"
    required_inputs = ["model", "dataset"]
    metadata = {
        "task_types": ["classification", "text_classification"],
        "tags": [
            "sklearn",
            "binary_classification",
            "multiclass_classification",
            "model_performance",
            "visualization",
        ],
    }

    def run(self):
        y_true = self.inputs.dataset.y
        labels = np.unique(y_true)
        labels.sort()
        labels = np.array(labels).T.tolist()

        y_pred = self.inputs.dataset.y_pred(self.inputs.model)
        y_true = y_true.astype(y_pred.dtype)

        cm = metrics.confusion_matrix(y_true, y_pred, labels=labels)

        text = None
        if len(labels) == 2:
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
            z=cm,
            colorscale="Blues",
            x=labels,
            y=labels,
            annotation_text=text,
        )

        fig["data"][0][
            "hovertemplate"
        ] = "True Label:%{y}<br>Predicted Label:%{x}<br>Count:%{z}<extra></extra>"

        fig.update_layout(
            xaxis=dict(title="Predicted label"),
            yaxis=dict(title="True label"),
            autosize=False,
            width=600,
            height=600,
        )

        return self.cache_results(
            metric_value={
                "confusion_matrix": cm,
            },
            figures=[
                Figure(
                    for_object=self,
                    key="confusion_matrix",
                    figure=fig,
                )
            ],
        )

    def test(self):
        """Unit Test for Confusion Matrix Metric"""
        assert self.result is not None

        assert self.result.metric is not None
        assert isinstance(self.result.metric.value, dict)
        assert "confusion_matrix" in self.result.metric.value

        assert len(self.result.figures) == 1
