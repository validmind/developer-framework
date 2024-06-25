# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go
from scipy import stats

from validmind.errors import SkipTestError
from validmind.vm_models import Figure, Metric


@dataclass
class RegressionCoeffsPlot(Metric):
    """
    Visualizes regression coefficients with 95% confidence intervals to assess predictor variables' impact on response
    variable.

    **Purpose**: The Regression Coefficients with Confidence Intervals plot and metric aims to understand the impact of
    predictor variables on the response variable in question. This understanding is achieved via the visualization and
    analysis of the regression model by presenting the coefficients derived from the model along with their associated
    95% confidence intervals. By doing so, it offers insights into the variability and uncertainty associated with the
    model's estimates.

    **Test Mechanism**: The test begins by extracting the estimated coefficients and their related standard errors from
    the regression model under test. It then calculates and draws confidence intervals based on a 95% confidence level
    (a standard convention in statistics). These intervals provide a range wherein the true value can be expected to
    fall 95% of the time if the same regression were re-run multiple times with samples drawn from the same population.
    This information is then visualized as a bar plot, with the predictor variables and their coefficients on the
    x-axis and y-axis respectively and the confidence intervals represented as error bars.

    **Signs of High Risk**:
    * If the calculated confidence interval contains the zero value, it could mean the feature/coefficient in question
    doesn't significantly contribute to prediction in the model.
    * If there are multiple coefficients exhibiting this behavior, it might raise concerns about overall model
    reliability.
    * Very wide confidence intervals might indicate high uncertainty in the associated coefficient estimates.

    **Strengths**:
    * This metric offers a simple and easily comprehendible visualization of the significance and impact of individual
    predictor variables in a regression model.
    * By including confidence intervals, it enables an observer to evaluate the uncertainty around each coefficient
    estimate.

    **Limitations**:
    * The test is dependent on a few assumptions about the data, namely normality of residuals and independence of
    observations, which may not always be true for all types of datasets.
    * The test does not consider multi-collinearity (correlation among predictor variables), which can potentially
    distort the model and make interpretation of coefficients challenging.
    * The test's application is limited to regression tasks and tabular datasets and is not suitable for other types of
    machine learning assignments or data structures.
    """

    name = "regression_coeffs_plot"
    required_inputs = ["models"]
    tasks = ["regression"]
    tags = ["tabular_data", "visualization", "model_interpretation"]

    @staticmethod
    def plot_coefficients_with_ci(model, model_name):
        # Extract estimated coefficients and standard errors
        coefficients = model.regression_coefficients()
        coef = pd.to_numeric(coefficients["coef"])
        std_err = pd.to_numeric(coefficients["std err"])

        # Calculate confidence intervals
        confidence_level = 0.95  # 95% confidence interval
        z_value = stats.norm.ppf((1 + confidence_level) / 2)  # Calculate Z-value
        lower_ci = coef - z_value * std_err
        upper_ci = coef + z_value * std_err

        # Create a bar plot with confidence intervals
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=list(coefficients["Feature"].values),
                y=coef,
                name="Estimated Coefficients",
                error_y=dict(
                    type="data",
                    symmetric=False,
                    arrayminus=lower_ci,
                    array=upper_ci,
                    visible=True,
                ),
            )
        )

        fig.update_layout(
            title=f"{model_name} Coefficients with Confidence Intervals",
            xaxis_title="Predictor Variables",
            yaxis_title="Coefficients",
        )

        return fig, {
            "values": list(coef),
            "lower_ci": list(lower_ci),
            "upper_ci": list(upper_ci),
        }

    def run(self):
        # Check models list is not empty
        if not self.inputs.models:
            raise ValueError("List of models must be provided in the models parameter")

        all_models = []
        all_figures = []
        all_metric_values = []

        if self.inputs.models is not None:
            all_models.extend(self.inputs.models)

        for i, model in enumerate(all_models):
            if model.library != "statsmodels":
                raise SkipTestError("Only statsmodels are supported for this metric")

            model_name = f"Model {i+1}"

            fig, metric_values = self.plot_coefficients_with_ci(model, model_name)
            all_figures.append(
                Figure(
                    for_object=self,
                    key=f"{model_name}_coefficients_ci_plot",
                    figure=fig,
                )
            )
            all_metric_values.append({"name": model_name, "metrics": metric_values})

        return self.cache_results(
            metric_value=all_metric_values,
            figures=all_figures,
        )
