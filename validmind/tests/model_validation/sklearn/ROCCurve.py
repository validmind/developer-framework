# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import roc_auc_score, roc_curve

from validmind.errors import SkipTestError
from validmind.models import FoundationModel
from validmind.vm_models import Figure, Metric


@dataclass
class ROCCurve(Metric):
    """
    Evaluates binary classification model performance by generating and plotting the Receiver Operating Characteristic
    (ROC) curve and calculating the Area Under Curve (AUC) score.

    ### Purpose

    The Receiver Operating Characteristic (ROC) curve is designed to evaluate the performance of binary classification
    models. This curve illustrates the balance between the True Positive Rate (TPR) and False Positive Rate (FPR)
    across various threshold levels. In combination with the Area Under the Curve (AUC), the ROC curve aims to measure
    the model's discrimination ability between the two defined classes in a binary classification problem (e.g.,
    default vs non-default). Ideally, a higher AUC score signifies superior model performance in accurately
    distinguishing between the positive and negative classes.

    ### Test Mechanism

    First, this script selects the target model and datasets that require binary classification. It then calculates the
    predicted probabilities for the test set, and uses this data, along with the true outcomes, to generate and plot
    the ROC curve. Additionally, it includes a line signifying randomness (AUC of 0.5). The AUC score for the model's
    ROC curve is also computed, presenting a numerical estimation of the model's performance. If any Infinite values
    are detected in the ROC threshold, these are effectively eliminated. The resulting ROC curve, AUC score, and
    thresholds are consequently saved for future reference.

    ### Signs of High Risk

    - A high risk is potentially linked to the model's performance if the AUC score drops below or nears 0.5.
    - Another warning sign would be the ROC curve lying closer to the line of randomness, indicating no discriminative
    ability.
    - For the model to be deemed competent at its classification tasks, it is crucial that the AUC score is
    significantly above 0.5.

    ### Strengths

    - The ROC Curve offers an inclusive visual depiction of a model's discriminative power throughout all conceivable
    classification thresholds, unlike other metrics that solely disclose model performance at one fixed threshold.
    - Despite the proportions of the dataset, the AUC Score, which represents the entire ROC curve as a single data
    point, continues to be consistent, proving to be the ideal choice for such situations.

    ### Limitations

    - The primary limitation is that this test is exclusively structured for binary classification tasks, thus limiting
    its application towards other model types.
    - Furthermore, its performance might be subpar with models that output probabilities highly skewed towards 0 or 1.
    - At the extreme, the ROC curve could reflect high performance even when the majority of classifications are
    incorrect, provided that the model's ranking format is retained. This phenomenon is commonly termed the "Class
    Imbalance Problem".
    """

    name = "roc_curve"
    required_inputs = ["model", "dataset"]
    tasks = ["classification", "text_classification"]
    tags = [
        "sklearn",
        "binary_classification",
        "multiclass_classification",
        "model_performance",
        "visualization",
    ]

    def run(self):
        if isinstance(self.inputs.model, FoundationModel):
            raise SkipTestError("Skipping ROCCurve for Foundation models")

        y_true = self.inputs.dataset.y
        y_prob = self.inputs.dataset.y_prob(self.inputs.model)

        # ROC curve is only supported for binary classification
        if len(np.unique(y_true)) > 2:
            raise SkipTestError(
                "ROC Curve is only supported for binary classification models"
            )

        y_true = y_true.astype(y_prob.dtype).flatten()
        assert np.all((y_prob >= 0) & (y_prob <= 1)), "Invalid probabilities in y_prob."

        fpr, tpr, roc_thresholds = roc_curve(y_true, y_prob, drop_intermediate=False)

        # Remove Inf values from roc_thresholds
        valid_thresholds_mask = np.isfinite(roc_thresholds)
        roc_thresholds = roc_thresholds[valid_thresholds_mask]
        auc = roc_auc_score(y_true, y_prob)

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
            title=f"ROC Curve for {self.inputs.model.input_id} on {self.inputs.dataset.input_id}",
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
