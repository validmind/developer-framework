# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import evaluate
import matplotlib.pyplot as plt
import seaborn as sns

from validmind import tags, tasks


@tags("nlp", "text_data", "data_validation")
@tasks("nlp")
def Toxicity(dataset):
    """
    Analyzes the toxicity of text data within a dataset using a pre-trained toxicity model.

    This method loads a toxicity evaluation model and applies it to each text entry
    in the specified column of the dataset's dataframe. It returns a KDE plot visualizing the distribution
    of toxicity scores across the dataset.

    Args:
        dataset (Dataset): A dataset object which must have a `df` attribute (a pandas DataFrame)
            and a `text_column` attribute indicating the name of the column containing text.

    Returns:
        matplotlib.figure.Figure: A KDE plot visualizing the distribution of toxicity scores.
    """
    toxicity = evaluate.load("toxicity")
    input_text = dataset.df[dataset.text_column]
    toxicity_scores = toxicity.compute(predictions=list(input_text.values))["toxicity"]

    fig = plt.figure()
    ax = sns.kdeplot(
        x=toxicity_scores,
        fill=True,
        common_norm=False,
        palette="crest",
        alpha=0.5,
        linewidth=0,
    )
    ax.set_title(f"Toxicity score of {dataset.text_column} ")
    ax.set_xlabel("Toxicity score")
    plt.close("all")
    return fig
