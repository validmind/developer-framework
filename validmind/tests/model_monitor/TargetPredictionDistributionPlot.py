# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import matplotlib.pyplot as plt
import seaborn as sns

from validmind import tags, tasks


@tags("monitoring", "visualization")
@tasks("classification")
def TargetPredictionDistributionPlot(datasets, model):
    """
    This test provides the prediction distributions from the reference dataset and the new monitoring dataset.
    If there are significant differences in the distributions then it might indicate of different underlying data
    characteristics that might lead to further investigation into the root causes.
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
