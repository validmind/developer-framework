# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.express as px
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_similarity

from validmind import tags, tasks

from .utils import get_renamed_columns


@tags("ragas", "llm")
@tasks("text_qa", "text_generation", "text_summarization")
def AnswerSimilarity(
    dataset,
    answer_column="answer",
    ground_truth_column="ground_truth",
):
    """
    Calculates the semantic similarity between generated answers and ground truths

    The concept of Answer Semantic Similarity pertains to the assessment of the semantic
    resemblance between the generated answer and the ground truth. This evaluation is
    based on the `ground_truth` and the `answer`, with values falling within the range
    of 0 to 1. A higher score signifies a better alignment between the generated answer
    and the ground truth.

    Measuring the semantic similarity between answers can offer valuable insights into
    the quality of the generated response. This evaluation utilizes a cross-encoder
    model to calculate the semantic similarity score.

    See this paper for more details: https://arxiv.org/pdf/2108.06130.pdf

    The following steps are involved in computing the answer similarity score:
    1. Vectorize the ground truth answer using the specified embedding model.
    2. Vectorize the generated answer using the same embedding model.
    3. Compute the cosine similarity between the two vectors.
    """
    required_columns = {
        answer_column: "answer",
        ground_truth_column: "ground_truth",
    }

    df = get_renamed_columns(dataset.df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df[list(required_columns.values())]),
        metrics=[answer_similarity],
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["answer_similarity"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["answer_similarity"].to_list())

    return (
        {
            "Scores": result_df[["answer", "ground_truth", "answer_similarity"]],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df["answer_similarity"].mean(),
                    "Median Score": result_df["answer_similarity"].median(),
                    "Max Score": result_df["answer_similarity"].max(),
                    "Min Score": result_df["answer_similarity"].min(),
                    "Standard Deviation": result_df["answer_similarity"].std(),
                    "Count": len(result_df),
                }
            ],
        },
        fig_histogram,
        fig_box,
    )
