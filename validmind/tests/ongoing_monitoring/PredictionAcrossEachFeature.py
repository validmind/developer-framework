# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial


import matplotlib.pyplot as plt

from validmind import tags, tasks


@tags("visualization")
@tasks("monitoring")
def PredictionAcrossEachFeature(datasets, model):
    """
    **Purpose:**
    This test shows visually the prediction using reference data and monitoring data across each individual feature. If
    there are significant differences in predictions across feature values from reference to monitoring dataset, then
    further investigation is needed as the model is producing predictions that are different than what was observed
    during the training of the model.

    **Test Mechanism:**
    The test creates scatter plots for each feature, comparing the reference dataset (used for training) with the
    monitoring dataset (used in production). Each plot has two subplots: one for the reference data and one for the
    monitoring data, visualizing the prediction probabilities. This allows for a visual comparison of the model's
    behavior across different datasets.

    **Signs of High Risk:**
    - Significant discrepancies between the reference and monitoring subplots for the same feature
    - Unexpected patterns or trends in monitoring data that weren't present in reference data

    **Strengths:**
    - Provides a clear visual representation of model performance across different features
    - Allows for easy identification of features where the model's predictions have changed
    - Facilitates quick detection of potential issues with the model when deployed in production

    **Limitations:**
    - Interpretation of scatter plots can be subjective and may require expertise
    - Visualizations do not provide quantitative metrics for objective evaluation
    - May not capture all types of distribution changes or issues with the model's predictions
    """

    """
    This test shows visually the prediction using reference data and monitoring data
    across each individual feature. If there are significant differences in predictions
    across feature values from reference to monitoring dataset then futher investigation
    is needed as the model is producing predictions that are different then what was
    observed during the training of the model.
    """

    df_reference = datasets[0]._df
    df_monitoring = datasets[1]._df

    figures_to_save = []
    for column in df_reference:
        prediction_prob_column = f"{model.input_id}_probabilities"
        prediction_column = f"{model.input_id}_prediction"
        if column == prediction_prob_column or column == prediction_column:
            pass
        else:
            fig, axs = plt.subplots(1, 2, figsize=(20, 10), sharey="row")

            ax1, ax2 = axs

            ax1.scatter(df_reference[column], df_reference[prediction_prob_column])
            ax2.scatter(df_monitoring[column], df_monitoring[prediction_prob_column])

            ax1.set_title("Reference")
            ax1.set_xlabel(column)
            ax1.set_ylabel("Prediction Value")

            ax2.set_title("Monitoring")
            ax2.set_xlabel(column)
            figures_to_save.append(fig)
            plt.close()

    return tuple(figures_to_save)
