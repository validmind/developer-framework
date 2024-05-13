# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.express as px
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_recall

from validmind import tags, tasks

from .utils import get_renamed_columns


@tags("ragas", "llm", "retrieval_performance")
@tasks("text_qa", "text_generation", "text_summarization", "text_classification")
def ContextRecall(
    dataset,
    question_column: str = "question",
    contexts_column: str = "contexts",
    ground_truth_column: str = "ground_truth",
):
    """
    Context recall measures the extent to which the retrieved context aligns with the
    annotated answer, treated as the ground truth. It is computed based on the `ground
    truth` and the `retrieved context`, and the values range between 0 and 1, with higher
    values indicating better performance.

    To estimate context recall from the ground truth answer, each sentence in the ground
    truth answer is analyzed to determine whether it can be attributed to the retrieved
    context or not. In an ideal scenario, all sentences in the ground truth answer
    should be attributable to the retrieved context.


    The formula for calculating context recall is as follows:
    $$
    \\text{context recall} = {|\\text{GT sentences that can be attributed to context}| \over |\\text{Number of sentences in GT}|}
    $$
    """
    required_columns = {
        question_column: "question",
        contexts_column: "contexts",
        ground_truth_column: "ground_truth",
    }

    df = get_renamed_columns(dataset.df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df[list(required_columns.values())]),
        metrics=[context_recall],
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["context_recall"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["context_recall"].to_list())

    return (
        {
            "Scores": result_df[
                ["question", "contexts", "ground_truth", "context_recall"]
            ],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df["context_recall"].mean(),
                    "Median Score": result_df["context_recall"].median(),
                    "Max Score": result_df["context_recall"].max(),
                    "Min Score": result_df["context_recall"].min(),
                    "Standard Deviation": result_df["context_recall"].std(),
                    "Count": len(result_df),
                }
            ],
        },
        fig_histogram,
        fig_box,
    )
