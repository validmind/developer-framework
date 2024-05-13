# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.express as px
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness

from validmind import tags, tasks


@tags("nlp", "text_data", "visualization")
@tasks("rag", "text_summarization")
def Faithfulness(
    dataset,
    question_column="question",
    answer_column="answer",
    ground_truth_column="ground_truth",
    contexts_column="contexts",
):
    """
    Evaluates the faithfulness metric for generated answers in a dataset and visualizes the results.

    This function analyzes how faithful the generated answers are to the provided contexts in a dataset.
    It processes a dataset containing questions, answers, ground truths, and contexts, calculates
    the faithfulness of each answer with respect to its context and ground truth, and returns a histogram
    plot of these faithfulness scores.

    Args:
        dataset (Dataset): A dataset object which must have a `df` attribute (a pandas DataFrame)
            that contains the necessary columns.
        question_column (str, optional): The name of the column containing questions. Defaults to "question".
        answer_column (str, optional): The name of the column containing generated answers. Defaults to "answer".
        ground_truth_column (str, optional): The name of the column containing the correct answers
            or reference text. Defaults to "ground_truth".
        contexts_column (str, optional): The name of the column containing the contexts related to each question
            and answer pair. Defaults to "contexts".

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly histogram plot showing the distribution of faithfulness scores
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
    df = dataset.df.copy()
    df.rename(columns=required_columns, inplace=False)

    result_df = evaluate(
        Dataset.from_pandas(df[list(required_columns.values())]),
        metrics=[faithfulness],
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["faithfulness"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["faithfulness"].to_list())

    return (
        {
            "Scores": result_df[
                ["question", "contexts", "answer", "ground_truth", "faithfulness"]
            ],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df["faithfulness"].mean(),
                    "Median Score": result_df["faithfulness"].median(),
                    "Max Score": result_df["faithfulness"].max(),
                    "Min Score": result_df["faithfulness"].min(),
                    "Standard Deviation": result_df["faithfulness"].std(),
                    "Count": len(result_df),
                }
            ],
        },
        fig_histogram,
        fig_box,
    )
