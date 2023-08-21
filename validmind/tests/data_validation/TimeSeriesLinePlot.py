# Copyright © 2023 ValidMind Inc. All rights reserved.

import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


class TimeSeriesLinePlot(Metric):
    """
    Generates a visual analysis of time series data by plotting the
    raw time series. The input dataset can have multiple time series
    if necessary. In this case we produce a separate plot for each time series.
    """

    name = "time_series_line_plot"
    required_inputs = ["dataset"]

    def run(self):
        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        columns = list(self.dataset.df.columns)
        df = self.dataset.df

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        figures = []
        for col in columns:
            # Creating the figure using Plotly
            fig = go.Figure()

            fig.add_trace(go.Scatter(x=df.index, y=df[col], mode="lines", name=col))

            fig.update_layout(
                title={
                    "text": f"{col}",
                    "y": 0.95,
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top",
                },
                font=dict(size=16),
            )

            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{col}",
                    figure=fig,
                )
            )

        return self.cache_results(
            figures=figures,
        )
