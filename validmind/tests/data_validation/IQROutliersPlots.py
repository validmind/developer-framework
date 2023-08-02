# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import plotly.graph_objects as go
from dataclasses import dataclass
from validmind.vm_models import Figure, Metric


@dataclass
class IQROutliersPlots(Metric):
    """
    Generates a visual analysis of the outliers for numeric variables.
    The input dataset is required.
    """

    name = "iqr_outliers_plots"
    required_context = ["dataset"]
    default_params = {"threshold": 1.5, "num_features": None, "fig_width": 800}

    def run(self):
        df = self.dataset.df
        num_features = self.params["num_features"]
        threshold = self.params["threshold"]
        fig_width = self.params["fig_width"]

        # If num_features is None, use all numeric columns.
        # Otherwise, only use the columns provided in num_features.
        if num_features is None:
            df = df.select_dtypes(include=[np.number])
        else:
            df = df[num_features]

        return self.detect_and_visualize_outliers(df, threshold, fig_width)

    @staticmethod
    def compute_outliers(series, threshold=1.5):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return series[(series < lower_bound) | (series > upper_bound)]

    def detect_and_visualize_outliers(self, df, threshold, fig_width):
        num_cols = df.columns.tolist()

        figures = []

        for col in num_cols:
            # Compute outliers
            outliers = self.compute_outliers(df[col], threshold)

            # Create box trace
            box_trace = go.Box(
                y=df[col].dropna(),
                name="",
                boxpoints=False,  # do not show original data points
                marker_color="skyblue",
                line_color="skyblue",
            )

            # Create scatter trace of outliers
            outliers_trace = go.Scatter(
                x=[""] * len(outliers),
                y=outliers,
                mode="markers",
                name="Outliers",
                marker=dict(
                    color="red",
                    size=6,
                    opacity=0.5,
                ),
            )

            # Create figure and add traces
            fig = go.Figure(data=[box_trace, outliers_trace])

            # Set layout properties
            fig.update_layout(
                showlegend=False,
                title_text=col,
                width=fig_width,
                height=400,
                plot_bgcolor="white",
            )

            fig.update_xaxes(showticklabels=False, showgrid=True, gridcolor="LightGray")
            fig.update_yaxes(title_text="Value", showgrid=True, gridcolor="LightGray")

            # Create a Figure object and append to figures list
            figure = Figure(for_object=self, key=f"{self.key}:{col}", figure=fig)
            figures.append(figure)

        return self.cache_results(figures=figures)
