# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import warnings

import plotly.express as px
from datasets import Dataset

from validmind import tags, tasks

from .utils import get_ragas_config, get_renamed_columns


@tags("ragas", "llm", "retrieval_performance")
@tasks("text_qa", "text_generation", "text_summarization")
def ContextEntityRecall(
    dataset,
    contexts_column: str = "contexts",
    ground_truth_column: str = "ground_truth",
):
    """
    Assesses the recall of entities from the context provided in relation to ground truth data to measure retrieval
    performance.

    ### Purpose

    The Context Entity Recall test aims to evaluate the effectiveness of context retrieval in recalling entities from
    ground truth data. This metric is particularly valuable in fact-based applications such as tourism help desks and
    historical question answering (QA), where accurately recalling entities from contexts is critical. By comparing
    entities in the contexts against those in the ground truth, this test provides a measure of the retrieval
    mechanism's success.

    ### Test Mechanism

    This test calculates the Context Entity Recall by:

    - Identifying two sets: GE (entities in ground truth) and CE (entities in context).
    - Computing the intersection of these sets.
    - Dividing the size of the intersection by the size of the GE set, according to the formula:
      \[
      \text{context entity recall} = \frac{|CE \cap GE|}{|GE|}
      \]
    - Generating a histogram and box plot to visualize context entity recall scores across the dataset.

    ### Signs of High Risk

    - Low context entity recall scores across most data points.
    - High variance in context entity recall scores, indicating inconsistency in retrieval.
    - Mean or median context entity recall scores significantly below expected thresholds for the application.

    ### Strengths

    - Provides a quantitative measure of retrieval performance.
    - Useful for evaluating fact-based retrieval mechanisms.
    - Helps in visually assessing the distribution and variability of recall scores.

    ### Limitations

    - Dependent on the accuracy of entity extraction from both contexts and ground truth.
    - May not capture context relevance beyond entity recall.
    - Assumes that entities are defined and extracted consistently across both contexts and ground truth.
    """
    try:
        from ragas import evaluate
        from ragas.metrics import context_entity_recall
    except ImportError:
        raise ImportError("Please run `pip install validmind[llm]` to use LLM tests")

    warnings.filterwarnings(
        "ignore",
        category=FutureWarning,
        message="promote has been superseded by promote_options='default'.",
    )

    required_columns = {
        "ground_truth": ground_truth_column,
        "contexts": contexts_column,
    }

    df = get_renamed_columns(dataset._df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df), metrics=[context_entity_recall], **get_ragas_config()
    ).to_pandas()

    fig_histogram = px.histogram(
        x=result_df["context_entity_recall"].to_list(), nbins=10
    )
    fig_box = px.box(x=result_df["context_entity_recall"].to_list())

    return (
        {
            "Scores (will not be uploaded to UI)": result_df[
                [
                    "contexts",
                    "ground_truth",
                    "context_entity_recall",
                ]
            ],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df["context_entity_recall"].mean(),
                    "Median Score": result_df["context_entity_recall"].median(),
                    "Max Score": result_df["context_entity_recall"].max(),
                    "Min Score": result_df["context_entity_recall"].min(),
                    "Standard Deviation": result_df["context_entity_recall"].std(),
                    "Count": len(result_df),
                }
            ],
        },
        fig_histogram,
        fig_box,
    )
