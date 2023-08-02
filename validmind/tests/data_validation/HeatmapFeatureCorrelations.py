# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import seaborn as sns

from dataclasses import dataclass
from validmind.vm_models import Figure, Metric


@dataclass
class HeatmapFeatureCorrelations(Metric):
    """
    Generates a visual analysis of correlations by plotting a heatmap.
    The input dataset is required.
    """

    name = "heatmap_feature_correlations"
    required_context = ["dataset"]
    default_params = {"declutter": None, "fontsize": None, "num_features": None}

    def run(self):
        features = self.params["features"]
        declutter = self.params.get("declutter", False)
        fontsize = self.params.get("fontsize", 13)

        # Filter DataFrame based on num_features
        if features is None:
            df = self.dataset.df
        else:
            df = self.dataset.df[features]

        figure = self.visualize_correlations(df, declutter, fontsize)

        return self.cache_results(figures=figure)

    def visualize_correlations(self, df, declutter, fontsize):
        # Compute Pearson correlations
        correlations = df.corr(method="pearson")

        # Create a figure and axes
        fig, ax = plt.subplots()

        # If declutter option is true, do not show correlation coefficients and variable names
        if declutter:
            sns.heatmap(
                correlations,
                cmap="coolwarm",
                vmin=-1,
                vmax=1,
                ax=ax,
                cbar_kws={"label": "Correlation"},
            )
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_xlabel(f"{df.shape[1]} Numerical Features", fontsize=fontsize)
            ax.set_ylabel(f"{df.shape[1]} Numerical Features", fontsize=fontsize)
        else:
            # For the correlation numbers, you can use the 'annot_kws' argument
            sns.heatmap(
                correlations,
                cmap="coolwarm",
                vmin=-1,
                vmax=1,
                annot=True,
                fmt=".2f",
                ax=ax,
                cbar_kws={"label": "Correlation"},
                annot_kws={"size": fontsize},
            )
            plt.yticks(fontsize=fontsize)
            plt.xticks(rotation=90, fontsize=fontsize)

        # To set the fontsize of the color bar, you can iterate over its text elements and set their size
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(labelsize=fontsize)
        cbar.set_label("Correlation", size=fontsize)

        # Show the plot
        plt.tight_layout()
        plt.close("all")

        figure = Figure(for_object=self, key=self.key, figure=fig)
        return [figure]
