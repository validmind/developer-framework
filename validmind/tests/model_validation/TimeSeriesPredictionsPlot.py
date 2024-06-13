# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.express as px
import plotly.graph_objects as go

from validmind import tags, tasks


@tags("model_predictions", "visualization")
@tasks("regression", "time_series_forecasting")
def TimeSeriesPredictionsPlot(datasets, models):
    """
    Plot actual vs predicted values for time series data and generate a visual comparison for each model.

    **Purpose**: The purpose of this function is to visualize the actual versus predicted values for time series data across different models.

    **Test Mechanism**: The function iterates through each dataset-model pair, plots the actual values from the dataset, and overlays the predicted values from each model using Plotly for interactive visualization.

    **Signs of High Risk**:
    - Large discrepancies between actual and predicted values indicate poor model performance.
    - Systematic deviations in predicted values can highlight model bias or issues with data patterns.

    **Strengths**:
    - Provides a clear visual comparison of model predictions against actual values.
    - Uses Plotly for interactive and visually appealing plots.
    - Can handle multiple models and datasets, displaying them with distinct colors.

    **Limitations**:
    - Assumes that the dataset is provided as a DataFrameDataset object with a datetime index.
    - Requires that `dataset.y_pred(model)` returns the predicted values for the model.
    - Visualization might become cluttered with a large number of models or datasets.
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
