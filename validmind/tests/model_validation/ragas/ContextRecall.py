# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import warnings

import plotly.express as px
from datasets import Dataset

from validmind import tags, tasks

from .utils import get_ragas_config, get_renamed_columns


@tags("ragas", "llm", "retrieval_performance")
@tasks("text_qa", "text_generation", "text_summarization", "text_classification")
def ContextRecall(
    dataset,
    question_column: str = "question",
    contexts_column: str = "contexts",
    ground_truth_column: str = "ground_truth",
):
    """
    Assesses the alignment of retrieved contexts with the ground truth in text-based retrieval tasks.

    ### Purpose

    The Context Recall test evaluates how well the retrieved context aligns with the annotated ground truth in
    text-based retrieval tasks. It quantifies the proportion of sentences in the ground truth that can be attributed to
    the retrieved context, providing insights into the model's retrieval performance.

    ### Test Mechanism

    This test involves calculating the context recall using the following steps:

    - Identify sentences in the ground truth answer.
    - Check if each sentence can be attributed to the retrieved context.
    - Calculate the context recall as the ratio of ground truth sentences attributable to the context to the total
    number of sentences in the ground truth.
    - Produce a histogram and box plot of the context recall values.

    The formula for context recall is:
    $$
    \\text{context recall} = {|\\text{GT sentences that can be attributed to context}| \\over |\\text{Number of
    sentences in GT}|}
    $$

    ### Signs of High Risk

    - Low mean or median context recall score, indicating poor alignment.
    - High standard deviation in scores, suggesting inconsistent retrieval performance.
    - Frequent occurrences of minimum context recall scores close to zero.

    ### Strengths

    - Provides a quantitative measure of retrieval accuracy.
    - Easy to interpret with meaningful scores ranging from 0 to 1.
    - Visual aids (histogram and box plot) help in understanding the distribution of scores.

    ### Limitations

    - Depends heavily on the quality of the annotated ground truth.
    - Specific to text-based tasks, not applicable to other types of retrieval tasks.
    - May not fully capture the semantic relevance of retrieved contexts beyond sentence attribution.
    """
    try:
        from ragas import evaluate
        from ragas.metrics import context_recall
    except ImportError:
        raise ImportError("Please run `pip install validmind[llm]` to use LLM tests")

    warnings.filterwarnings(
        "ignore",
        category=FutureWarning,
        message="promote has been superseded by promote_options='default'.",
    )

    required_columns = {
        "question": question_column,
        "contexts": contexts_column,
        "ground_truth": ground_truth_column,
    }

    df = get_renamed_columns(dataset._df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df), metrics=[context_recall], **get_ragas_config()
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["context_recall"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["context_recall"].to_list())

    return (
        {
            "Scores (will not be uploaded to UI)": result_df[
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
