# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.express as px
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_correctness

from validmind import tags, tasks


@tags("nlp", "text_data", "visualization")
@tasks("text_classification", "text_summarization")
def AnswerCorrectness(
    dataset,
    question_column="question",
    answer_column="answer",
    ground_truth_column="ground_truth",
    contexts_column="contexts",
):
    """
    Evaluates the correctness of answers in a dataset with respect to the provided ground truths and
    visualizes the results in a histogram.

    This function calculates the correctness of answers by comparing them to the ground truth references
    within the context of the given questions and contexts. It utilizes a pre-defined correctness metric
    to assess these comparisons and generates a histogram plot of the correctness scores.

    Args:
        dataset (Dataset): A dataset object which must have a `df` attribute (a pandas DataFrame)
            containing the necessary columns.
        question_column (str, optional): The name of the column containing questions. Defaults to "question".
        answer_column (str, optional): The name of the column containing answers. Defaults to "answer".
        ground_truth_column (str, optional): The name of the column containing the correct answers
            or reference text. Defaults to "ground_truth".
        contexts_column (str, optional): The name of the column containing the contexts related to each
            question and answer pair. Defaults to "contexts".

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly histogram plot showing the distribution of answer correctness
        scores across the dataset's entries.

    Raises:
        KeyError: If any of the required columns are missing in the dataset.
    """
    required_columns = {
        question_column: "question",
        answer_column: "answer",
        ground_truth_column: "ground_truth",
        contexts_column: "contexts",
    }
    df = dataset.df.copy()
    df.rename(columns=required_columns, inplace=False)

    result_df = evaluate(
        Dataset.from_pandas(df[list(required_columns.values())]),
        metrics=[answer_correctness],
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["answer_correctness"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["answer_correctness"].to_list())

    return (
        {
            "Scores": result_df[
                ["question", "contexts", "answer", "ground_truth", "answer_correctness"]
            ],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df["answer_correctness"].mean(),
                    "Median Score": result_df["answer_correctness"].median(),
                    "Max Score": result_df["answer_correctness"].max(),
                    "Min Score": result_df["answer_correctness"].min(),
                    "Standard Deviation": result_df["answer_correctness"].std(),
                    "Count": len(result_df),
                }
            ],
        },
        fig_histogram,
        fig_box,
    )
