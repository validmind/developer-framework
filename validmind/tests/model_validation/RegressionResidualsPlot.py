# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class RegressionResidualsPlot(Metric):
    """
    Evaluates regression model performance using residual distribution and actual vs. predicted plots.

    ### Purpose

    The `RegressionResidualsPlot` metric aims to evaluate the performance of regression models. By generating and
    analyzing two plots – a distribution of residuals and a scatter plot of actual versus predicted values – this tool
    helps to visually appraise how well the model predicts and the nature of errors it makes.

    ### Test Mechanism

    The process begins by extracting the true output values (`y_true`) and the model's predicted values (`y_pred`).
    Residuals are computed by subtracting predicted from true values. These residuals are then visualized using a
    histogram to display their distribution. Additionally, a scatter plot is derived to compare true values against
    predicted values, together with a "Perfect Fit" line, which represents an ideal match (predicted values equal
    actual values), facilitating the assessment of the model's predictive accuracy.

    ### Signs of High Risk

    - Residuals showing a non-normal distribution, especially those with frequent extreme values.
    - Significant deviations of predicted values from actual values in the scatter plot.
    - Sparse density of data points near the "Perfect Fit" line in the scatter plot, indicating poor prediction
    accuracy.
    - Visible patterns or trends in the residuals plot, suggesting the model's failure to capture the underlying data
    structure adequately.

    ### Strengths

    - Provides a direct, visually intuitive assessment of a regression model’s accuracy and handling of data.
    - Visual plots can highlight issues of underfitting or overfitting.
    - Can reveal systematic deviations or trends that purely numerical metrics might miss.
    - Applicable across various regression model types.

    ### Limitations

    - Relies on visual interpretation, which can be subjective and less precise than numerical evaluations.
    - May be difficult to interpret in cases with multi-dimensional outputs due to the plots’ two-dimensional nature.
    - Overlapping data points in the residuals plot can complicate interpretation efforts.
    - Does not summarize model performance into a single quantifiable metric, which might be needed for comparative or
    summary analyses.
    """

    name = "regression_residuals_plot"
    required_inputs = ["model", "dataset"]
    tasks = ["regression"]
    tags = ["model_performance"]
    default_params = {"bin_size": 0.1}

    def run(self):
        y_true = self.inputs.dataset.y
        y_pred = self.inputs.dataset.y_pred(self.inputs.model)
        # Calculate residuals
        residuals = y_true.flatten() - y_pred.flatten()
        # Create residuals plot
        hist_data = [residuals]
        group_labels = ["Residuals"]  # Names of the dataset
        bin_size = self.params["bin_size"]
        fig = ff.create_distplot(
            hist_data, group_labels, bin_size=[bin_size], show_hist=True, show_rug=False
        )
        fig.update_layout(
            title="Distribution of Residuals",
            xaxis_title="Residuals",
            yaxis_title="Density",
        )
        figures = [
            Figure(
                for_object=self,
                key=self.key,
                figure=fig,
            )
        ]
        # Create a scatter plot of actual vs predicted values
        scatter = go.Scatter(
            x=y_true.flatten(),
            y=y_pred.flatten(),
            mode="markers",
            name="True vs Predicted",
            marker=dict(color="blue", opacity=0.5),
        )

        # Line of perfect prediction
        max_val = np.nanmax([np.nanmax(y_true), np.nanmax(y_pred)])
        min_val = np.nanmin([np.nanmin(y_true), np.nanmin(y_pred)])
        line = go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode="lines",
            name="Perfect Fit",
            line=dict(color="red", dash="dash"),
        )

        # Layout settings
        layout = go.Layout(
            title="True vs. Predicted Values",
            xaxis_title="True Values",
            yaxis_title="Predicted Values",
            showlegend=True,
        )

        fig = go.Figure(data=[scatter, line], layout=layout)

        figures.append(
            Figure(
                for_object=self,
                key=self.key,
                figure=fig,
            )
        )

        return self.cache_results(
            figures=figures,
        )
