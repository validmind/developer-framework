# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go
from scipy import stats

from validmind.vm_models import Figure, Metric


@dataclass
class RegressionCoeffsPlot(Metric):
    """
    **Purpose**: The Regression Coefficients with Confidence Intervals plot and metric is used to gain an understanding
    of the impacts of predictor variables on the response variable under examination. It enables the visualization and
    analysis of the regression model by displaying the set of coefficients derived from the model and their associated
    95% confidence intervals. This provides insight into the variability and uncertainty associated with the model's
    estimates.

    **Test Mechanism**: The test extracts the estimated coefficients and their associated standard errors from the
    regression model. Then, it calculates and draws confidence intervals using a 95% confidence level (standard
    convention in statistics), which provides an indication of the range where the true value can be expected to fall
    in 95% of the samples. For instance, if the same regression were run multiple times with samples taken from the
    same population. The process then visualizes these as a bar plot, with predictor variables on the x-axis and their
    corresponding coefficients on the y-axis, and the calculated upper and lower margins of the confidence intervals
    being illustrated as error bars.

    **Signs of High Risk**: If the zero value (indicating no effect) is within the calculated confidence interval, it
    suggests that that particular feature/coefficient may not significantly contribute to prediction in the model. If
    multiple coefficients demonstrate this behavior, the overall reliability of the model could be questioned.
    Additionally, very wide confidence intervals could suggest high uncertainty in the associated coefficient estimates.

    **Strengths**: This metric provides a straightforward and easily understood visualization of the significance and
    impact of the individual predictor variables in a regression model. The inclusion of confidence intervals allows
    for an examination of the uncertainty around each coefficient estimate.

    **Limitations**: This test is reliant on certain assumptions about the data: it assumes normality of the residuals
    and independence of observations, which might not be the case in all types of datasets. Additionally, it does not
    take into account multi-collinearity (correlation between predictor variables), which can distort the model and
    make interpretation of the coefficients difficult. Finally, this test is only applicable to regression tasks and
    tabular data sets, and is not suitable for other types of machine learning tasks or data structures.
    """

    name = "regression_coeffs_plot"
    required_inputs = ["models"]
    metadata = {
        "task_types": ["regression"],
        "tags": ["tabular_data", "visualization", "model_interpretation"],
    }

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
        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")

        all_models = []
        all_figures = []
        all_metric_values = []

        if self.models is not None:
            all_models.extend(self.models)

        for i, model in enumerate(all_models):
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
