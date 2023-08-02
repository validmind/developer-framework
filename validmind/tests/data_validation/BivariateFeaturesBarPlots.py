# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from dataclasses import dataclass
from validmind.vm_models import Figure, Metric


@dataclass
class BivariateFeaturesBarPlots(Metric):
    """
    Generates a visual analysis of categorical data by plotting bivariate feautres bar plots.
    The input dataset and features_pairs are required.
    """

    name = "bivariate_features_bar_plots"
    required_context = ["dataset"]
    default_params = {"features_pairs": None}

    def run(self):
        features_pairs = self.params["features_pairs"]

        figures = self.plot_bivariate_bar(features_pairs)

        return self.cache_results(figures=figures)

    def plot_bivariate_bar(self, features_pairs):
        status_var = self.dataset.target_column
        figures = []
        for x, hue in features_pairs.items():
            df = self.dataset.df

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
