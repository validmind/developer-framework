# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from itertools import combinations

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity

from validmind import tags, tasks


@tags("visualization", "dimensionality_reduction", "embeddings")
@tasks("text_qa", "text_generation", "text_summarization")
def CosineSimilarityComparison(dataset, models):
    """
    Computes pairwise cosine similarities between model embeddings and visualizes the results through bar charts,
    alongside compiling a comprehensive table of descriptive statistics for each model pair.

    **Purpose:**
    This function is designed to analyze and compare the embeddings produced by different models using Cosine Similarity.
    Cosine Similarity, a measure calculating the cosine of the angle between two vectors, is widely used to determine
    the alignment or similarity between vectors in high-dimensional spaces, such as text embeddings. This analysis helps
    to understand how similar or different the models' predictions are in terms of embedding generation.

    **Test Mechanism:**
    The function begins by computing the embeddings for each model using the provided dataset. It then calculates the
    cosine similarity for every possible pair of models, generating a similarity matrix. Each element of this matrix
    represents the cosine similarity between two model embeddings. The function flattens this matrix and uses it to
    create a bar chart for each model pair, visualizing their similarity distribution. Additionally, it compiles a table
    with descriptive statistics (mean, median, standard deviation, minimum, and maximum) for the similarities of each
    pair, including a reference to the compared models.

    **Signs of High Risk:**

    - A high concentration of cosine similarity values close to 1 could suggest that the models are producing very
      similar embeddings, which could be a sign of redundancy or lack of diversity in model training or design.
    - Conversely, very low similarity values near -1 indicate strong dissimilarity, potentially highlighting models
      that are too divergent, possibly focusing on very different features of the data.

    **Strengths:**

    - Enables detailed comparisons between multiple models' embedding strategies through visual and statistical means.
    - Helps identify which models produce similar or dissimilar embeddings, useful for tasks requiring model diversity.
    - Provides quantitative and visual feedback on the degree of similarity, enhancing interpretability of model
      behavior in embedding spaces.

    **Limitations:**

    - The analysis is confined to the comparison of embeddings and does not assess the overall performance of the models
      in terms of their primary tasks (e.g., classification, regression).
    - Assumes that the models are suitable for generating comparable embeddings, which might not always be the case,
      especially across different types of models.
    - Interpretation of results is heavily dependent on the understanding of Cosine Similarity and the nature of high-dimensional
      embedding spaces.
    """

    figures = []
    # Initialize a list to store data for the DataFrame
    all_stats = []

    # Generate all pairs of models for comparison
    for model_A, model_B in combinations(models, 2):
        embeddings_A = np.stack(dataset.y_pred(model_A))
        embeddings_B = np.stack(dataset.y_pred(model_B))

        # Calculate pairwise cosine similarity
        similarity_matrix = cosine_similarity(embeddings_A, embeddings_B)
        similarities = similarity_matrix.flatten()

        # Generate statistics and add model combination as a column
        stats_data = {
            "Combination": f"{model_A.input_id} vs {model_B.input_id}",
            "Mean": np.mean(similarities),
            "Median": np.median(similarities),
            "Standard Deviation": np.std(similarities),
            "Minimum": np.min(similarities),
            "Maximum": np.max(similarities),
        }
        all_stats.append(stats_data)

        # Generate an index for each similarity value
        indices = range(len(similarities))

        # Create the bar chart using Plotly
        fig = px.bar(
            x=indices,
            y=similarities,
            labels={"x": "Pair Index", "y": "Cosine Similarity"},
            title=f"Cosine Similarity - {model_A.input_id} vs {model_B.input_id}",
        )
        fig.update_layout(xaxis_title="Pair Index", yaxis_title="Cosine Similarity")
        figures.append(fig)

    # Create a DataFrame from all collected statistics
    stats_df = pd.DataFrame(all_stats)

    return (stats_df, *tuple(figures))
