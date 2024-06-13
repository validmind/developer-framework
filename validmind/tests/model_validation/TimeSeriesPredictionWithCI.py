# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm

from validmind import tags, tasks


@tags("model_predictions", "visualization")
@tasks("regression", "time_series_forecasting")
def TimeSeriesPredictionWithCI(dataset, model, confidence=0.95):
    """
    Plot actual vs predicted values for a time series with confidence intervals and compute breaches.

    **Purpose**: The purpose of this function is to visualize the actual versus predicted values for time series data, including confidence intervals, and to compute and report the number of breaches beyond these intervals.

    **Test Mechanism**: The function calculates the standard deviation of prediction errors, determines the confidence intervals, and counts the number of actual values that fall outside these intervals (breaches). It then generates a plot with the actual values, predicted values, and confidence intervals, and returns a DataFrame summarizing the breach information.

    **Signs of High Risk**:
    - A high number of breaches indicates that the model's predictions are not reliable within the specified confidence level.
    - Significant deviations between actual and predicted values may highlight model inadequacies or issues with data quality.

    **Strengths**:
    - Provides a visual representation of prediction accuracy and the uncertainty around predictions.
    - Includes a statistical measure of prediction reliability through confidence intervals.
    - Computes and reports breaches, offering a quantitative assessment of prediction performance.

    **Limitations**:
    - Assumes that the dataset is provided as a DataFrameDataset object with a datetime index.
    - Requires that `dataset.y_pred(model)` returns the predicted values for the model.
    - The calculation of confidence intervals assumes normally distributed errors, which may not hold for all datasets.
    """
    dataset_name = dataset.input_id
    model_name = model.input_id
    time_index = dataset.df.index  # Assuming the index of the dataset is datetime

    # Get actual and predicted values
    y_true = dataset.y
    y_pred = dataset.y_pred(model)

    # Compute the standard deviation of the errors
    errors = y_true - y_pred
    std_error = np.std(errors)

    # Compute z-score for the given confidence level
    z_score = norm.ppf(1 - (1 - confidence) / 2)

    # Compute confidence intervals
    lower_conf = y_pred - z_score * std_error
    upper_conf = y_pred + z_score * std_error

    # Calculate breaches
    upper_breaches = (y_true > upper_conf).sum()
    lower_breaches = (y_true < lower_conf).sum()
    total_breaches = upper_breaches + lower_breaches

    # Create DataFrame
    breaches_df = pd.DataFrame(
        {
            "Confidence Level": [confidence],
            "Total Breaches": [total_breaches],
            "Upper Breaches": [upper_breaches],
            "Lower Breaches": [lower_breaches],
        }
    )

    # Plotting
    fig = go.Figure()

    # Plot actual values
    fig.add_trace(
        go.Scatter(
            x=time_index,
            y=y_true,
            mode="lines",
            name="Actual Values",
            line=dict(color="blue"),
        )
    )

    # Plot predicted values
    fig.add_trace(
        go.Scatter(
            x=time_index,
            y=y_pred,
            mode="lines",
            name=f"Predicted by {model_name}",
            line=dict(color="red"),
        )
    )

    # Add confidence interval lower bound as an invisible line
    fig.add_trace(
        go.Scatter(
            x=time_index,
            y=lower_conf,
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            name="CI Lower",
        )
    )

    # Add confidence interval upper bound and fill area
    fig.add_trace(
        go.Scatter(
            x=time_index,
            y=upper_conf,
            mode="lines",
            fill="tonexty",
            fillcolor="rgba(200, 200, 200, 0.5)",
            line=dict(width=0),
            showlegend=True,
            name="Confidence Interval",
        )
    )

    # Update layout
    fig.update_layout(
        title=f"Time Series Actual vs Predicted Values for {dataset_name} and {model_name}",
        xaxis_title="Time",
        yaxis_title="Values",
        legend_title="Legend",
        template="plotly_white",
    )

    return fig, breaches_df
