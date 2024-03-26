# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd
import plotly.graph_objs as go

from validmind.vm_models import Figure, Metric


class TabularCategoricalBarPlots(Metric):
    """
    Generates and visualizes bar plots for each category in categorical features to evaluate dataset's composition.

    **Purpose**: The purpose of this metric is to visually analyze categorical data using bar plots. It is intended to
    evaluate the dataset's composition by displaying the counts of each category in each categorical feature.

    **Test Mechanism**: The provided dataset is first checked to determine if it contains any categorical variables. If
    no categorical columns are found, the tool raises a ValueError. For each categorical variable in the dataset, a
    separate bar plot is generated. The number of occurrences for each category is calculated and displayed on the
    plot. If a dataset contains multiple categorical columns, multiple bar plots are produced.

    **Signs of High Risk**:

    - High risk could occur if the categorical variables exhibit an extreme imbalance, with categories having very few
    instances possibly being underrepresented in the model, which could affect the model's performance and its ability
    to generalize.
    - Another sign of risk is if there are too many categories in a single variable, which could lead to overfitting
    and make the model complex.

    **Strengths**: This metric provides a visual and intuitively understandable representation of categorical data,
    which aids in the analysis of variable distributions. By presenting model inputs in this way, we can easily
    identify imbalances or rare categories that could affect the model's performance.

    **Limitations**:

    - This method only works with categorical data, meaning it won't apply to numerical variables.
    - In addition, the method does not provide any informative value when there are too many categories, as the bar
    chart could become cluttered and hard to interpret.
    - It offers no insights into the model's performance or precision, but rather provides a descriptive analysis of
    the input.
    """

    name = "tabular_categorical_bar_plots"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "visualization"],
    }

    def run(self):
        df = self.inputs.dataset.df

        # Extract categorical columns from the dataset
        categorical_columns = df.select_dtypes(
            include=[object, pd.Categorical]
        ).columns.tolist()

        if len(categorical_columns) == 0:
            raise ValueError("No categorical columns found in the dataset")

        # Define a color sequence for the categories
        color_sequence = [
            "#636EFA",
            "#EF553B",
            "#00CC96",
            "#AB63FA",
            "#FFA15A",
            "#19D3F3",
            "#FF6692",
            "#B6E880",
            "#FF97FF",
            "#FECB52",
        ]

        figures = []
        for col in categorical_columns:
            counts = df[col].value_counts()

            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=counts.index,
                    y=counts.values,
                    name=col,
                    marker_color=color_sequence[: len(counts)],
                )
            )  # add colored bar plot trace
            fig.update_layout(
                title_text=f"{col}",  # title of plot
                xaxis_title_text="",  # xaxis label
                yaxis_title_text="",  # yaxis label
                autosize=False,
                width=500,
                height=500,
                margin=dict(l=50, r=50, b=100, t=100, pad=4),
            )
            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{col}",
                    figure=fig,
                )
            )

        return self.cache_results(
            figures=figures,
        )
