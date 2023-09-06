# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class IQROutliersBarPlot(Metric):
    """
    Generates a visual analysis of the outliers for numeric variables based on percentiles.
    The input dataset is required.
    """

    name = "iqr_outliers_bar_plot"
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

            Q1_count = outliers[
                (outliers >= 0) & (outliers < outliers.quantile(0.25))
            ].count()
            Q2_count = outliers[
                (outliers >= outliers.quantile(0.25)) & (outliers < outliers.median())
            ].count()
            Q3_count = outliers[
                (outliers >= outliers.median()) & (outliers < outliers.quantile(0.75))
            ].count()
            Q4_count = outliers[
                (outliers >= outliers.quantile(0.75)) & (outliers <= outliers.max())
            ].count()

            # Prepare data for bar plot
            bar_data = [Q1_count, Q2_count, Q3_count, Q4_count]
            percentile_labels = [
                "0-25",
                "25-50",
                "50-75",
                "75-100",
            ]

            # Create a bar plot
            fig = go.Figure(
                data=[go.Bar(x=percentile_labels, y=bar_data, marker_color="skyblue")]
            )

            # Set layout properties
            fig.update_layout(
                title_text=col,
                width=fig_width,
                height=400,
                plot_bgcolor="white",
                xaxis_title="Percentile",
                yaxis_title="Outlier Count",
            )

            # Create a Figure object and append to figures list
            figure = Figure(for_object=self, key=f"{self.key}:{col}", figure=fig)
            figures.append(figure)

        return self.cache_results(figures=figures)
