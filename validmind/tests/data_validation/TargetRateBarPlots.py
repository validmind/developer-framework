# Copyright © 2023 ValidMind Inc. All rights reserved.

import plotly.graph_objs as go
from plotly.subplots import make_subplots
from validmind.vm_models import Figure, Metric


class TargetRateBarPlots(Metric):
    """
    Generates a visual analysis of target ratios by plotting bar plots.
    The input dataset can have multiple categorical variables if necessary.
    In this case, we produce a separate row of plots for each categorical variable.
    """

    name = "target_rate_bar_plots"
    required_context = ["dataset"]
    default_params = {"default_column": None, "columns": None}

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
                rows=1, cols=2, subplot_titles=("Counts", "Target Rate")
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
