# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


class TimeSeriesLinePlot(Metric):
    """
    Generates and analyses time-series data through line plots revealing trends, patterns, anomalies over time.

    ### Purpose

    The TimeSeriesLinePlot metric is designed to generate and analyze time series data through the creation of line
    plots. This assists in the initial inspection of the data by providing a visual representation of patterns, trends,
    seasonality, irregularity, and anomalies that may be present in the dataset over a period of time.

    ### Test Mechanism

    The mechanism for this Python class involves extracting the column names from the provided dataset and subsequently
    generating line plots for each column using the Plotly Python library. For every column in the dataset, a
    time-series line plot is created where the values are plotted against the dataset's datetime index. It is important
    to note that indexes that are not of datetime type will result in a ValueError.

    ### Signs of High Risk

    - Presence of time-series data that does not have datetime indices.
    - Provided columns do not exist in the provided dataset.
    - The detection of anomalous patterns or irregularities in the time-series plots, indicating potential high model
    instability or probable predictive error.

    ### Strengths

    - The visual representation of complex time series data, which simplifies understanding and helps in recognizing
    temporal trends, patterns, and anomalies.
    - The adaptability of the metric, which allows it to effectively work with multiple time series within the same
    dataset.
    - Enables the identification of anomalies and irregular patterns through visual inspection, assisting in spotting
    potential data or model performance problems.

    ### Limitations

    - The effectiveness of the metric is heavily reliant on the quality and patterns of the provided time series data.
    - Exclusively a visual tool, it lacks the capability to provide quantitative measurements, making it less effective
    for comparing and ranking multiple models or when specific numerical diagnostics are needed.
    - The metric necessitates that the time-specific data has been transformed into a datetime index, with the data
    formatted correctly.
    - The metric has an inherent limitation in that it cannot extract deeper statistical insights from the time series
    data, which can limit its efficacy with complex data structures and phenomena.
    """

    name = "time_series_line_plot"
    required_inputs = ["dataset"]
    tasks = ["regression"]
    tags = ["time_series_data", "visualization"]

    def run(self):
        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.inputs.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        columns = list(self.inputs.dataset.df.columns)
        df = self.inputs.dataset.df

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
