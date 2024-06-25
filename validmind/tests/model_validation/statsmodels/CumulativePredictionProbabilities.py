# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go
from matplotlib import cm

from validmind.vm_models import Figure, Metric


@dataclass
class CumulativePredictionProbabilities(Metric):
    """
    Visualizes cumulative probabilities of positive and negative classes for both training and testing in logistic
    regression models.

    **Purpose**: This metric is utilized to evaluate the distribution of predicted probabilities for positive and
    negative classes in a logistic regression model. It's not solely intended to measure the model's performance but
    also provides a visual assessment of the model's behavior by plotting the cumulative probabilities for positive and
    negative classes across both the training and test datasets.

    **Test Mechanism**: The logistic regression model is evaluated by first computing the predicted probabilities for
    each instance in both the training and test datasets, which are then added as a new column in these sets. The
    cumulative probabilities for positive and negative classes are subsequently calculated and sorted in ascending
    order. Cumulative distributions of these probabilities are created for both positive and negative classes across
    both training and test datasets. These cumulative probabilities are represented visually in a plot, containing two
    subplots - one for the training data and the other for the test data, with lines representing cumulative
    distributions of positive and negative classes.

    **Signs of High Risk**:
    - Imbalanced distribution of probabilities for either positive or negative classes.
    - Notable discrepancies or significant differences between the cumulative probability distributions for the
    training data versus the test data.
    - Marked discrepancies or large differences between the cumulative probability distributions for positive and
    negative classes.

    **Strengths**:
    - It offers not only numerical probabilities but also provides a visual illustration of data, which enhances the
    ease of understanding and interpreting the model's behavior.
    - Allows for the comparison of model's behavior across training and testing datasets, providing insights about how
    well the model is generalized.
    - It differentiates between positive and negative classes and their respective distribution patterns, which can aid
    in problem diagnosis.

    **Limitations**:
    - Exclusive to classification tasks and specifically to logistic regression models.
    - Graphical results necessitate human interpretation and may not be directly applicable for automated risk
    detection.
    - The method does not give a solitary quantifiable measure of model risk, rather it offers a visual representation
    and broad distributional information.
    - If the training and test datasets are not representative of the overall data distribution, the metric could
    provide misleading results.
    """

    name = "cumulative_prediction_probabilities"
    required_inputs = ["model", "datasets"]
    tasks = ["classification"]
    tags = ["logistic_regression", "visualization"]

    default_params = {"title": "Cumulative Probabilities"}

    @staticmethod
    def plot_cumulative_prob(dataframes, dataset_titles, target_col, title):
        figures = []

        # Generate a colormap and convert to Plotly-accepted color format
        # Adjust 'viridis' to any other matplotlib colormap if desired
        colormap = cm.get_cmap("viridis")

        for _, (df, dataset_title) in enumerate(zip(dataframes, dataset_titles)):
            fig = go.Figure()

            # Get unique classes and assign colors
            classes = sorted(df[target_col].unique())
            colors = [
                colormap(i / len(classes))[:3] for i in range(len(classes))
            ]  # RGB
            color_dict = {
                cls: f"rgb({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)})"
                for cls, rgb in zip(classes, colors)
            }
            for class_value in sorted(df[target_col].unique()):
                # Calculate cumulative distribution for the current class
                sorted_probs = np.sort(
                    df[df[target_col] == class_value]["probabilities"]
                )
                cumulative_probs = np.cumsum(sorted_probs) / np.sum(sorted_probs)

                fig.add_trace(
                    go.Scatter(
                        x=sorted_probs,
                        y=cumulative_probs,
                        mode="lines",
                        name=f"{dataset_title} {target_col} = {class_value}",
                        line=dict(
                            color=color_dict[class_value],
                        ),
                    )
                )
            fig.update_layout(
                title_text=f"{title} - {dataset_title}",
                xaxis_title="Probability",
                yaxis_title="Cumulative Distribution",
                legend_title=target_col,
            )
            figures.append(fig)
        return figures

    def run(self):
        dataset_titles = [dataset.input_id for dataset in self.inputs.datasets]
        target_column = self.inputs.datasets[0].target_column
        title = self.params.get("title", self.default_params["title"])

        dataframes = []
        metric_value = {"cum_prob": {}}
        for dataset in self.inputs.datasets:
            df = dataset.df.copy()
            y_prob = dataset.y_prob(self.inputs.model)
            df["probabilities"] = y_prob
            dataframes.append(df)
            metric_value["cum_prob"][dataset.input_id] = list(df["probabilities"])

        figures = self.plot_cumulative_prob(
            dataframes, dataset_titles, target_column, title
        )

        figures_list = [
            Figure(
                for_object=self,
                key=f"cumulative_prob_{title.replace(' ', '_')}_{i+1}",
                figure=fig,
            )
            for i, fig in enumerate(figures)
        ]

        return self.cache_results(metric_value=metric_value, figures=figures_list)
