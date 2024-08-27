# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.graph_objs as go
from plotly.subplots import make_subplots

from validmind.vm_models import Figure, Metric


class TargetRateBarPlots(Metric):
    """
    Generates bar plots visualizing the default rates of categorical features for a classification machine learning
    model.

    ### Purpose

    This test, implemented as a metric, is designed to provide an intuitive, graphical summary of the decision-making
    patterns exhibited by a categorical classification machine learning model. The model's performance is evaluated
    using bar plots depicting the ratio of target rates—meaning the proportion of positive classes—for different
    categorical inputs. This allows for an easy, at-a-glance understanding of the model's accuracy.

    ### Test Mechanism

    The test involves creating a pair of bar plots for each categorical feature in the dataset. The first plot depicts
    the frequency of each category in the dataset, with each category visually distinguished by its unique color. The
    second plot shows the mean target rate of each category (sourced from the "default_column"). Plotly, a Python
    library, is used to generate these plots, with distinct plots created for each feature. If no specific columns are
    selected, the test will generate plots for each categorical column in the dataset.

    ### Signs of High Risk

    - Inconsistent or non-binary values in the "default_column" could complicate or render impossible the calculation
    of average target rates.
    - Particularly low or high target rates for a specific category might suggest that the model is misclassifying
    instances of that category.

    ### Strengths

    - This test offers a visually interpretable breakdown of the model's decisions, providing an easy way to spot
    irregularities, inconsistencies, or patterns.
    - Its flexibility allows for the inspection of one or multiple columns, as needed.

    ### Limitations

    - The test is less useful when dealing with numeric or continuous data, as it's designed specifically for
    categorical features.
    - If the model in question is dealing with a multi-class problem rather than binary classification, the test's
    assumption of binary target values (0s and 1s) becomes a significant limitation.
    - The readability of the bar plots drops as the number of distinct categories increases in the dataset, which can
    make them harder to understand and less useful.
    """

    name = "target_rate_bar_plots"
    required_inputs = ["dataset"]
    default_params = {"default_column": None, "columns": None}
    tasks = ["classification"]
    tags = ["tabular_data", "visualization", "categorical_data"]

    def plot_loan_default_ratio(self, default_column, columns=None):
        df = self.inputs.dataset.df

        # Use all categorical features if columns is not specified, else use selected columns
        if columns is None:
            features = self.inputs.dataset.feature_columns_categorical
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

        unique_values = self.inputs.dataset.df[default_column].unique()
        binary_values = [0, 1]

        if sorted(unique_values) != binary_values:
            raise ValueError(
                f"The column {default_column} is not binary. It contains: {unique_values}"
            )

        print(f"The column {default_column} is correct and contains only 1 and 0.")

    def run(self):
        default_column = (
            self.params.get("default_column") or self.inputs.dataset.target_column
        )
        columns = self.params["columns"]

        # Check loan status variable has only 1 and 0
        self.check_default_column(default_column)

        return self.plot_loan_default_ratio(
            default_column=default_column, columns=columns
        )
