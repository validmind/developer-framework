# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.express as px
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_precision

from validmind import tags, tasks

from .utils import get_renamed_columns


@tags("ragas", "llm", "retrieval_performance")
@tasks("text_qa", "text_generation", "text_summarization", "text_classification")
def ContextPrecision(
    dataset,
    question_column: str = "question",
    contexts_column: str = "contexts",
    ground_truth_column: str = "ground_truth",
):
    """
    Context Precision is a metric that evaluates whether all of the ground-truth
    relevant items present in the contexts are ranked higher or not. Ideally all the
    relevant chunks must appear at the top ranks. This metric is computed using the
    `question`, `ground_truth` and the `contexts`, with values ranging between 0 and 1,
    where higher scores indicate better precision.

    $$
    \\text{Context Precision@K} = \\frac{\sum_{k=1}^{K} \left( \\text{Precision@k} \\times v_k \\right)}{\\text{Total number of relevant items in the top } K \\text{ results}}
    $$
    $$
    \\text{Precision@k} = {\\text{true positives@k} \over  (\\text{true positives@k} + \\text{false positives@k})}
    $$

    Where $K$ is the total number of chunks in contexts and $v_k \in \{0, 1\}$ is the
    relevance indicator at rank $k$.
    """
    required_columns = {
        question_column: "question",
        contexts_column: "contexts",
        ground_truth_column: "ground_truth",
    }

    df = get_renamed_columns(dataset.df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df[list(required_columns.values())]),
        metrics=[context_precision],
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["context_precision"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["context_precision"].to_list())

    return (
        {
            "Scores": result_df[
                ["question", "contexts", "ground_truth", "context_precision"]
            ],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df["context_precision"].mean(),
                    "Median Score": result_df["context_precision"].median(),
                    "Max Score": result_df["context_precision"].max(),
                    "Min Score": result_df["context_precision"].min(),
                    "Standard Deviation": result_df["context_precision"].std(),
                    "Count": len(result_df),
                }
            ],
        },
        fig_histogram,
        fig_box,
    )
