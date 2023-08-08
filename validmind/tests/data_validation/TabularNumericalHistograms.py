# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import plotly.graph_objs as go
from validmind.vm_models import Figure, Metric


class TabularNumericalHistograms(Metric):
    """
    Generates a visual analysis of numerical data by plotting the histogram.
    The input dataset can have multiple numerical variables if necessary.
    In this case, we produce a separate plot for each numerical variable.
    """

    name = "tabular_numerical_histograms"
    required_context = ["dataset"]

    def run(self):
        df = self.dataset.df

        # Extract numerical columns from the dataset
        numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numerical_columns) == 0:
            raise ValueError("No numerical columns found in the dataset")

        figures = []
        for col in numerical_columns:
            fig = go.Figure()
            fig.add_trace(
                go.Histogram(x=df[col], nbinsx=50, name=col)
            )  # add histogram trace
            fig.update_layout(
                title_text=f"{col}",  # title of plot
                xaxis_title_text="",  # xaxis label
                yaxis_title_text="",  # yaxis label
                bargap=0.2,  # gap between bars of adjacent location coordinates
                bargroupgap=0.1,  # gap between bars of the same location coordinates
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
