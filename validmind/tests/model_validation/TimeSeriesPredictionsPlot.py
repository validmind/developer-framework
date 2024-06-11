# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.graph_objects as go
import plotly.express as px


def TimeSeriesPredictionsPlot(datasets, models):
    """
    Plot actual vs predicted values for time series data
    """
    fig = go.Figure()

    # Use Plotly's color sequence for different model predictions
    colors = px.colors.qualitative.Plotly

    # Plot actual values from the first dataset
    dataset = datasets[0]
    time_index = dataset.df.index  # Assuming the index of the dataset is datetime
    fig.add_trace(
        go.Scatter(
            x=time_index,
            y=dataset.y,
            mode="lines",
            name="Actual Values",
            line=dict(color="blue"),
        )
    )

    # Plot predicted values for each dataset-model pair
    for idx, (dataset, model) in enumerate(zip(datasets, models)):
        model_name = model.input_id
        y_pred = dataset.y_pred(model)
        fig.add_trace(
            go.Scatter(
                x=time_index,
                y=y_pred,
                mode="lines",
                name=f"Predicted by {model_name}",
                line=dict(color=colors[idx % len(colors)]),
            )
        )

    # Update layout
    fig.update_layout(
        title="Time Series Actual vs Predicted Values",
        xaxis_title="Time",
        yaxis_title="Values",
        legend_title="Legend",
        template="plotly_white",
    )

    return fig
