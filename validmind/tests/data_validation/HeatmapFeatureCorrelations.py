# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import Figure, Metric


@dataclass
class HeatmapFeatureCorrelations(Metric):
    """
    Creates a heatmap to visually represent correlation patterns between pairs of numerical features in a dataset.

    **Purpose:** The HeatmapFeatureCorrelations metric is utilized to evaluate the degree of interrelationships between
    pairs of input features within a dataset. This metric allows us to visually comprehend the correlation patterns
    through a heatmap, which can be essential in understanding which features may contribute most significantly to the
    performance of the model. Features that have high intercorrelation can potentially reduce the model's ability to
    learn, thus impacting the overall performance and stability of the machine learning model.

    **Test Mechanism:** The metric executes the correlation test by computing the Pearson correlations for all pairs of
    numerical features. It then generates a heatmap plot using seaborn, a Python data visualization library. The
    colormap ranges from -1 to 1, indicating perfect negative correlation and perfect positive correlation
    respectively. A 'declutter' option is provided which, if set to true, removes variable names and numerical
    correlations from the plot to provide a more streamlined view. The size of feature names and correlation
    coefficients can be controlled through 'fontsize' parameters.

    **Signs of High Risk:**

    - Indicators of potential risk include features with high absolute correlation values.
    - A significant degree of multicollinearity might lead to instabilities in the trained model and can also result in
    overfitting.
    - The presence of multiple homogeneous blocks of high positive or negative correlation within the plot might
    indicate redundant or irrelevant features included within the dataset.

    **Strengths:**

    - The strength of this metric lies in its ability to visually represent the extent and direction of correlation
    between any two numeric features, which aids in the interpretation and understanding of complex data relationships.
    - The heatmap provides an immediate and intuitively understandable representation, hence, it is extremely useful
    for high-dimensional datasets where extracting meaningful relationships might be challenging.

    **Limitations:**

    - The central limitation might be that it can only calculate correlation between numeric features, making it
    unsuitable for categorical variables unless they are already numerically encoded in a meaningful manner.
    - It uses Pearson's correlation, which only measures linear relationships between features. It may perform poorly
    in cases where the relationship is non-linear.
    - Large feature sets might result in cluttered and difficult-to-read correlation heatmaps, especially when the
    'declutter' option is set to false.
    """

    name = "heatmap_feature_correlations"
    required_inputs = ["dataset"]
    default_params = {"declutter": None, "fontsize": None, "num_features": None}
    tasks = ["classification", "regression"]
    tags = ["tabular_data", "visualization", "correlation"]

    def run(self):
        features = self.params.get("features")
        declutter = self.params.get("declutter", False)
        fontsize = self.params.get("fontsize", 13)

        # Filter DataFrame based on num_features
        if features is None:
            df = self.inputs.dataset.df
        else:
            df = self.inputs.dataset.df[features]

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
