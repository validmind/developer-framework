# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class PearsonCorrelationMatrix(Metric):
    """
    Evaluates linear dependency between numerical variables in a dataset via a Pearson Correlation coefficient heat map.

    **Purpose**: This test is intended to evaluate the extent of linear dependency between all pairs of numerical
    variables in the given dataset. It provides the Pearson Correlation coefficient, which reveals any high
    correlations present. The purpose of doing this is to identify potential redundancy, as variables that are highly
    correlated can often be removed to reduce the dimensionality of the dataset without significantly impacting the
    model's performance.

    **Test Mechanism**: This metric test generates a correlation matrix for all numerical variables in the dataset
    using the Pearson correlation formula. A heat map is subsequently created to visualize this matrix effectively. The
    color of each point on the heat map corresponds to the magnitude and direction (positive or negative) of the
    correlation, with a range from -1 (perfect negative correlation) to 1 (perfect positive correlation). Any
    correlation coefficients higher than 0.7 (in absolute terms) are indicated in white in the heat map, suggesting a
    high degree of correlation.

    **Signs of High Risk**:
    - A large number of variables in the dataset showing a high degree of correlation (coefficients approaching ±1).
    This indicates redundancy within the dataset, suggesting that some variables may not be contributing new
    information to the model.
    - This could potentially lead to overfitting.

    **Strengths**:
    - The primary strength of this metric test is its ability to detect and quantify the linearity of relationships
    between variables. This allows for the identification of redundant variables, which in turn can help in simplifying
    models and potentially improving their performance.
    - The visualization aspect (heatmap) is another strength as it offers an easy-to-understand overview of the
    correlations, beneficial for those not comfortable navigating numerical matrices.

    **Limitations**:
    - The primary limitation of Pearson Correlation is its inability to detect non-linear relationships between
    variables, which can lead to missed opportunities for dimensionality reduction.
    - It only measures the degree of linear relationship and not the strength of effect of one variable on the other.
    - The cutoff value of 0.7 for high correlation is a somewhat arbitrary choice and some valid dependencies might be
    missed if they have a correlation coefficient less than this value.
    """

    name = "pearson_correlation_matrix"
    required_inputs = ["dataset"]
    tasks = ["classification", "regression"]
    tags = ["tabular_data", "numerical_data", "correlation"]

    def run(self):
        columns = self.params.get("columns", list(self.inputs.dataset.df.columns))

        corr_matrix = self.inputs.dataset.df[columns].corr(numeric_only=True)
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
