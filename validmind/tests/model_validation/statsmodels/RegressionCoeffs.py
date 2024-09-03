# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial


import pandas as pd
import plotly.graph_objects as go
from scipy import stats

from validmind.errors import SkipTestError
from validmind import tags, tasks


@tags("tabular_data", "visualization", "model_training")
@tasks("regression")
def RegressionCoeffs(model):
    """
    Assesses the significance and uncertainty of predictor variables in a regression model through visualization of
    coefficients and their 95% confidence intervals.

    ### Purpose

    The test visualizes regression coefficients along with their 95% confidence intervals to assess the impact of
    predictor variables on the response variable. This visualization offers insights into the variability and
    uncertainty of the model's estimates, helping to understand the significance of each predictor.

    ### Test Mechanism

    The test involves extracting the estimated coefficients and their standard errors from the regression model. It
    then calculates the confidence intervals at a 95% confidence level, which indicates the range within which the true
    value is expected to fall 95% of the time. This information is visualized using a bar plot, where the x-axis
    represents predictor variables, the y-axis represents coefficients, and the error bars depict the confidence
    intervals.

    ### Signs of High Risk

    - The confidence interval contains the zero value, indicating insignificant contribution from the feature.
    - Multiple coefficients exhibit confidence intervals containing zero, suggesting overall model reliability issues.
    - Very wide confidence intervals, indicating high uncertainty in the coefficient estimates.

    ### Strengths

    - Provides a clear and comprehensible visualization of the significance and impact of predictor variables.
    - Enables evaluation of uncertainty around each coefficient estimate through the inclusion of confidence intervals.

    ### Limitations

    - Assumes normality of residuals and independence of observations, which may not always hold true.
    - Does not address multi-collinearity, which can impact the interpretation of coefficients.
    - Limited to regression tasks and tabular datasets, and not applicable to other machine learning assignments or
    data structures.
    """

    if model.library != "statsmodels":
        raise SkipTestError("Only statsmodels are supported for this metric")

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
        title=f"{model.input_id} Coefficients with Confidence Intervals",
        xaxis_title="Predictor Variables",
        yaxis_title="Coefficients",
    )

    return (fig, coefficients)
