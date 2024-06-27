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
    Generates and visualizes histograms of the Probability of Default predictions for both positive and negative
    classes in training and testing datasets.

    **Purpose**: This code is designed to generate histograms that display the Probability of Default (PD) predictions
    for positive and negative classes in both the training and testing datasets. By doing so, it evaluates the
    performance of a logistic regression model, particularly in the context of credit risk prediction.

    **Test Mechanism**: The metric executes these steps to run the test:
    - Firstly, it extracts the target column from both the train and test datasets.
    - The model's predict function is then used to calculate probabilities.
    - These probabilities are added as a new column to the training and testing dataframes.
    - Histograms are generated for each class (0 or 1 in binary classification scenarios) within the training and
    testing datasets.
    - To enhance visualization, the histograms are set to have different opacities.
    - The four histograms (two for training data and two for testing) are overlaid on two different subplot frames (one
    for training and one for testing data).
    - The test returns a plotly graph object displaying the visualization.

    **Signs of High Risk**: Several indicators could suggest a high risk or failure in the model's performance. These
    include:
    - Significant discrepancies observed between the histograms of training and testing data.
    - Large disparities between the histograms for the positive and negative classes.
    - These issues could signal potential overfitting or bias in the model.
    - Unevenly distributed probabilities may also indicate that the model does not accurately predict outcomes.

    **Strengths**: This metric and test offer several benefits, including:
    - The visual representation of the PD predictions made by the model, which aids in understanding the model's
    behaviour.
    - The ability to assess both the training and testing datasets, adding depth to the validation of the model.
    - Highlighting disparities between multiple classes, providing potential insights into class imbalance or data
    skewness issues.
    - Particularly beneficial for credit risk prediction, it effectively visualizes the spread of risk across different
    classes.

    **Limitations**: Despite its strengths, the test has several limitations:
    - It is specifically tailored for binary classification scenarios, where the target variable only has two classes;
    as such, it isn't suited for multi-class classification tasks.
    - This metric is mainly applicable for logistic regression models. It might not be effective or accurate when used
    on other model types.
    - While the test provides a robust visual representation of the model's PD predictions, it does not provide a
    quantifiable measure or score to assess model performance.
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
