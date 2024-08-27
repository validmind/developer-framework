# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd
import plotly.graph_objects as go
from scipy.stats import kstest

from validmind import tags, tasks


@tags("regression")
@tasks("residual_analysis", "visualization")
def ModelPredictionResiduals(
    datasets, models, nbins=100, p_value_threshold=0.05, start_date=None, end_date=None
):
    """
    Assesses normality and behavior of residuals in regression models through visualization and statistical tests.

    ### Purpose

    The Model Prediction Residuals test aims to visualize the residuals of model predictions and assess their normality
    using the Kolmogorov-Smirnov (KS) test. It helps to identify potential issues related to model assumptions and
    effectiveness.

    ### Test Mechanism

    This test involves the following steps for each dataset-model pair:

    - Calculate the residuals by subtracting predicted values from the actual values.
    - Generate two types of plots: a time series plot of residuals and a histogram of residuals.
    - Perform the KS test to assess the normality of the residuals and summarize the results in a table.

    ### Signs of High Risk

    - Residuals are not normally distributed, indicating potential issues with model assumptions.
    - High skewness or kurtosis in the residuals, which may suggest model misspecification.

    ### Strengths

    - Provides clear visualizations of residuals over time and their distribution.
    - Includes statistical tests to assess the normality of residuals.
    - Helps in identifying potential model misspecifications and assumption violations.

    ### Limitations

    - Assumes that the dataset is provided as a DataFrameDataset object with a .df attribute to access the pandas
    DataFrame.
    - Only generates plots for datasets with a datetime index, resulting in errors for other types of indices.
    """

    figures = []
    summary = []

    for dataset, model in zip(datasets, models):
        df = dataset.df.copy()

        # Filter DataFrame by date range if specified
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]

        y_true = dataset.y
        y_pred = dataset.y_pred(model)
        residuals = y_true - y_pred

        # Plot residuals
        residuals_fig = go.Figure()
        residuals_fig.add_trace(
            go.Scatter(x=df.index, y=residuals, mode="lines", name="Residuals")
        )
        residuals_fig.update_layout(
            title=f"Residuals for {model.input_id}",
            xaxis_title="Date",
            yaxis_title="Residuals",
            font=dict(size=16),
            showlegend=False,
        )
        figures.append(residuals_fig)

        # Plot histogram of residuals
        hist_fig = go.Figure()
        hist_fig.add_trace(go.Histogram(x=residuals, nbinsx=nbins, name="Residuals"))
        hist_fig.update_layout(
            title=f"Histogram of Residuals for {model.input_id}",
            xaxis_title="Residuals",
            yaxis_title="Frequency",
            font=dict(size=16),
            showlegend=False,
        )
        figures.append(hist_fig)

        # Perform KS normality test
        ks_stat, p_value = kstest(
            residuals, "norm", args=(residuals.mean(), residuals.std())
        )
        ks_normality = "Normal" if p_value > p_value_threshold else "Not Normal"

        summary.append(
            {
                "Model": model.input_id,
                "KS Statistic": ks_stat,
                "p-value": p_value,
                "KS Normality": ks_normality,
                "p-value Threshold": p_value_threshold,
            }
        )

    # Create a summary DataFrame for the KS normality test results
    summary_df = pd.DataFrame(summary)

    return (summary_df, *figures)
