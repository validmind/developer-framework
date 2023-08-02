# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import seaborn as sns

from dataclasses import dataclass
from validmind.vm_models import Figure, Metric


@dataclass
class BivariateHistograms(Metric):
    """
    Generates a visual analysis of categorical data by plotting bivariate histograms.
    The input dataset and variable_pairs are required.
    """

    name = "bivariate_histograms"
    required_context = ["dataset"]
    default_params = {"features_pairs": None, "target_filter": None}

    def plot_bivariate_histogram(self, features_pairs, target_filter):
        status_var = self.dataset.target_column
        figures = []
        palette = {0: (0.5, 0.5, 0.5, 0.8), 1: "tab:red"}

        for x, y in features_pairs.items():
            df = self.dataset.df
            if target_filter is not None:
                df = df[df[status_var] == target_filter]

            fig, axes = plt.subplots(2, 1)

            for ax, var in zip(axes, [x, y]):
                for status, color in palette.items():
                    subset = df[df[status_var] == status]
                    sns.histplot(
                        subset[var],
                        ax=ax,
                        color=color,
                        edgecolor=None,
                        kde=True,
                        label=status_var if status else "Non-" + status_var,
                    )

                ax.set_title(f"Histogram of {var} by {status_var}")
                ax.set_xlabel(var)
                ax.legend()

            plt.tight_layout()
            plt.show()

            figures.append(
                Figure(for_object=self, key=f"{self.key}:{x}_{y}", figure=plt.figure())
            )

        plt.close("all")

        return figures

    def run(self):
        features_pairs = self.params["features_pairs"]
        target_filter = self.params["target_filter"]

        figures = self.plot_bivariate_histogram(features_pairs, target_filter)

        return self.cache_results(figures=figures)
