# Copyright © 2023 ValidMind Inc. All rights reserved.

import plotly.graph_objects as go

from dataclasses import dataclass
from validmind.vm_models import Figure, Metric


@dataclass
class MissingValuesBarPlot(Metric):
    """
    Generates a visual analysis of missing values by plotting horizontal bar plots with colored bars and a threshold line.
    The input dataset is required.
    """

    name = "missing_values_bar_plot"
    required_context = ["dataset"]
    default_params = {"threshold": 80, "fig_height": 600}

    def run(self):
        threshold = self.params["threshold"]
        fig_height = self.params["fig_height"]

        figure = self.visualize_missing_values(threshold, fig_height)

        return self.cache_results(figures=figure)

    def visualize_missing_values(self, threshold, fig_height):
        # Calculate the percentage of missing values in each column
        missing_percentages = (
            self.dataset.df.isnull().sum() / len(self.dataset.df)
        ) * 100

        # Only keep entries where missing_percentage > 0
        missing_percentages = missing_percentages[missing_percentages > 0]

        # Sort missing value percentages in ascending order
        missing_percentages_sorted = missing_percentages.sort_values(ascending=True)

        # Create lists to store the x and y values for each bar
        y_below_threshold = []
        x_below_threshold = []
        y_above_threshold = []
        x_above_threshold = []

        # Iterate through the missing percentages and separate values based on the threshold
        for index, value in missing_percentages_sorted.items():
            if value < threshold:
                y_below_threshold.append(index)
                x_below_threshold.append(value)
            else:
                y_above_threshold.append(index)
                x_above_threshold.append(value)

        # Create bar traces for values below and above threshold
        trace_below_threshold = go.Bar(
            y=y_below_threshold,
            x=x_below_threshold,
            marker_color="grey",
            name="Below Threshold",
            orientation="h",
            hovertemplate="Column: %{y}<br>Missing Value Percentage: %{x:.2f}%",
        )

        trace_above_threshold = go.Bar(
            y=y_above_threshold,
            x=x_above_threshold,
            marker_color="lightcoral",
            name="Above Threshold",
            orientation="h",
            hovertemplate="Column: %{y}<br>Missing Value Percentage: %{x:.2f}%",
        )

        # Draw a red line at the specified threshold
        threshold_line = go.Scatter(
            y=missing_percentages_sorted.index,
            x=[threshold] * len(missing_percentages_sorted.index),
            mode="lines",
            name="Threshold: {}%".format(threshold),
            line=dict(color="red", dash="dash"),
        )

        # Create a layout
        layout = go.Layout(
            title="Missing Values",
            yaxis=dict(title="Columns"),
            xaxis=dict(title="Missing Value Percentage (%)", range=[0, 100]),
            barmode="stack",
            height=fig_height,
        )

        # Create a Figure object
        fig = go.Figure(
            data=[trace_below_threshold, trace_above_threshold, threshold_line],
            layout=layout,
        )

        figure = Figure(for_object=self, key=self.key, figure=fig)
        return [figure]
