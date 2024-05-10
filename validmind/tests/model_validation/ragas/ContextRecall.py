# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.express as px
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_recall


def ContextRecall(
    dataset,
    question_column="question",
    answer_column="answer",
    ground_truth_column="ground_truth",
    contexts_column="contexts",
):
    """
    Evaluates the context recall metric for dataset entries and visualizes the results in a histogram.

    This function processes a dataset containing questions, answers, ground truths, and contexts,
    calculating the context recall using a specified metric. Context recall assesses how well the
    context provided supports the answers in relation to the questions and ground truths. The function
    returns a histogram plot of these recall scores.

    Args:
        dataset (Dataset): A dataset object which must have a `df` attribute (a pandas DataFrame)
            that contains the necessary columns.
        question_column (str, optional): The name of the column containing questions. Defaults to "question".
        answer_column (str, optional): The name of the column containing answers. Defaults to "answer".
        ground_truth_column (str, optional): The name of the column containing the correct answers
            or reference text. Defaults to "ground_truth".
        contexts_column (str, optional): The name of the column containing the contexts related to each
            question and answer pair. Defaults to "contexts".

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly histogram plot showing the distribution of context recall scores
        across the dataset's entries.

    Raises:
        KeyError: If any of the required columns are missing in the dataset.
    """
    required_columns = {
        question_column: "question",
        answer_column: "answer",
        ground_truth_column: "ground_truth",
        contexts_column: "contexts",
    }
    df = dataset.df.rename(columns=required_columns, inplace=False)
    result = evaluate(
        Dataset.from_pandas(df[list(required_columns.values())]),
        metrics=[context_recall],
    )

    fig = px.histogram(
        x=result.to_pandas()["context_recall"].to_list(), nbins=10
    )

    return fig
