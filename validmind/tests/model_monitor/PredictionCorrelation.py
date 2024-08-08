# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial


import matplotlib.pyplot as plt
import numpy as np

from validmind import tags, tasks


@tags("visualization")
@tasks("monitoring")
def PredictionCorrelation(datasets, model):
    """
    This test shows the correlation pairs for each feature in the model and model predictions from
    reference dataset and monitoring dataset. The primary goal in this test is to assess if correlation
    pairs between predictions from reference to monitoring have changed significantly. If there is a large
    change between correlation pairs then there is a heightened risk of target drift which can result in
    lower performing models.

    The primary goal is to assess the predictions and each individual feature in the two predictions in order
    to detect a change in the relationship between target and feature.
    """

    prediction_prob_column = f"{model.input_id}_probabilities"
    prediction_column = f"{model.input_id}_prediction"

    df_corr = datasets[0]._df.corr()
    df_corr = df_corr[[prediction_prob_column]]

    df_corr2 = datasets[1]._df.corr()
    df_corr2 = df_corr2[[prediction_prob_column]]

    corr_final = df_corr.merge(df_corr2, left_index=True, right_index=True)
    corr_final.columns = ["Reference Predictions", "Monitoring Predictions"]
    corr_final = corr_final.drop(index=[prediction_column, prediction_prob_column])

    n = len(corr_final)
    r = np.arange(n)
    width = 0.25

    fig = plt.figure()

    plt.bar(
        r,
        corr_final["Reference Predictions"],
        color="b",
        width=width,
        edgecolor="black",
        label="Reference Prediction Correlation",
    )
    plt.bar(
        r + width,
        corr_final["Monitoring Predictions"],
        color="g",
        width=width,
        edgecolor="black",
        label="Monitoring Prediction Correlation",
    )

    plt.xlabel("Features")
    plt.ylabel("Correlation")
    plt.title("Correlation between Predictions and Features")

    features = corr_final.index.to_list()
    plt.xticks(r + width / 2, features, rotation=45)
    plt.legend()
    plt.tight_layout()

    corr_final["Features"] = corr_final.index
    corr_final = corr_final[
        ["Features", "Reference Predictions", "Monitoring Predictions"]
    ]
    return ({"Correlation Pair Table": corr_final}, fig)
