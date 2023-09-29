# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import roc_auc_score, roc_curve

from validmind.errors import SkipTestError
from validmind.vm_models import Figure, Metric


@dataclass
class ROCCurve(Metric):
    """
    **Purpose**:
    The Receiver Operating Characteristic (ROC) curve is a critical analysis tool for the performance of binary
    classification models. The ROC curve displays the trade-off between the True Positive Rate (TPR) and False Positive
    Rate (FPR) at varying threshold levels. The ROC curve, together with the Area Under the Curve (AUC), is designed to
    provide a measure of how well the model can discriminate between the two classes in a binary classification problem
    (e.g., default vs non-default). The higher the AUC score, the better the model is at correctly distinguishing
    between the positive and negative classes.

    **Test Mechanism**:
    This script extracts the target model and datasets, where binary classification is a requirement. Next, it computes
    predicted probabilities for the test set. It then calculates and plots the ROC curve using the true outcomes and
    predicted probabilities, along with the line representing randomness (AUC of 0.5). The AUC score for the ROC curve
    of the model is also computed, giving a numeric estimate of the model's performance. Any Infinite values in the ROC
    threshold are identified and removed in the process. The resulting ROC curve, AUC score, and thresholds are
    subsequently saved.

    **Signs of High Risk**:
    There would be a high risk associated with the performance of the model if the AUC score is below or close to 0.5,
    or if the ROC curve is observed to be closer to the line of randomness (indicating no discriminative power). It's
    essential to note that the AUC score must be significantly greater than 0.5 for the model to be considered
    effective at its classification task.

    **Strengths**:
    The ROC Curve provides a comprehensive visual representation of a model’s discriminative power over all possible
    classification thresholds, unlike metrics that only reveal model performance at a single set threshold. The AUC
    Score, which summarizes the ROC curve into a single value, remains consistent in the face of imbalanced datasets,
    making it an ideal choice for such cases.

    **Limitations**:
    This test is designed specifically for binary classification tasks, limiting its application to other model types.
    Additionally, it might not perform well for models that output probabilities severely skewed towards 0 or 1. In an
    extreme case, the ROC curve can exhibit high performance even in situations where the majority of classifications
    are incorrect, if the model's score ranking is preserved. This is known as the "class imbalance problem."
    """

    name = "roc_curve"
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
        if self.model.model_library() == "FoundationModel":
            raise SkipTestError("Skipping ROCCurve for Foundation models")

        # Extract the actual model
        model = self.model[0] if isinstance(self.model, list) else self.model

        y_true = model.test_ds.y
        y_pred = model.predict(model.test_ds.x)

        # ROC curve is only supported for binary classification
        if len(np.unique(y_true)) > 2:
            raise SkipTestError(
                "ROC Curve is only supported for binary classification models"
            )

        y_true = y_true.astype(y_pred.dtype).flatten()
        assert np.all((y_pred >= 0) & (y_pred <= 1)), "Invalid probabilities in y_pred."

        fpr, tpr, roc_thresholds = roc_curve(y_true, y_pred, drop_intermediate=False)
        # Remove Inf values from roc_thresholds
        valid_thresholds_mask = np.isfinite(roc_thresholds)
        roc_thresholds = roc_thresholds[valid_thresholds_mask]
        auc = roc_auc_score(y_true, y_pred)

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
            width=700,
            height=500,
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
