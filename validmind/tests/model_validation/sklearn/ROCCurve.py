from dataclasses import dataclass

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
        y_true = self.model.test_ds.df[self.model.test_ds.target_column]
        class_pred = self.model.class_predictions(self.model.y_test_predict)
        fpr, tpr, roc_thresholds = metrics.roc_curve(
            y_true, self.model.y_test_predict, drop_intermediate=True
        )
        auc = metrics.roc_auc_score(y_true, class_pred)

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
