# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import plotly.figure_factory as ff
from sklearn import metrics

from validmind.vm_models import Figure, Metric


@dataclass
class ConfusionMatrix(Metric):
    """
    **Purpose**: The Confusion Matrix tester is tasked with evaluating the performance of a classification Machine
    Learning model. The matrix indicates how well the model can accurately distinguish true and false positives and
    negatives - basic indicators of model accuracy.

    **Test Mechanism**: The classification model's results (`y_test_predict`) are compared against the actual results
    (`y_test_true`). The unique labels identified from `y_test_true` are used to create a confusion matrix using
    scikit-learn's metrics. The matrix is then rendered using Plotly's `create_annotated_heatmap` function. Outcomes
    such as True Positives (TP), True Negatives (TN), False Positives (FP), and False Negatives (FN) are plotted in a
    color-coded heatmap, providing a visualized 2D representation of the model's performance.

    **Signs of High Risk**: High risks associated with the model are signaled by high numbers of False Positives (FP)
    and False Negatives (FN), which demonstrates the model's inability to accurately classify. On the other hand, low
    numbers of True Positives (TP) and True Negatives (TN) also indicate problematic situation, meaning the model is
    unable to correctly identify the class labels.

    **Strengths**: Utilizing a Confusion Matrix has various strengths:

    - It allows a clear and simple visual summary of the classification model's prediction accuracy.
    - It provides explicit metrics for True Positives (TP), True Negatives (TN), False Positives (FP), and False
    Negatives (FN), making it easy to highlight potential improvements.
    - It's beneficial for multi-class classification problems, since it can provide readability for complex models in a
    simplified manner.
    - It assists in understanding the different types of errors your model might make, by providing both Type-I and
    Type-II errors.

    **Limitations**: However, the Confusion Matrix also comes with limitations:

    - In conditions of unbalanced classes, the utility of the confusion matrix can be limited. It might quite
    erroneously perceive a model to perform well when it's merely predicting the majority class.
    - It does not deliver a single unified statistic that can appraise model performance. It merely indicates different
    facets of model performance separately.
    - It's largely a descriptive technique and does not allow for statistical hypothesis testing.
    - Misinterpretation risks also exist, as it doesn't directly provide precision, recall or F1-score data. These
    metrics need to be computed separately.
    """

    name = "confusion_matrix"
    required_inputs = ["model"]
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
        y_true = self.model.y_test_true
        labels = np.unique(y_true)
        labels.sort()
        labels = np.array(labels).T.tolist()

        class_pred = self.model.y_test_predict
        y_true = y_true.astype(class_pred.dtype)
        cm = metrics.confusion_matrix(y_true, class_pred, labels=labels)

        fig = ff.create_annotated_heatmap(
            z=cm,
            colorscale="Blues",
            x=labels,
            y=labels,
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
