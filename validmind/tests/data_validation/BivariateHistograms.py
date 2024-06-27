# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import Figure, Metric


@dataclass
class BivariateHistograms(Metric):
    """
    Generates bivariate histograms for paired features, aiding in visual inspection of categorical variables'
    distributions and correlations.

    **Purpose**: This metric, dubbed BivariateHistograms, is primarily used for visual data analysis via the inspection
    of variable distribution, specifically categorical variables. Its main objective is to ascertain any potential
    correlations between these variables and distributions within each defined target class. This is achieved by
    offering an intuitive avenue into gaining insights into the characteristics of the data and any plausible patterns
    therein.

    **Test Mechanism**: The working mechanism of the BivariateHistograms module revolves around an input dataset and a
    series of feature pairs. It uses seaborn's histogram plotting function and matplotlib techniques to create
    bivariate histograms for each feature pair in the dataset. Two histograms, stratified by the target column status,
    are produced for every pair of features. This enables the telling apart of different target statuses through color
    differentiation. The module also offers optional functionality for restricting the data by a specific status
    through the target_filter parameter.

    **Signs of High Risk**:
    - Irregular or unexpected distributions of data across the different categories.
    - Highly skewed data distributions.
    - Significant deviations from the perceived 'normal' or anticipated distributions.
    - Large discrepancies in distribution patterns between various target statuses.

    **Strengths**:
    - Owing to its simplicity, the histogram-based approach is easy to implement and interpret which translates to
    quick insights.
    - The metrics provides a consolidated view of the distribution of data across different target conditions for each
    variable pair, thereby assisting in highlighting potential correlations and patterns.
    - It proves advantageous in spotting anomalies, comprehending interactions among features, and facilitating
    exploratory data analysis.

    **Limitations**:
    - Its simplicity may be a drawback when it comes to spotting intricate or complex patterns in data.
    - Overplotting might occur when working with larger datasets.
    - The metric is only applicable to categorical data, and offers limited insights for numerical or continuous
    variables.
    - The interpretation of visual results hinges heavily on the expertise of the observer, possibly leading to
    subjective analysis.
    """

    name = "bivariate_histograms"
    required_inputs = ["dataset"]
    default_params = {"features_pairs": None, "target_filter": None}
    tasks = ["classification"]
    tags = [
        "tabular_data",
        "categorical_data",
        "binary_classification",
        "multiclass_classification",
        "visualization",
    ]

    def plot_bivariate_histogram(self, features_pairs, target_filter):
        status_var = self.inputs.dataset.target_column
        figures = []
        palette = {0: (0.5, 0.5, 0.5, 0.8), 1: "tab:red"}

        for x, y in features_pairs.items():
            df = self.inputs.dataset.df
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

        if features_pairs is None:
            raise ValueError(
                "The features_pairs parameter is required for this metric."
            )

        figures = self.plot_bivariate_histogram(features_pairs, target_filter)

        return self.cache_results(figures=figures)
