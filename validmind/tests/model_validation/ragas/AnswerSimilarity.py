# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.express as px
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_similarity

from validmind import tags, tasks


@tags("nlp", "text_data", "visualization")
@tasks("text_classification", "text_summarization")
def AnswerSimilarity(
    dataset,
    question_column="question",
    answer_column="answer",
    ground_truth_column="ground_truth",
    contexts_column="contexts",
):
    """
    Calculates the answer similarity metric for dataset entries based on a provided ground truth.

    This function takes a dataset containing columns for questions, answers, the correct answers
    (ground truth), and context information. It evaluates answer similarity using a specified
    metric, mapping columns as needed and returns a list of similarity scores.

    Args:
        dataset (Dataset): A dataset object which must have a `df` attribute (a pandas DataFrame)
            that contains the necessary columns.
        question_column (str, optional): The name of the column containing questions. Defaults to "question".
        answer_column (str, optional): The name of the column containing answers. Defaults to "answer".
        ground_truth_column (str, optional): The name of the column containing the correct answers.
            Defaults to "ground_truth".
        contexts_column (str, optional): The name of the column containing context information.
            Defaults to "contexts".

    Returns:
        list: A list of answer similarity scores for each entry in the dataset.

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
        metrics=[answer_similarity],
    )

    fig = px.histogram(x=result.to_pandas()["answer_similarity"].to_list(), nbins=10)

    return fig
