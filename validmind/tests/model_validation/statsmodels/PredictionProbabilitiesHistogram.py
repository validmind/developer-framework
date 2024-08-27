# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import plotly.graph_objects as go
from matplotlib import cm

from validmind.vm_models import Figure, Metric


@dataclass
class PredictionProbabilitiesHistogram(Metric):
    """
    Assesses the predictive probability distribution for binary classification to evaluate model performance and
    potential overfitting or bias.

    ### Purpose

    The Prediction Probabilities Histogram test is designed to generate histograms displaying the Probability of
    Default (PD) predictions for both positive and negative classes in training and testing datasets. This helps in
    evaluating the performance of a logistic regression model, particularly for credit risk prediction.

    ### Test Mechanism

    The metric follows these steps to execute the test:
    - Extracts the target column from both the train and test datasets.
    - Uses the model's predict function to calculate probabilities.
    - Adds these probabilities as a new column to the training and testing dataframes.
    - Generates histograms for each class (0 or 1) within the training and testing datasets.
    - Sets different opacities for the histograms to enhance visualization.
    - Overlays the four histograms (two for training and two for testing) on two different subplot frames.
    - Returns a plotly graph object displaying the visualization.

    ### Signs of High Risk

    - Significant discrepancies between the histograms of training and testing data.
    - Large disparities between the histograms for the positive and negative classes.
    - Potential overfitting or bias indicated by significant issues.
    - Unevenly distributed probabilities suggesting inaccurate model predictions.

    ### Strengths

    - Offers a visual representation of the PD predictions made by the model, aiding in understanding its behavior.
    - Assesses both the training and testing datasets, adding depth to model validation.
    - Highlights disparities between classes, providing insights into class imbalance or data skewness.
    - Effectively visualizes risk spread, which is particularly beneficial for credit risk prediction.

    ### Limitations

    - Specifically tailored for binary classification scenarios and not suited for multi-class classification tasks.
    - Mainly applicable to logistic regression models, and may not be effective for other model types.
    - Provides a robust visual representation but lacks a quantifiable measure to assess model performance.
    """

    name = "prediction_probabilities_histogram"
    required_inputs = ["model", "datasets"]
    tasks = ["classification"]
    tags = ["tabular_data", "visualization", "credit_risk", "logistic_regression"]

    default_params = {"title": "Histogram of Predictive Probabilities"}

    @staticmethod
    def plot_prob_histogram(dataframes, dataset_titles, target_col, title):
        figures = []

        # Generate a colormap and convert to Plotly-accepted color format
        # Adjust 'viridis' to any other matplotlib colormap if desired
        colormap = cm.get_cmap("viridis")

        for i, (df, dataset_title) in enumerate(zip(dataframes, dataset_titles)):
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

            # Ensure classes are plotted in the specified order
            for class_value in sorted(df[target_col].unique()):
                fig.add_trace(
                    go.Histogram(
                        x=df[df[target_col] == class_value]["probabilities"],
                        opacity=0.75,
                        name=f"{dataset_title} {target_col} = {class_value}",
                        marker=dict(
                            color=color_dict[class_value],
                        ),
                    )
                )
            fig.update_layout(
                barmode="overlay",
                title_text=f"{title} - {dataset_title}",
                xaxis_title="Probability",
                yaxis_title="Frequency",
            )
            figures.append(fig)
        return figures

    def run(self):
        dataset_titles = [dataset.input_id for dataset in self.inputs.datasets]
        target_column = self.inputs.datasets[0].target_column
        title = self.params.get("title", self.default_params["title"])

        dataframes = []
        metric_value = {"prob_histogram": {}}
        for _, dataset in enumerate(self.inputs.datasets):
            df = dataset.df.copy()
            y_prob = dataset.y_prob(self.inputs.model)
            df["probabilities"] = y_prob
            dataframes.append(df)
            metric_value["prob_histogram"][dataset.input_id] = list(df["probabilities"])

        figures = self.plot_prob_histogram(
            dataframes, dataset_titles, target_column, title
        )

        figures_list = [
            Figure(
                for_object=self,
                key=f"prob_histogram_{title.replace(' ', '_')}_{i+1}",
                figure=fig,
            )
            for i, fig in enumerate(figures)
        ]

        return self.cache_results(metric_value=metric_value, figures=figures_list)
