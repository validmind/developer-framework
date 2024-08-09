# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import matplotlib.pyplot as plt
import seaborn as sns

from validmind import tags, tasks


@tags("visualization")
@tasks("monitoring")
def TargetPredictionDistributionPlot(datasets, model):
    """
    **Purpose:**
    This test provides the prediction distributions from the reference dataset and the new monitoring dataset. If there
    are significant differences in the distributions, it might indicate different underlying data characteristics that
    warrant further investigation into the root causes.

    **Test Mechanism:**
    The methodology involves generating Kernel Density Estimation (KDE) plots for the prediction probabilities from
    both the reference and monitoring datasets. By comparing these KDE plots, one can visually assess any significant
    differences in the prediction distributions between the two datasets.

    **Signs of High Risk:**
    - Significant divergence between the distribution curves of the reference and monitoring predictions
    - Unusual shifts or bimodal distribution in the monitoring predictions compared to the reference predictions

    **Strengths:**
    - Visual representation makes it easy to spot differences in prediction distributions
    - Useful for identifying potential data drift or changes in underlying data characteristics
    - Simple and efficient to implement using standard plotting libraries

    **Limitations:**
    - Subjective interpretation of the visual plots
    - Might not pinpoint the exact cause of distribution changes
    - Less effective if the differences in distributions are subtle and not easily visible
    """

    pred_ref = datasets[0].y_prob_df(model)
    pred_ref.columns = ["Reference Prediction"]
    pred_monitor = datasets[1].y_prob_df(model)
    pred_monitor.columns = ["Monitoring Prediction"]

    fig = plt.figure()
    plot = sns.kdeplot(
        pred_ref["Reference Prediction"], shade=True, label="Reference Prediction"
    )
    plot = sns.kdeplot(
        pred_monitor["Monitoring Prediction"], shade=True, label="Monitor Prediction"
    )
    plot.set(
        xlabel="Prediction", title="Distribution of Reference & Monitor Predictions"
    )
    plot.legend()

    return fig
