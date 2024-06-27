# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from validmind.vm_models import Figure, Metric


@dataclass
class BivariateFeaturesBarPlots(Metric):
    """
    Generates visual bar plots to analyze the relationship between paired features within categorical data in the model.

    **Purpose**: The BivariateFeaturesBarPlots metric is intended to perform a visual analysis of categorical data
    within the model. The goal is to assess and understand the specific relationships between various feature pairs,
    while simultaneously highlighting the model's target variable. This form of bivariate plotting is immensely
    beneficial in uncovering trends, correlations, patterns, or inconsistencies that may not be readily apparent within
    raw tabular data.

    **Test Mechanism**: These tests establish bar plots for each pair of features defined within the parameters. The
    dataset is grouped by each feature pair and then calculates the mean of the target variable within each specific
    grouping. Each group is represented via a bar in the plot, and the height of this bar aligns with the calculated
    mean. The colors assigned to these bars are based on the categorical section to which they pertain: these colors
    can either come from a colormap or generated anew if the total number of categories exceeds the current colormap's
    scope.

    **Signs of High Risk**:
    - If any values are found missing or inconsistent within the feature pairs.
    - If there exist large discrepancies or irregularities between the mean values of certain categories within feature
    pairs.
    - If the parameters for feature pairs have not been specified or if they were wrongly defined.

    **Strengths**:
    - The BivariateFeaturesBarPlots provides a clear, visual comprehension of the relationships between feature pairs
    and the target variable.
    - It allows an easy comparison between different categories within feature pairs.
    - The metric can handle a diverse array of categorical data, enhancing its universal applicability.
    - It is highly customizable due to its allowance for users to define feature pairs based on their specific
    requirements.

    **Limitations**:
    - It can only be used with categorical data, limiting its usability with numerical or textual data.
    - It relies on manual input for feature pairs, which could result in the overlooking of important feature pairs if
    not chosen judiciously.
    - The generated bar plots could become overly cluttered and difficult to decipher when dealing with feature pairs
    with a large number of categories.
    - This metric only provides a visual evaluation and fails to offer any numerical or statistical measures to
    quantify the relationship between feature pairs.
    """

    name = "bivariate_features_bar_plots"
    required_inputs = ["dataset"]
    default_params = {"features_pairs": None}
    tasks = ["classification"]
    tags = [
        "tabular_data",
        "categorical_data",
        "binary_classification",
        "multiclass_classification",
        "visualization",
    ]

    def run(self):
        features_pairs = self.params["features_pairs"]

        if features_pairs is None:
            raise ValueError(
                "The features_pairs parameter is required for this metric."
            )

        figures = self.plot_bivariate_bar(features_pairs)

        return self.cache_results(figures=figures)

    def plot_bivariate_bar(self, features_pairs):
        status_var = self.inputs.dataset.target_column
        figures = []
        for x, hue in features_pairs.items():
            df = self.inputs.dataset.df

            means = df.groupby([x, hue])[status_var].mean().unstack().reset_index()
            hue_categories = means.columns[1:]

            n = len(hue_categories)
            width = 1 / (n + 1)

            plt.figure()

            # Number of colors in the colormap
            num_colors = len(plt.cm.get_cmap("tab10").colors)

            if n <= num_colors:
                # Use the colors from the colormap if there are enough
                color_palette = {
                    category: color
                    for category, color in zip(
                        hue_categories, plt.cm.get_cmap("tab10").colors
                    )
                }
            else:
                # Generate a larger set of colors if needed
                hues = np.linspace(0, 1, n + 1)[
                    :-1
                ]  # exclude the last value which is equal to 1
                color_palette = {
                    category: mcolors.hsv_to_rgb(
                        (h, 1, 1)
                    )  # replace 1, 1 with desired saturation and value
                    for category, h in zip(hue_categories, hues)
                }

            for i, hue_category in enumerate(hue_categories):
                plt.bar(
                    np.arange(len(means)) + i * width,
                    means[hue_category],
                    color=color_palette[hue_category],
                    alpha=0.7,
                    label=hue_category,
                    width=width,
                )

            plt.title(x + " by " + hue)
            plt.xlabel(x)
            plt.ylabel("Default Ratio")
            plt.xticks(ticks=np.arange(len(means)), labels=means[x], rotation=90)
            plt.legend()
            plt.show()

            figures.append(
                Figure(
                    for_object=self, key=f"{self.key}:{x}_{hue}", figure=plt.figure()
                )
            )

        plt.close("all")

        return figures
