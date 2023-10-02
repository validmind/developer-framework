# Copyright © 2023 ValidMind Inc. All rights reserved.

import plotly.graph_objs as go
from plotly.subplots import make_subplots

from validmind.vm_models import Figure, Metric


class TargetRateBarPlots(Metric):
    """
    **Purpose**: The purpose of this metric is to visually summarize the distinct categorizations made by a
    classification-oriented machine learning model. Specifically, it generates bar plots representing target rate
    ratios for different categorical variables within the input dataset. This makes it easier to evaluate the
    performance of the classification model and gain quick insights into its accuracy.

    **Test Mechanism**: The test mechanic involves the creation of two bar plots for each categorical feature in the
    dataset. The first plot counts the number of times each category appears in the dataset, using a unique color to
    facilitate identification. On the second plot, it calculates the average target rate for each category and plots
    these averages. The target rate value comes from the column specified as "default_column." The plots are generated
    using the Plotly library in Python, with subplots created for each feature. If no specific columns are indicated,
    all categorical feature columns in the dataset will be used to generate the plot.

    **Signs of High Risk**: High risk or failure signs might involve inconsistent or non-binary values in the
    "default_column," making it difficult to calculate a meaningful default rate. Another risk sign could be an
    unusually low or high default rate for any particular category, suggesting the model might be wrongly classifying
    data points for those categories.

    **Strengths**: The main strength of this metric is its ability to provide a clear, visual representation of the
    model's categorization patterns. This helps stakeholders spot anomalies, inconsistencies, or trends in model
    behavior quickly. The metric is also flexible, allowing for the examination of a single column or multiple columns
    in the data.

    **Limitations**: This metric only works well with categorical data, limiting its application to numeric or
    continuous variables. It also assumes binary target values (only 0s and 1s), making it less useful for multi-class
    problems. The bar plots can become confusing and less interpretable if the dataset has too many distinct categories.
    """

    name = "target_rate_bar_plots"
    required_inputs = ["dataset"]
    default_params = {"default_column": None, "columns": None}
    metadata = {
        "task_types": ["classification"],
        "tags": ["tabular_data", "visualization", "categorical_data"],
    }

    def plot_loan_default_ratio(self, default_column, columns=None):
        df = self.dataset.df

        # Use all categorical features if columns is not specified, else use selected columns
        if columns is None:
            features = self.dataset.get_categorical_features_columns()
        else:
            features = columns

        figures = []
        for feature in features:
            fig = make_subplots(
                rows=1,
                cols=2,
            )

            # Calculate counts and default rate for each category
            counts = df[feature].value_counts()
            default_rate = df.groupby(feature)[default_column].mean()

            # Left plot: Counts
            fig.add_trace(
                go.Bar(
                    x=counts.index,
                    y=counts.values,
                    name="Counts",
                    marker_color="#6699cc",
                ),
                row=1,
                col=1,
            )

            # Right plot: Default rate
            fig.add_trace(
                go.Bar(
                    x=default_rate.index,
                    y=default_rate.values,
                    name="Target Rate",
                    marker_color="orange",
                ),
                row=1,
                col=2,
            )

            fig.update_layout(
                title_text=f"{feature}",  # title of plot
                autosize=False,
                width=500,
                height=400,
                margin=dict(l=50, r=50, b=100, t=100, pad=4),
            )

            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{feature}",
                    figure=fig,
                )
            )

        return self.cache_results(
            figures=figures,
        )

    def check_default_column(self, default_column):
        if default_column is None:
            raise ValueError("The default_column parameter needs to be specified.")

        unique_values = self.dataset.df[default_column].unique()
        binary_values = [0, 1]

        if sorted(unique_values) != binary_values:
            raise ValueError(
                f"The column {default_column} is not binary. It contains: {unique_values}"
            )

        print(f"The column {default_column} is correct and contains only 1 and 0.")

    def run(self):
        default_column = self.params["default_column"]
        columns = self.params["columns"]

        # Check loan status variable has only 1 and 0
        self.check_default_column(default_column)

        return self.plot_loan_default_ratio(
            default_column=default_column, columns=columns
        )
