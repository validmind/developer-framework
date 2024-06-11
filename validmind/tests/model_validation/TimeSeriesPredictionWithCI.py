import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm


def TimeSeriesPredictionWithCI(dataset, model, confidence=0.95):
    """
    Plot actual vs predicted values for a time series with confidence intervals and compute breaches.
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
