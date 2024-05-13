# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.express as px
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_entity_recall

from .utils import get_renamed_columns


def ContextEntityRecall(
    dataset,
    contexts_column: str = "contexts",
    ground_truth_column: str = "ground_truth",
):
    """
    Evaluates the context entity recall metric for dataset entries and visualizes the results.

    This function processes a dataset containing questions, answers, ground truths, and contexts,
    calculates the context entity recall using a specified metric, and returns a histogram plot of
    the recall scores.

    Args:
        dataset (Dataset): A dataset object which must have a `df` attribute (a pandas DataFrame)
            that contains the necessary columns.
        contexts_column (str, optional): The name of the column containing context information.
            Defaults to "contexts".
        ground_truth_column (str, optional): The name of the column containing the correct answers.
            Defaults to "ground_truth".

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly histogram plot showing the distribution of context entity recall scores.

    Raises:
        KeyError: If any of the required columns are missing in the dataset.
    """
    required_columns = {
        ground_truth_column: "ground_truth",
        contexts_column: "contexts",
    }

    df = get_renamed_columns(dataset.df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df[list(required_columns.values())]),
        metrics=[context_entity_recall],
    ).to_pandas()

    fig_histogram = px.histogram(
        x=result_df["context_entity_recall"].to_list(), nbins=10
    )
    fig_box = px.box(x=result_df["context_entity_recall"].to_list())

    return (
        {
            "Scores": result_df[
                [
                    "contexts",
                    "ground_truth",
                    "context_entity_recall",
                ]
            ],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df["context_entity_recall"].mean(),
                    "Median Score": result_df["context_entity_recall"].median(),
                    "Max Score": result_df["context_entity_recall"].max(),
                    "Min Score": result_df["context_entity_recall"].min(),
                    "Standard Deviation": result_df["context_entity_recall"].std(),
                    "Count": len(result_df),
                }
            ],
        },
        fig_histogram,
        fig_box,
    )
