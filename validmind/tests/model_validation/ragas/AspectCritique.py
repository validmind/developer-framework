# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from datasets import Dataset
from ragas import evaluate
from ragas.metrics.critique import (
    coherence,
    conciseness,
    correctness,
    harmfulness,
    maliciousness,
)

from validmind import tags, tasks


@tags("nlp", "text_data", "visualization")
@tasks("text_classification", "text_summarization")
def AspectCritique(
    dataset,
    question_column="question",
    answer_column="answer",
    ground_truth_column="ground_truth",
    contexts_column="contexts",
):
    """
    Evaluates the harmfulness of answers in a dataset and visualizes the results in a histogram.

    This function assesses the potential harmfulness of answers by comparing them to the provided ground truths
    within the context of the given questions and contexts. It utilizes a harmfulness metric to measure these
    assessments and generates a histogram plot of the harmfulness scores.

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
        plotly.graph_objs._figure.Figure: A Plotly histogram plot showing the distribution of harmfulness scores
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
        metrics=[
            harmfulness,
            maliciousness,
            coherence,
            correctness,
            conciseness,
        ],
    ).to_pandas()

    score_columns = [
        "harmfulness",
        "maliciousness",
        "coherence",
        "correctness",
        "conciseness",
    ]

    # fig_histogram = px.histogram(x=result_df["harmfulness"].to_list(), nbins=10)

    return (
        {
            "Scores": result_df[
                ["question", "contexts", "answer", "ground_truth", *score_columns]
            ],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df[column].mean(),
                    "Median Score": result_df[column].median(),
                    "Max Score": result_df[column].max(),
                    "Min Score": result_df[column].min(),
                    "Standard Deviation": result_df[column].std(),
                    "Count": len(result_df),
                }
                for column in score_columns
            ],
        },
        # fig_histogram,
        # fig_box,
    )
