# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
from dataclasses import dataclass
import plotly.graph_objects as go
from sklearn.metrics import roc_curve, auc
from validmind.vm_models import Figure, Metric, Model


@dataclass
class RegressionROCCurve(Metric):
    """
    Regression ROC Curve
    """

    name = "regression_roc_curve"
    required_context = ["model"]

    def description(self):
        return """
        A receiver operating characteristic (ROC), or simply ROC curve, is a graphical plot that illustrates the diagnostic ability of a binary classifier system as its discrimination threshold is varied. The curve is created by plotting the true positive rate (TPR) against the false positive rate (FPR) at various threshold settings. The area under the ROC curve (AUC) is a measure of how well a parameter can distinguish between two diagnostic groups.
        """

    @staticmethod
    def plot_roc_curve(fpr, tpr, thresholds, roc_auc):
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=fpr,
                    y=tpr,
                    mode="lines",
                    name="ROC curve (AUC = %0.2f)" % roc_auc,
                    hovertemplate="FPR: %{x:.3f}<br>TPR: %{y:.3f}<br>Threshold: %{text}<extra></extra>",
                    text=[f"{thr:.3f}" for thr in thresholds],
                ),
                go.Scatter(
                    x=[0, 1],
                    y=[0, 1],
                    mode="lines",
                    name="Random (AUC = 0.50)",
                    line=dict(dash="dash"),
                    hoverinfo="none",
                ),
            ]
        )

        fig.update_layout(
            title_text="Receiver Operating Characteristic (ROC)",
            xaxis_title_text="False Positive Rate",
            yaxis_title_text="True Positive Rate",
            yaxis=dict(scaleanchor="x", scaleratio=1),
            xaxis=dict(constrain="domain"),
            width=700,
            height=500,
        )

        return fig

    def run(self):
        if not Model.is_supported_model(self.model.model):
            raise ValueError(
                f"{Model.model_library(self.model.model)}.{Model.model_class(self.model.model)} \
                              is not supported by ValidMind framework yet"
            )

        y_true = np.array(self.model.test_ds.y)
        y_scores = self.model.predict(self.model.test_ds.x)

        fpr, tpr, thresholds = roc_curve(y_true, y_scores)
        roc_auc = auc(fpr, tpr)

        fig = self.plot_roc_curve(fpr, tpr, thresholds, roc_auc)

        return self.cache_results(
            metric_value={
                "roc_curve": {
                    "fpr": list(fpr),
                    "tpr": list(tpr),
                    "thresholds": list(thresholds),
                    "auc": roc_auc,
                },
            },
            figures=[
                Figure(
                    for_object=self,
                    key="roc_curve",
                    figure=fig,
                )
            ],
        )
