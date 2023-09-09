# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import precision_recall_curve

from validmind.errors import SkipTestError
from validmind.vm_models import Figure, Metric


@dataclass
class PrecisionRecallCurve(Metric):
    """
    Precision Recall Curve
    """

    name = "pr_curve"
    required_inputs = ["model"]

    def description(self):
        return """
        The precision-recall curve shows the trade-off between precision and recall for different thresholds.
        A high area under the curve represents both high recall and high precision, where high precision
        relates to a low false positive rate, and high recall relates to a low false negative rate. High scores
        for both show that the classifier is returning accurate results (high precision), as well as returning
        a majority of all positive results (high recall).
        """

    def run(self):
        if self.model.model_library() == "FoundationModel":
            raise SkipTestError("Skipping PrecisionRecallCurve for Foundation models")

        y_true = np.array(self.model.test_ds.y)
        y_pred = self.model.predict(self.model.test_ds.x)

        # PR curve is only supported for binary classification
        if len(np.unique(y_true)) > 2:
            raise SkipTestError(
                "Precision Recall Curve is only supported for binary classification models"
            )

        precision, recall, pr_thresholds = precision_recall_curve(y_true, y_pred)

        trace = go.Scatter(
            x=recall,
            y=precision,
            mode="lines",
            name="Precision-Recall Curve",
            line=dict(color="#DE257E"),
        )
        layout = go.Layout(
            title="Precision-Recall Curve",
            xaxis=dict(title="Recall"),
            yaxis=dict(title="Precision"),
        )

        fig = go.Figure(data=[trace], layout=layout)

        return self.cache_results(
            metric_value={
                "precision": precision,
                "recall": recall,
                "thresholds": pr_thresholds,
            },
            figures=[
                Figure(
                    for_object=self,
                    key="pr_curve",
                    figure=fig,
                )
            ],
        )
