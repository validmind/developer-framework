# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from validmind.vm_models import Figure, Metric


@dataclass
class BivariateFeaturesBarPlots(Metric):
    """
    **Purpose**: The BivariateFeaturesBarPlots metric is used to conduct a visual analysis of categorical data in the
    model. The primary aim is to evaluate and comprehend the relationship between different feature pairs while
    emphasizing the model's target variable. These bivariate plots are extremely useful in revealing trends,
    correlations, patterns or anomalies that might not be immediately obvious in tabular data.

    **Test Mechanism**: The test constructs bar plots for each feature pair defined in the parameters. It groups the
    dataset by each feature pair and calculates the mean of the target variable within each pair grouping. Each group
    is represented as a bar in the plot with the height of the bar corresponding to the calculated mean. The colors of
    the bars are determined by the specific category they belong to: either taken from a colormap or generated if the
    number of categories exceeds the colormap's capacity.

    **Signs of High Risk**: High risk or failure may be indicated if:

    1. Any values are missing or inconsistent in the feature pairs.
    2. Large differences or variations exist between the mean values of certain categories within the feature pairs.
    3. The parameters for feature pairs are not defined or are defined incorrectly.

    **Strengths**:

    1. BivariateFeaturesBarPlots provides a clear, visual understanding of the relationships between feature pairs and
    the target variable.
    2. It allows for easy comparison of different categories within the feature pairs.
    3. This metric can deal with a range of categorical data, thus increasing its broad applicability.
    4. It's highly customizable, as users can define the feature pairs based on their specific requirements.

    **Limitations**:

    1. It can only be used with categorical data, limiting its utility with numerical or text data.
    2. It's dependent on manual input for feature pairs, which may lead to overlooking important feature pairs if not
    chosen wisely.
    3. The generated bar plots can become very cluttered and hard to interpret when dealing with feature pairs with a
    large number of categories.
    4. This metric solely provides a visual analysis and doesn't provide any numerical or statistical measures for
    quantifying the relationship between feature pairs.
    """

    name = "bivariate_features_bar_plots"
    required_inputs = ["dataset"]
    default_params = {"features_pairs": None}
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

    def run(self):
        features_pairs = self.params["features_pairs"]

        if features_pairs is None:
            raise ValueError(
                "The features_pairs parameter is required for this metric."
            )

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
