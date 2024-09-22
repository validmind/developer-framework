# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class MissingValuesBarPlot(Metric):
    """
    Assesses the percentage and distribution of missing values in the dataset via a bar plot, with emphasis on
    identifying high-risk columns based on a user-defined threshold.

    ### Purpose

    The 'MissingValuesBarPlot' metric provides a color-coded visual representation of the percentage of missing values
    for each column in an ML model's dataset. The primary purpose of this metric is to easily identify and quantify
    missing data, which are essential steps in data preprocessing. The presence of missing data can potentially skew
    the model's predictions and decrease its accuracy. Additionally, this metric uses a pre-set threshold to categorize
    various columns into ones that contain missing data above the threshold (high risk) and below the threshold (less
    risky).

    ### Test Mechanism

    The test mechanism involves scanning each column in the input dataset and calculating the percentage of missing
    values. It then compares each column's missing data percentage with the predefined threshold, categorizing columns
    with missing data above the threshold as high-risk. The test generates a bar plot in which columns with missing
    data are represented on the y-axis and their corresponding missing data percentages are displayed on the x-axis.
    The color of each bar reflects the missing data percentage in relation to the threshold: grey for values below the
    threshold and light coral for those exceeding it. The user-defined threshold is represented by a red dashed line on
    the plot.

    ### Signs of High Risk

    - Columns with higher percentages of missing values beyond the threshold are high-risk. These are visually
    represented by light coral bars on the bar plot.

    ### Strengths

    - Helps in quickly identifying and quantifying missing data across all columns of the dataset.
    - Facilitates pattern recognition through visual representation.
    - Enables customization of the level of risk tolerance via a user-defined threshold.
    - Supports both classification and regression tasks, sharing its versatility.

    ### Limitations

    - It only considers the quantity of missing values, not differentiating between different types of missingness
    (Missing completely at random - MCAR, Missing at random - MAR, Not Missing at random - NMAR).
    - It doesn't offer insights into potential approaches for handling missing entries, such as various imputation
    strategies.
    - The metric does not consider possible impacts of the missing data on the model's accuracy or precision.
    - Interpretation of the findings and the next steps might require an expert understanding of the field.
    """

    name = "missing_values_bar_plot"
    required_inputs = ["dataset"]
    default_params = {"threshold": 80, "fig_height": 600}
    tasks = ["classification", "regression"]
    tags = ["tabular_data", "data_quality", "visualization"]

    def run(self):
        threshold = self.params["threshold"]
        fig_height = self.params["fig_height"]

        figure = self.visualize_missing_values(threshold, fig_height)

        return self.cache_results(figures=figure)

    def visualize_missing_values(self, threshold, fig_height):
        # Calculate the percentage of missing values in each column
        missing_percentages = (
            self.inputs.dataset.df.isnull().sum() / len(self.inputs.dataset.df)
        ) * 100

        # Only keep entries where missing_percentage > 0
        missing_percentages = missing_percentages[missing_percentages > 0]

        # Sort missing value percentages in ascending order
        missing_percentages_sorted = missing_percentages.sort_values(ascending=True)

        # Create lists to store the x and y values for each bar
        y_below_threshold = []
        x_below_threshold = []
        y_above_threshold = []
        x_above_threshold = []

        # Iterate through the missing percentages and separate values based on the threshold
        for index, value in missing_percentages_sorted.items():
            if value < threshold:
                y_below_threshold.append(index)
                x_below_threshold.append(value)
            else:
                y_above_threshold.append(index)
                x_above_threshold.append(value)

        # Create bar traces for values below and above threshold
        trace_below_threshold = go.Bar(
            y=y_below_threshold,
            x=x_below_threshold,
            marker_color="grey",
            name="Below Threshold",
            orientation="h",
            hovertemplate="Column: %{y}<br>Missing Value Percentage: %{x:.2f}%",
        )

        trace_above_threshold = go.Bar(
            y=y_above_threshold,
            x=x_above_threshold,
            marker_color="lightcoral",
            name="Above Threshold",
            orientation="h",
            hovertemplate="Column: %{y}<br>Missing Value Percentage: %{x:.2f}%",
        )

        # Draw a red line at the specified threshold
        threshold_line = go.Scatter(
            y=missing_percentages_sorted.index,
            x=[threshold] * len(missing_percentages_sorted.index),
            mode="lines",
            name="Threshold: {}%".format(threshold),
            line=dict(color="red", dash="dash"),
        )

        # Create a layout
        layout = go.Layout(
            title="Missing Values",
            yaxis=dict(title="Columns"),
            xaxis=dict(title="Missing Value Percentage (%)", range=[0, 100]),
            barmode="stack",
            height=fig_height,
        )

        # Create a Figure object
        fig = go.Figure(
            data=[trace_below_threshold, trace_above_threshold, threshold_line],
            layout=layout,
        )

        figure = Figure(for_object=self, key=self.key, figure=fig)
        return [figure]
