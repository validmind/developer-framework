# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import Figure, Metric


@dataclass
class BivariateHistograms(Metric):
    """
    **Purpose**: This metric is used for visual data analysis, specifically for inspecting the distribution of
    categorical variables. By presenting bivariate histograms, the metric assists in assessing correlations between
    variables and distributions within each defined target class, giving us intuitive insights into the data's traits
    and potential patterns.

    **Test Mechanism**: The BivariateHistograms module requires an input dataset and a set of feature pairs. For each
    pair of features in the dataset, a bivariate histogram is drawn using seaborn's histogram plotting function. This
    histogram separates the data by the status of the target column, optionally restricted to a specific status by the
    *target_filter* parameter. The module creates two histograms for each pair - one for each variable, where colors
    distinguish between different target statuses.

    **Signs of High Risk**: High risk signs would be irregular or unexpected distributions of data among categories.
    For instance, extremely skewed distributions, differing significantly from normal or expected distributions, or
    large discrepancies in distribution patterns between different target states, might all be reasons for concern.

    **Strengths**: The key strength of this test lies in its simplicity and visualization power. It provides a quick,
    consolidated view of data distributions across different target conditions for each variable pair, highlighting
    potential correlations and patterns. This can be instrumental in detecting anomalies, understanding feature
    interactions, and driving exploratory data analysis.

    **Limitations**: This metric's limitations are inherent in its simplicity. The use of histograms might not be
    effective in identifying complex patterns or detailed intricacies in the data. There could also be an issue of
    overplotting with larger datasets. Additionally, this test only works with categorical data and may not provide
    useful insights for numerical or continuous variables. Also, the interpretation of the visual results depends a lot
    on the expertise of the observer.
    """

    name = "bivariate_histograms"
    required_inputs = ["dataset"]
    default_params = {"features_pairs": None, "target_filter": None}
    metadata = {
        "task_types": ["classification"],
        "tags": [
            "tabular_data",
            "categorical_data",
            "binary_classification",
            "multiclass_classification",
            "visualization",
        ],
    }

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

        if features_pairs is None:
            raise ValueError(
                "The features_pairs parameter is required for this metric."
            )

        figures = self.plot_bivariate_histogram(features_pairs, target_filter)

        return self.cache_results(figures=figures)
