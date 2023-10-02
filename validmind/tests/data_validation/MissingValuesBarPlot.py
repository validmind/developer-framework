# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class MissingValuesBarPlot(Metric):
    """
    **Purpose**: The 'MissingValuesBarPlot' metric generates a visual representation that highlights the percentage of
    missing values in each column of a dataset used in an ML model. This visualization is used to quickly identify and
    quantify missing data, a critical step in data preprocessing. Missing data can distort the predictions of an ML
    model and reduce its accuracy. The metric also applies a user-defined threshold to classify columns into those with
    missing data above (high-risk) and below (less-risk) the threshold.

    **Test Mechanism**: This metric scans through each column in the input dataset and calculates the percentage of
    missing values. It preferentially selects columns that have at least some missing data (more than 0%). Each
    column's missing data percentage is then examined against the predefined threshold. Columns with missing data above
    the threshold are classified as high-risk. A bar plot is then generated; columns with missing data are displayed on
    the y-axis, while their corresponding missing data percentages are plotted on the x-axis. Each bar's color is
    dictated by the missing data's percentage relation to the threshold. Values below the threshold are grey, while
    ones above are light coral. A red dashed line represents the user-defined threshold on the plot.

    **Signs of High Risk**: Columns in the dataset represented by light coral bars indicate a high risk. These columns
    have a higher percentage of missing values than the threshold. If a significant number of columns or crucial
    features fall into this category, it implies a substantial risk for reliable model performance.

    **Strengths**: This method offers a snapshot overview of missing data across all the dataset's columns, making it
    easier to identify problematic areas promptly. It not only helps with quantitative assessment but also with pattern
    recognition through its visual summary. The user-defined threshold allows a customized level of risk tolerance. It
    also supports classification and regression tasks, adding to its versatility.

    **Limitations**: This metric purely looks at the number of missing values and doesn't consider the type of
    missingness (MCAR, MAR, NMAR) or methods for handling missing entries (like imputation strategies). It also doesn't
    factor in the potential impact of missing data on the model's accuracy or precision. It might require expert
    understanding to interpret the findings and take appropriate action.
    """

    name = "missing_values_bar_plot"
    required_inputs = ["dataset"]
    default_params = {"threshold": 80, "fig_height": 600}
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "data_quality", "visualization"],
    }

    def run(self):
        threshold = self.params["threshold"]
        fig_height = self.params["fig_height"]

        figure = self.visualize_missing_values(threshold, fig_height)

        return self.cache_results(figures=figure)

    def visualize_missing_values(self, threshold, fig_height):
        # Calculate the percentage of missing values in each column
        missing_percentages = (
            self.dataset.df.isnull().sum() / len(self.dataset.df)
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
