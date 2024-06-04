# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial


import plotly.graph_objects as go


def PyMCSeasonalityPlot(dataset, seasonality, title):
    """
    PyMC Seasonality Plot
    """

    fig = go.Figure()

    df = dataset.df.copy()

    for sample in seasonality.T:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=sample,
                mode="lines",
                line=dict(color="blue", width=1),
                opacity=0.05,
            )
        )

    fig.update_layout(
        title=title, xaxis_title="Date", yaxis_title=dataset.target_column
    )

    return fig
