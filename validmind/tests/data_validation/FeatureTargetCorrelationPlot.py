# Copyright © 2023 ValidMind Inc. All rights reserved.

import plotly.graph_objects as go
import numpy as np
from dataclasses import dataclass
from validmind.vm_models import Figure, Metric


@dataclass
class FeatureTargetCorrelationPlot(Metric):
    """
    Generates a visual analysis of correlations between features and target by plotting a bar plot.
    The input dataset is required.
    """

    name = "feature_target_correlation_plot"
    required_context = ["dataset"]
    default_params = {"features": None, "fig_height": 600}

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
