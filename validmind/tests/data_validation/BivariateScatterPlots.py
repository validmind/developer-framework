# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import seaborn as sns

from dataclasses import dataclass
from validmind.vm_models import Figure, Metric


@dataclass
class BivariateScatterPlots(Metric):
    """
    Generates a visual analysis of categorical data by plotting bivariate scatter plots.
    The input dataset and variable_pairs are required.
    """

    name = "bivariate_scatter_plots"
    required_context = ["dataset"]
    default_params = {"features_pairs": None, "target_filter": None}

    def plot_bivariate_scatter(self, features_pairs, target_filter):
        status_var = self.dataset.target_column
        figures = []
        for x, y in features_pairs.items():
            df = self.dataset.df
            if target_filter is not None:
                df = df[df[status_var] == target_filter]

            plt.figure()

            # Scatterplot using seaborn, with color variation based on 'status_var'
            # Create color mapping with rgba values, last value is alpha (transparency)
            palette = {0: (0.8, 0.8, 0.8, 0.8), 1: "tab:red"}
            plot = sns.scatterplot(
                data=df, x=x, y=y, hue=status_var, palette=palette, alpha=1
            )

            # Change legend labels
            legend_labels = [
                "Category 1" if t.get_text() == "1" else "Category 2"
                for t in plot.legend_.texts[1:]
            ]
            plot.legend_.texts[1:] = legend_labels

            plt.title(x + " and " + y)
            plt.xlabel(x)
            plt.ylabel(y)
            plt.show()

            figures.append(
                Figure(for_object=self, key=f"{self.key}:{x}_{y}", figure=plt.figure())
            )

        plt.close("all")

        return figures

    def run(self):
        features_pairs = self.params["features_pairs"]
        target_filter = self.params["target_filter"]

        figures = self.plot_bivariate_scatter(features_pairs, target_filter)

        return self.cache_results(figures=figures)
