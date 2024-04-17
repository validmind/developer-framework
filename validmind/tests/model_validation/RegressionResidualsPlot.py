# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import plotly.figure_factory as ff
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class RegressionResidualsPlot(Metric):
    """
    Evaluates regression model performance by visualizing discrepancy distribution and modeling predicted vs actual
    value fit.

    **Purpose:**
    The `RegressionResidualsPlot` metric is utilized to assess the performance of regression models. The metric
    generates two visualizations: a distribution plot of residuals and a scatter plot of true vs predicted values.
    These visualizations are used to evaluate the model's errors (residuals) and how closely predicted values align
    with actual values.

    **Test Mechanism:**
    In the given Python code snippet, the mechanism initiates by extracting actual (y_true) and predicted (y_pred)
    values from the input data. The residuals are then calculated by subtracting the predicted values from the actual
    values. These residuals feed into a histogram for their distribution visualization. The code also generates a
    scatter plot comparing the true values with the predicted ones. The "Perfect Fit" line in the scatter plot
    represents an ideal scenario where true values and predicted values match perfectly.

    **Signs of High Risk:**
    - If residuals have a non-normal distribution, containing high-frequency extreme values.
    - In the scatter plot, predicted values are significantly deviating from the actual values.
    - Lower density around the "Perfect Fit" line in the scatter plot, which indicates inaccurate predictions.
    - In the case of residuals plot, obvious patterns or trends suggest that the model has not sufficiently captured
    the data's underlying structure.

    **Strengths:**
    - Direct visual representation of regression model's performance, offering intuitive interpretation.
    - Offers clear visual evidence of underfitting or overfitting models.
    - Capability to uncover trends or systematic deviations that could not be detected by numeric metrics.
    - Suitable for a wide range of regression models.

    **Limitations:**
    - Visual interpretations can be subjective and may lack precision compared to numerical metrics.
    - Difficulties might arise when interpreting in scenarios with multi-dimensional outputs due to the inherent
    two-dimensional nature of the plots.
    - Residuals plots can sometimes be hard to interpret if there are too many overlapping points.
    - The method doesn't provide a single, definitive number to capture model performance.
    """

    name = "regression_residuals_plot"
    required_inputs = ["model", "dataset"]
    metadata = {
        "task_types": ["regression"],
        "tags": [
            "model_performance",
        ],
    }

    def run(self):
        y_true = self.inputs.dataset.y
        y_pred = self.inputs.dataset.y_pred(self.inputs.model.input_id)
        # Calculate residuals
        residuals = y_true.flatten() - y_pred.flatten()
        # Create residuals plot
        hist_data = [residuals]
        group_labels = ["Residuals"]  # Names of the dataset

        fig = ff.create_distplot(
            hist_data, group_labels, bin_size=[0.1], show_hist=True, show_rug=False
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
        max_val = max(max(y_true), max(y_pred))
        min_val = min(min(y_true), min(y_pred))
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
