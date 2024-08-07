# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial


import matplotlib.pyplot as plt

from validmind import tags, tasks


@tags("visualization")
@tasks("monitoring")
def PredictionAcrossEachFeature(datasets):

    """
    This test shows visually the prediction using reference data and monitoring data
    across each individual feature. If there are significant differences in predictions
    across feature values from reference to monitoring dataset then futher investigation
    is needed as the model is producing predictions that are different then what was
    observed during the training of the model.
    """

    df_reference = datasets[0].df
    df_monitoring = datasets[1].df

    figures_to_save = []
    for column in df_reference:

        if column == "model_probabilities" or column == "model_prediction":
            pass
        else:
            fig, axs = plt.subplots(1, 2, figsize=(20, 10), sharey="row")

            ax1, ax2 = axs

            ax1.scatter(df_reference[column], df_reference["model_probabilities"])
            ax2.scatter(df_monitoring[column], df_monitoring["model_probabilities"])

            ax1.set_title("Reference")
            ax1.set_xlabel(column)
            ax1.set_ylabel("Prediction Value")

            ax2.set_title("Monitoring")
            ax2.set_xlabel(column)
            figures_to_save.append(fig)
            plt.close()

    return tuple(figures_to_save)
