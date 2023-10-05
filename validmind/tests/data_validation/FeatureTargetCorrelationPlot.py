# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class FeatureTargetCorrelationPlot(Metric):
    """
    **Purpose**: The purpose of this test is to visually analyze and display the correlations between different input
    features and the target output of a Machine Learning model. This is important in understanding how each feature
    impacts the model's predictions. A high correlation means the feature strongly influences the target variable -
    something particularly useful in feature selection and understanding model behaviour.

    **Test Mechanism**: The FeatureTargetCorrelationPlot test computes correlations between features and the target
    variable of a given dataset. The correlations are calculated and then plotted in a horizontal bar graph, with color
    varying according to the strength of the correlation. An automatic hover template is also provided for descriptive
    tooltips. The features to be analyzed can be specified, and the graph's height can be adjusted per requirement.

    **Signs of High Risk**: Absence of any strong correlations (either positive or negative) between features and the
    target variable might suggest a high risk as it indicates that the given features don't have a significant
    influence on the prediction output. Also, duplication of correlation values might indicate redundancy in feature
    selection.

    **Strengths**: This test provides a visual aid, significantly improving the interpretation of correlations and
    giving a clear, easy-to-understand overview of how each feature impacts the model's target variable. This aids in
    feature selection and in understanding the nature of model predictions. Additionally, the hover template provides
    precise correlation values for each feature, essential for a granular level understanding.

    **Limitations**: The test only works with numerical data, so variables of other types must be preprocessed. Also,
    the plot assumes a linear correlation - it cannot efficiently capture non-linear relationships. One more limitation
    is that it may not accurately reflect importance for models that use complex interactions of features, like
    Decision Trees or Neural Networks.
    """

    name = "feature_target_correlation_plot"
    required_inputs = ["dataset"]
    default_params = {"features": None, "fig_height": 600}
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "visualization", "feature_importance", "correlation"],
    }

    def run(self):
        features = self.params["features"]
        fig_height = self.params["fig_height"]

        if features is None:
            features = self.dataset.df.columns.to_list()
        else:
            features = self.params["features"]

        target_column = self.dataset.target_column

        # Filter DataFrame based on features and target_column
        df = self.dataset.df[features + [target_column]]

        figure = self.visualize_feature_target_correlation(
            df, target_column, fig_height
        )

        return self.cache_results(figures=figure)

    def visualize_feature_target_correlation(self, df, target_column, fig_height):
        # Compute correlations with the target variable
        correlations = df.corr(numeric_only=True)[target_column].drop(target_column)
        correlations = correlations.loc[:, ~correlations.columns.duplicated()]

        correlations = correlations.sort_values(by=target_column, ascending=True)

        # Create a gradual color map from red (1) to blue (-1)
        color_map = np.linspace(1, -1, len(correlations))
        colors = [
            f"rgb({int(255 * (1 - val))}, 0, {int(255 * (1 + val))})"
            for val in color_map
        ]

        # Create a horizontal bar plot with gradual color mapping
        fig = go.Figure(
            data=go.Bar(
                x=correlations[target_column],
                y=correlations.index,
                orientation="h",
                marker=dict(color=colors),
                hovertemplate="Feature: %{y}<br>Correlation: %{x:.2f}<extra></extra>",  # Hover template for tooltips
            )
        )

        # Set the title and axis labels
        fig.update_layout(
            title=f"Correlations of Features vs Target Variable ({target_column})",
            xaxis_title="",
            yaxis_title="",
            height=fig_height,  # Adjust the height value as needed
        )

        figure = Figure(for_object=self, key=self.key, figure=fig)
        return [figure]
