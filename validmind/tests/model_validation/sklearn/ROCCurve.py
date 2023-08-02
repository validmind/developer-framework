# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
import numpy as np
import plotly.graph_objects as go
from sklearn import metrics
from validmind.vm_models import Figure, Metric


@dataclass
class ROCCurve(Metric):
    """
    ROC Curve
    """

    name = "roc_curve"
    required_context = ["model"]

    def description(self):
        return """
        The ROC curve shows the trade-off between the true positive rate (TPR) and false positive rate (FPR)
        for different thresholds. The area under the curve (AUC) is a measure of how well a model can
        distinguish between two groups (e.g. default/non-default). The higher the AUC, the better the model is
        at distinguishing between positive and negative classes.
        """

    def run(self):
        if self.model.device_type and self.model._is_pytorch_model:
            if not self.model.device_type == "gpu":
                y_true = np.array(self.model.test_ds.y.cpu())
            else:
                y_true = np.array(self.model.test_ds.y)
        else:
            y_true = self.model.test_ds.y
        y_pred = self.model.predict_proba(self.model.test_ds.x)

        y_true = y_true.astype(y_pred.dtype).flatten()
        assert np.all((y_pred >= 0) & (y_pred <= 1)), "Invalid probabilities in y_pred."

        fpr, tpr, roc_thresholds = metrics.roc_curve(
            y_true, y_pred, drop_intermediate=False
        )
        # Remove Inf values from roc_thresholds
        valid_thresholds_mask = np.isfinite(roc_thresholds)
        roc_thresholds = roc_thresholds[valid_thresholds_mask]
        auc = metrics.roc_auc_score(y_true, y_pred)

        trace0 = go.Scatter(
            x=fpr,
            y=tpr,
            mode="lines",
            name=f"ROC curve (AUC = {auc:.2f})",
            line=dict(color="#DE257E"),
        )
        trace1 = go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Random (AUC = 0.5)",
            line=dict(color="grey", dash="dash"),
        )

        layout = go.Layout(
            title="ROC Curve",
            xaxis=dict(title="False Positive Rate"),
            yaxis=dict(title="True Positive Rate"),
        )

        fig = go.Figure(data=[trace0, trace1], layout=layout)
        return self.cache_results(
            metric_value={
                "auc": auc,
                "fpr": fpr,
                "tpr": tpr,
                "thresholds": roc_thresholds,
            },
            figures=[
                Figure(
                    for_object=self,
                    key="roc_auc_curve",
                    figure=fig,
                )
            ],
        )
