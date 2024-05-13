# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.express as px
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_relevancy

from .utils import get_renamed_columns


def ContextRelevancy(
    dataset,
    question_column: str = "question",
    contexts_column: str = "contexts",
):
    """
    Evaluates the context relevancy metric for entries in a dataset and visualizes the results.

    This function processes a dataset containing questions, answers, ground truths, and contexts,
    calculates the context relevancy using a specified metric, and returns a histogram plot of
    the relevancy scores. This provides an insight into how relevant the context provided is
    for the answers in relation to the questions and ground truths.

    Args:
        dataset (Dataset): A dataset object which must have a `df` attribute (a pandas DataFrame)
            that contains the necessary columns.
        question_column (str, optional): The name of the column containing questions. Defaults to "question".
        contexts_column (str, optional): The name of the column containing context information.
            Defaults to "contexts".

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly histogram plot showing the distribution of context relevancy scores.

    Raises:
        KeyError: If any of the required columns are missing in the dataset.
    """
    required_columns = {
        question_column: "question",
        contexts_column: "contexts",
    }

    df = get_renamed_columns(dataset.df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df[list(required_columns.values())]),
        metrics=[context_relevancy],
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["context_relevancy"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["context_relevancy"].to_list())

    return (
        {
            "Scores": result_df[["question", "contexts", "context_relevancy"]],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df["context_relevancy"].mean(),
                    "Median Score": result_df["context_relevancy"].median(),
                    "Max Score": result_df["context_relevancy"].max(),
                    "Min Score": result_df["context_relevancy"].min(),
                    "Standard Deviation": result_df["context_relevancy"].std(),
                    "Count": len(result_df),
                }
            ],
        },
        fig_histogram,
        fig_box,
    )
