# Copyright © 2023 ValidMind Inc. All rights reserved.

import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


class TimeSeriesLinePlot(Metric):
    """
    **1. Purpose**:
    The "TimeSeriesLinePlot" metric is designed to generate and analyze time series data visual plots for model
    performance inspection purposes. This analysis manifests as line plots that represent various time series in the
    dataset. By visual plotting, the metric helps in the initial data inspection, which gives a sense of patterns,
    trends, seasonality, irregularity, and any anomalies that might occur over time in the given dataset.

    **2. Test Mechanism**:
    This Python class extracts the column names from the input dataset and iteratively generates line plots for each
    column. The Python library 'Plotly' is used for creating the line plots. For every column (representing a time
    series), a plot's time-series values are generated against the dataset's datetime index. Indexes that are not of
    datetime type will trigger a ValueError.

    **3. Signs of High Risk**:
    Red flags that could denote potential high risk scenarios include:
    * Time-series data lacking datetime indices
    * Non-existence of provided columns in the dataset
    * Anomalous patterns or irregularities seen in time-series plots indicating high model instability or predictive
    error potential

    **4. Strengths**:
    This metric comes with several favourable assets:
    * It succinctly visualizes complex time series data, facilitating easier interpretation and detection of temporal
    trends, patterns and anomalies.
    * It is highly adaptable and capable of functioning well with multiple time series within the same dataset.
    * By visual inspection, it allows the detection of anomalies and irregular patterns that could indicate a potential
    issue with the data or model performance.

    **5. Limitations**:
    Despite its numerous advantages, the metric has a few limitations:
    * The effectiveness of this metric relies heavily on the quality and patterns of the input time series data.
    * It's solely a visual inspection tool and does not provide quantitative measurement. This can be a disadvantage
    when the aim is to compare and rank multiple models or when precise, numeric diagnostics are required.
    * It assumes that the time specific data has already been transformed into a datetime index and requires the input
    data to be formatted appropriately.
    * It inherently lacks the ability to extract any deeper statistical insights from the time series data, making it
    less effective when dealing with complex data structures and phenomena.
    """

    name = "time_series_line_plot"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "visualization"],
    }

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
