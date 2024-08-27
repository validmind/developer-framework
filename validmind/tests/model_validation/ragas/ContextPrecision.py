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
def ContextPrecision(
    dataset,
    question_column: str = "question",
    contexts_column: str = "contexts",
    ground_truth_column: str = "ground_truth",
):  # noqa: B950
    """
    Assesses the precision of retrieved contexts in containing relevant information in response to a query input.

    ### Purpose

    The Context Precision test aims to evaluate the accuracy with which relevant information is ranked within retrieved
    text contexts in relation to a given query. By comparing the retrieved contexts against the ground truth, this test
    provides a precision score that reflects the relevance and correct ordering of the contexts, with higher scores
    indicating better precision.

    ### Test Mechanism

    This test calculates the Context Precision by:
    - Using the `question`, `ground_truth`, and `contexts` columns from the provided dataset.
    - Applying the following metric formula:

      $$
      \\text{Context Precision@K} = \\frac{\\sum_{k=1}^{K} \\left( \\text{Precision@k} \\times v_k
    \\right)}{\\text{Total number of relevant items in the top } K \\text{ results}}
      $$
      
      $$
      \\text{Precision@k} = {\\text{true positives@k} \\over  (\\text{true positives@k} + \\text{false positives@k})}
      $$
      
      Where \( K \) is the total number of chunks in contexts and \( v_k \\in \\{0, 1\\} \) is the relevance indicator
    at rank \( k \).

    - Renaming columns as specified in the parameters, if default names are not used.
    - Calculating the precision score for each query-context-ground truth triplet.
    - Generating visualizations including a histogram and a box plot of the precision scores.

    ### Signs of High Risk

    - Low mean and median precision scores across contexts.
    - High standard deviation in precision scores, indicating inconsistency.
    - Scores significantly lower than expected thresholds for the domain or use case.

    ### Strengths

    - Provides a quantitative measure of how well the retrieved contexts match the ground truth.
    - Offers a clear perspective on the ranking quality of retrieved information.
    - Visualization aids in quickly identifying performance distribution and outliers.

    ### Limitations

    - Relies on the completeness and accuracy of the ground truth data.
    - May not capture nuances where partial relevance is significant.
    - Assumes that contexts can be clearly distinguished as relevant or irrelevant without gray areas.
    """
    try:
        from ragas import evaluate
        from ragas.metrics import context_precision
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
        Dataset.from_pandas(df), metrics=[context_precision], **get_ragas_config()
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["context_precision"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["context_precision"].to_list())

    return (
        {
            "Scores (will not be uploaded to UI)": result_df[
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
