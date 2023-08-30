# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import plotly.figure_factory as ff
from sklearn import metrics

from validmind.vm_models import Figure, Metric


@dataclass
class ConfusionMatrix(Metric):
    """
    Confusion Matrix
    """

    name = "confusion_matrix"
    required_inputs = ["model"]

    def description(self):
        return """
        A confusion matrix is a table that is used to describe the performance of a classification
        model. For metrics such as **True Positives (TP)** and **True Negatives (TN)**, the higher their
        values the better as the model is able to distinguish the correct class from the incorrect
        class more effectively. For **False Positives (FP)** and **False Negatives (FN)**, the lower
        their values the better.
        """

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
