# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import roc_auc_score, roc_curve


from validmind.vm_models import Figure, Metric


@dataclass
class LogRegROCCurve(Metric):
    """
    Evaluates binary classification model performance by generating and plotting the Receiver Operating Characteristic
    (ROC) curve and calculating the Area Under Curve (AUC) score specifically for logistic regression models.

    **Purpose**:
    The Receiver Operating Characteristic (ROC) curve assesses the performance of binary logistic regression models by
    illustrating the trade-off between the True Positive Rate (TPR) and False Positive Rate (FPR) across various
    threshold levels. This curve quantifies the model's ability to discriminate between the positive and negative classes
    in a binary classification problem, such as predicting default vs non-default outcomes. A higher AUC score indicates
    superior performance in accurately distinguishing between the two classes.

    **Test Mechanism**:
    This script calculates the predicted probabilities for the test set using the logistic regression model. It then
    constructs the ROC curve using the true outcomes and predicted probabilities. Additionally, it includes a line
    representing randomness (AUC of 0.5) for comparison. The AUC score is computed as a numerical estimation of the
    model's discriminatory power. Any infinite values detected in the ROC thresholds are eliminated. The resulting ROC
    curve, AUC score, and thresholds are saved for future reference.

    **Signs of High Risk**:
    - A high risk may be associated with the model's performance if the AUC score drops below or nears 0.5.
    - Another indicator of poor performance is when the ROC curve closely resembles the line of randomness, suggesting
    limited discriminative ability.
    - For competent classification, the AUC score should significantly exceed 0.5.

    **Strengths**:
    - The logistic regression ROC curve provides a comprehensive visualization of the model's discriminative ability
    across various classification thresholds, unlike metrics that evaluate performance at a single threshold.
    - Despite dataset proportions, the AUC score remains consistent, making it suitable for diverse scenarios.

    **Limitations**:
    - This test is exclusively designed for binary classification tasks, limiting its applicability to other model types.
    - Performance may be suboptimal with models that output probabilities heavily skewed towards 0 or 1.
    - In cases of extreme class imbalance, the ROC curve may indicate high performance even with a majority of incorrect
    classifications, provided the model's ranking format is preserved (Class Imbalance Problem).

    """

    name = "log_regression_roc_curve"
    required_inputs = ["model", "dataset"]
    metadata = {
        "task_types": ["classification"],
        "tags": [
            "sklearn",
            "logistic_regression",
            "model_performance",
            "visualization",
        ],
    }

    def run(self):

        y_pred = self.inputs.dataset.y_pred(self.inputs.model.input_id)
        y_pred = np.array(y_pred, dtype=float)
        assert np.all((y_pred >= 0) & (y_pred <= 1)), "Invalid probabilities in y_pred."

        y_true = self.inputs.dataset.y
        y_true = np.array(y_true, dtype=float)

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
