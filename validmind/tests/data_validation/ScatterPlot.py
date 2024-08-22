# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import matplotlib.pyplot as plt
import seaborn as sns

from validmind import tags, tasks


@tags("tabular_data", "visualization")
@tasks("classification", "regression")
def ScatterPlot(dataset):
    """
    Creates a scatter plot matrix to visually analyze feature relationships, patterns, and outliers in a dataset.

    **Purpose**: The ScatterPlot metric is designed to offer a visual analysis of a given dataset by constructing a
    scatter plot matrix encapsulating the dataset's numerical features. Its primary function is to uncover
    relationships, patterns, or outliers across different features, thus providing both quantitative and qualitative
    insights into the multidimensional relationships within the dataset. This visual assessment aids in understanding
    the efficacy of the chosen features for model training and their overall suitability.

    **Test Mechanism**: Using the Plotly library, the ScatterPlot function creates the scatter plot matrix. The process
    involves retrieving all numerical columns from the dataset and subsequently generating a scatter matrix for these
    columns. The resulting Plotly figure provides interactive capabilities, enabling users to explore relationships
    between features dynamically. The final plot is returned as a Plotly Figure object for further analysis and
    visualization.

    **Signs of High Risk**:
    - The emergence of non-linear or random patterns across different feature pairs. This may suggest intricate
    relationships unfit for linear presumptions.
    - A lack of clear patterns or clusters, which might point to weak or non-existent correlations among features, thus
    creating challenges for certain model types.
    - The presence of outliers, as visual outliers in your data can adversely influence the model's performance.

    **Strengths**:
    - It provides insight into the multidimensional relationships among multiple features.
    - It assists in identifying trends, correlations, and outliers that could potentially affect the model's
    performance.
    - As a diagnostic tool, it can validate whether certain assumptions made during the model-creation process, such as
    linearity, hold true.
    - The tool's versatility extends to its application for both regression and classification tasks.
    - The use of Plotly offers interactive exploration of the data, which can be valuable for deeper analysis.

    **Limitations**:
    - Scatter plot matrices may become cluttered and hard to decipher as the number of features increases, leading to
    complexity and confusion.
    - While extremely proficient in revealing pairwise relationships, these matrices may fail to illuminate complex
    interactions that involve three or more features.
    - These matrices are primarily visual tools, so the precision of quantitative analysis may be compromised.
    - If not clearly visible, outliers can be missed, which could negatively affect model performance.
    - It assumes that the dataset can fit into the computer's memory, which might not always be valid, particularly for
    extremely large datasets.
    """

    g = sns.pairplot(data=dataset.df, diag_kind="kde")
    for ax in g.axes.flatten():
        # rotate x axis labels
        ax.set_xlabel(ax.get_xlabel(), rotation=45)
        # rotate y axis labels
        ax.set_ylabel(ax.get_ylabel(), rotation=45)
        # set y labels alignment
        ax.yaxis.get_label().set_horizontalalignment("right")
    # Get the current figure
    fig = plt.gcf()

    figures = []
    figures.append(fig)

    plt.close("all")

    return tuple(figures)
