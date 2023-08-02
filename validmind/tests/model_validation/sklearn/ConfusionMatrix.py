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
    required_context = ["model"]

    def description(self):
        return """
        A confusion matrix is a table that is used to describe the performance of a classification
        model. For metrics such as **True Positives (TP)** and **True Negatives (TN)**, the higher their
        values the better as the model is able to distinguish the correct class from the incorrect
        class more effectively. For **False Positives (FP)** and **False Negatives (FN)**, the lower
        their values the better.
        """

    def run(self):
        if self.model.device_type and self.model._is_pytorch_model:
            if not self.model.device_type == "gpu":
                y_true = np.array(self.model.test_ds.y.cpu())
            else:
                y_true = np.array(self.model.test_ds.y)
        else:
            y_true = np.array(self.model.test_ds.y)

        y_labels = np.unique(y_true)
        y_labels.sort()

        class_pred = self.model.model.predict(self.model.test_ds.x)
        y_true = y_true.astype(class_pred.dtype)
        cm = metrics.confusion_matrix(y_true, class_pred, labels=y_labels)
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
