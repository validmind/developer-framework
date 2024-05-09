# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import numpy as np
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity


def CosineSimilarityHeatmap(
    dataset,
    model,
    title="Cosine Similarity Matrix",
    color="Cosine Similarity",
    xaxis_title="Index",
    yaxis_title="Index",
    color_scale="Blues",
):
    """
    Plots an interactive heatmap of cosine similarities for embeddings stored in a DataFrame.

    Args:
        dataset (pd.DataFrame): DataFrame containing the embeddings.
        embedding_column (str): Column name where embeddings are stored as lists or arrays.
        title (str): Title of the heatmap.
        xaxis_title (str): Title for the X-axis.
        yaxis_title (str): Title for the Y-axis.
        color_scale (str): Color scale for the heatmap.
        rows_to_use (list[int]): List of indices specifying which rows to use for computation.

    Returns:
        None: Displays an interactive heatmap.
    """
    embeddings = np.stack(dataset.y_pred(model))

    # Calculate pairwise cosine similarity
    similarity_matrix = cosine_similarity(embeddings)

    # Create the heatmap using Plotly
    fig = px.imshow(
        similarity_matrix,
        labels=dict(x=xaxis_title, y=yaxis_title, color=color),
        text_auto=True,
        aspect="auto",
        color_continuous_scale=color_scale,
    )

    fig.update_layout(
        title=f"{title} - {model.input_id}",
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
    )

    return fig
