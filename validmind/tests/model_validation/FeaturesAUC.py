# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import roc_auc_score

from validmind.errors import SkipTestError
from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric

logger = get_logger(__name__)


@dataclass
class FeaturesAUC(Metric):
    """
    Evaluates the discriminatory power of each individual feature within a binary classification model by calculating the Area Under the Curve (AUC) for each feature separately.

    **Purpose**: The central objective of this metric is to quantify how well each feature on its own can differentiate between the two classes in a binary classification problem. It serves as a univariate analysis tool that can help in pre-modeling feature selection or post-modeling interpretation.

    **Test Mechanism**: For each feature, the metric treats the feature values as raw scores to compute the AUC against the actual binary outcomes. It provides an AUC value for each feature, offering a simple yet powerful indication of each feature's univariate classification strength.

    **Signs of High Risk**:
    - A feature with a low AUC score may not be contributing significantly to the differentiation between the two classes, which could be a concern if it is expected to be predictive.
    - Conversely, a surprisingly high AUC for a feature not believed to be informative may suggest data leakage or other issues with the data.

    **Strengths**:
    - By isolating each feature, it highlights the individual contribution of features to the classification task without the influence of other variables.
    - Useful for both initial feature evaluation and for providing insights into the model's reliance on individual features after model training.

    **Limitations**:
    - Does not reflect the combined effects of features or any interaction between them, which can be critical in certain models.
    - The AUC values are calculated without considering the model's use of the features, which could lead to different interpretations of feature importance when considering the model holistically.
    - This metric is applicable only to binary classification tasks and cannot be directly extended to multiclass classification or regression without modifications.
    """

    name = "features_auc"
    required_inputs = ["model", "dataset"]
    default_params = {
        "fontsize": 12,
        "figure_height": 500,
    }
    metadata = {
        "task_types": ["classification"],
        "tags": [
            "feature_importance",
            "AUC",
            "visualization",
        ],
    }

    def run(self):
        x = self.inputs.dataset.x_df()
        y = self.inputs.dataset.y_df()

        if y.nunique() != 2:
            raise SkipTestError("FeaturesAUC metric requires a binary target variable.")

        aucs = pd.DataFrame(index=x.columns, columns=["AUC"])

        for column in x.columns:
            feature_values = x[column]
            if feature_values.nunique() > 1:
                auc_score = roc_auc_score(y, feature_values)
                aucs.loc[column, "AUC"] = auc_score
            else:
                aucs.loc[
                    column, "AUC"
                ] = np.nan  # Not enough unique values to calculate AUC

        # Sorting the AUC scores in descending order
        sorted_indices = aucs["AUC"].dropna().sort_values(ascending=False).index

        # Plotting the results
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                y=[column for column in sorted_indices],
                x=[aucs.loc[column, "AUC"] for column in sorted_indices],
                orientation="h",
            )
        )
        fig.update_layout(
            title_text="Feature AUC Scores",
            yaxis=dict(
                tickmode="linear",
                dtick=1,
                tickfont=dict(size=self.params["fontsize"]),
                title="Features",
                autorange="reversed",  # Ensure that the highest AUC is at the top
            ),
            xaxis=dict(title="AUC"),
            height=self.params["figure_height"],
        )

        return self.cache_results(
            metric_value=aucs.to_dict(),
            figures=[
                Figure(
                    for_object=self,
                    key="features_auc",
                    figure=fig,
                ),
            ],
        )
