# Copyright © 2023 ValidMind Inc. All rights reserved.
import numpy as np
from dataclasses import dataclass
import plotly.graph_objects as go
from sklearn.metrics import precision_recall_curve, average_precision_score
from validmind.vm_models import Figure, Metric


@dataclass
class RegressionPrecisionRecallCurve(Metric):
    """
    Regression Precision-Recall Curve
    """

    name = "regression_precision_recall_curve"
    required_inputs = ["model"]

    def description(self):
        return """
        The Precision-Recall curve illustrates the trade-off between precision and recall for different threshold values. A high area under the curve represents both high recall and high precision, where high precision relates to a low false positive rate, and high recall relates to a low false negative rate.
        """

    @staticmethod
    def plot_pr_curve(precision, recall, thresholds, avg_precision):
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=recall,
                    y=precision,
                    mode="lines",
                    name="PR curve (AP = %0.2f)" % avg_precision,
                    hovertemplate="Recall: %{x:.3f}<br>Precision: %{y:.3f}<br>Threshold: %{text}<extra></extra>",
                    text=[f"{thr:.3f}" for thr in thresholds],
                )
            ]
        )

        fig.update_layout(
            title_text="Precision-Recall Curve",
            xaxis_title_text="Recall",
            yaxis_title_text="Precision",
            width=700,
            height=500,
        )

        return fig

    def run(self):
        # Extract the actual model
        model = self.model[0] if isinstance(self.model, list) else self.model

        y_true = np.array(model.test_ds.y)
        y_scores = model.predict(model.test_ds.x)

        precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
        avg_precision = average_precision_score(y_true, y_scores)

        fig = self.plot_pr_curve(precision, recall, thresholds, avg_precision)

        return self.cache_results(
            metric_value={
                "pr_curve": {
                    "precision": list(precision),
                    "recall": list(recall),
                    "thresholds": list(thresholds),
                    "average_precision": avg_precision,
                }
            },
            figures=[
                Figure(
                    for_object=self,
                    key="pr_curve",
                    figure=fig,
                )
            ],
        )
