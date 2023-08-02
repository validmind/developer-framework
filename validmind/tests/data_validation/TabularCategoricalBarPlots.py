# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from validmind.vm_models import Figure, Metric


class TabularCategoricalBarPlots(Metric):
    """
    Generates a visual analysis of categorical data by plotting bar plots.
    The input dataset can have multiple categorical variables if necessary.
    In this case, we produce a separate plot for each categorical variable.
    """

    name = "tabular_categorical_bar_plots"
    required_context = ["dataset"]

    def run(self):
        df = self.dataset.df

        # Extract categorical columns from the dataset
        categorical_columns = df.select_dtypes(
            include=[np.object, pd.Categorical]
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
