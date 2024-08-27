# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import warnings

import plotly.express as px
from datasets import Dataset

from validmind import tags, tasks

from .utils import get_ragas_config, get_renamed_columns


@tags("ragas", "llm", "rag_performance")
@tasks("text_qa", "text_generation", "text_summarization")
def Faithfulness(
    dataset,
    answer_column="answer",
    contexts_column="contexts",
):  # noqa
    """
    Evaluates the faithfulness of the generated answers with respect to retrieved contexts.

    ### Purpose

    The Faithfulness test aims to evaluate the factual consistency and reliability of generated answers from a language
    model in relation to the retrieved contexts. This test is essential for ensuring that the model's responses are
    accurate and grounded in the provided information, minimizing the risk of misinformation.

    ### Test Mechanism

    This test uses a judge LLM to measure the factual consistency of the generated answer against the given context(s).
    The process entails:

    - Identifying individual claims within the generated answer.
    - Cross-checking each claim with the retrieved contexts to verify inferability.
    - Calculating the faithfulness score as the ratio of the number of claims that can be inferred from the given
    context to the total number of claims in the generated answer. The score ranges from 0 to 1, with higher scores
    indicating greater faithfulness.

    ### Signs of High Risk

    - Low faithfulness scores (close to 0), indicating a significant portion of claims are not supported by the
    contexts.
    - High variability in faithfulness scores across different samples.
    - Consistent failure to achieve acceptable faithfulness scores over time.

    ### Strengths

    - Provides a quantitative measure of the reliability of generated answers.
    - Helps in identifying specific areas where the model may be producing inaccurate or unsupported information.
    - Easy to interpret and provides clear metrics for decision-making.

    ### Limitations

    - Relies on the accuracy and completeness of the provided contexts for evaluation.
    - May not fully capture nuanced or indirect inferences from the context.
    - The judge LLM's own limitations could affect the accuracy of the faithfulness assessment.
    """
    try:
        from ragas import evaluate
        from ragas.metrics import faithfulness
    except ImportError:
        raise ImportError("Please run `pip install validmind[llm]` to use LLM tests")

    warnings.filterwarnings(
        "ignore",
        category=FutureWarning,
        message="promote has been superseded by promote_options='default'.",
    )

    required_columns = {
        "answer": answer_column,
        "contexts": contexts_column,
    }

    df = get_renamed_columns(dataset._df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df), metrics=[faithfulness], **get_ragas_config()
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["faithfulness"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["faithfulness"].to_list())

    return (
        {
            "Scores (will not be uploaded to UI)": result_df[
                ["contexts", "answer", "faithfulness"]
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
