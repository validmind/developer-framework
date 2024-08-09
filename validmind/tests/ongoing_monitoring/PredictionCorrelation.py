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
    **Purpose:**
    The test is used to assess the correlation pairs for each feature between model predictions from reference and
    monitoring datasets. The primary goal is to detect significant changes in these pairs, which may signal target
    drift, leading to lower model performance.

    **Test Mechanism:**
    The test calculates the correlation of each feature with model predictions for both reference and monitoring
    datasets. The test then compares these correlations side-by-side via a bar plot and a correlation table. Features
    with significant changes in correlation pairs highlight potential risks of model drift.

    **Signs of High Risk:**
    - Significant changes in correlation pairs between the reference and monitoring predictions.
    - Notable correlation differences indicating a potential shift in the relationship between features and the target
    variable.

    **Strengths:**
    - Allows for visual identification of drift in feature relationships with model predictions.
    - Comparison via a clear bar plot assists in understanding model stability over time.
    - Helps in early detection of target drift, enabling timely interventions.

    **Limitations:**
    - May require substantial reference and monitoring data for accurate comparison.
    - Correlation does not imply causation, and other factors might influence changes.
    - The method solely focuses on linear relationships, potentially missing non-linear interactions.
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
