# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class PearsonCorrelationMatrix(Metric):
    """
    Extracts the Pearson correlation coefficient for all pairs of numerical variables
    in the dataset. This metric is useful to identify highly correlated variables
    that can be removed from the dataset to reduce dimensionality.
    """

    name = "pearson_correlation_matrix"
    required_context = ["dataset"]

    def run(self):
        columns = self.params.get("columns", list(self.dataset.df.columns))

        corr_matrix = self.dataset.df[columns].corr(numeric_only=True)
        heatmap = go.Heatmap(
            z=corr_matrix.values,
            x=list(corr_matrix.columns),
            y=list(corr_matrix.index),
            colorscale="rdbu",
            zmin=-1,
            zmax=1,
        )

        annotations = []
        for i, row in enumerate(corr_matrix.values):
            for j, value in enumerate(row):
                color = "#ffffff" if abs(value) > 0.7 else "#000000"
                annotations.append(
                    go.layout.Annotation(
                        text=str(round(value, 2)),
                        x=corr_matrix.columns[j],
                        y=corr_matrix.index[i],
                        showarrow=False,
                        font=dict(color=color),
                    )
                )

        layout = go.Layout(
            annotations=annotations,
            xaxis=dict(side="top"),
            yaxis=dict(scaleanchor="x", scaleratio=1),
            width=800,
            height=800,
            autosize=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        fig = go.Figure(data=[heatmap], layout=layout)

        return self.cache_results(
            figures=[
                Figure(
                    for_object=self,
                    key=self.key,
                    figure=fig,
                )
            ]
        )
