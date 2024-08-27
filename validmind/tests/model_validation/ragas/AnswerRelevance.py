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
def AnswerRelevance(
    dataset,
    question_column="question",
    contexts_column="contexts",
    answer_column="answer",
):
    """
    Assesses how pertinent the generated answer is to the given prompt.

    ### Purpose

    The Answer Relevance test aims to evaluate the pertinence of the generated answers from a language model in
    relation to the given prompts. By quantifying how closely the answers align with the original questions, it helps
    identify whether the model produces meaningful and contextually appropriate responses.

    ### Test Mechanism

    This test calculates Answer Relevancy using the mean cosine similarity between the original question and a set of
    artificially generated questions derived from the answer. The methodology involves:

    - Generating artificial questions based on the provided answer.
    - Computing the embeddings for both the original question and each generated question.
    - Calculating the cosine similarity between these embeddings.
    - Averaging the cosine similarity scores to produce the final Answer Relevancy score.

    ### Signs of High Risk

    - Low mean cosine similarity scores for answer relevancy.
    - Large standard deviation in the relevancy scores, implying inconsistency.
    - Significant number of answers with very low relevancy scores.
    - High median score deviation from the mean score.

    ### Strengths

    - Provides a quantitative measure of answer pertinence to the query.
    - No need for ground-truth answers, making it versatile across different datasets.
    - Highlights both the average performance and variability in the model’s responses.

    ### Limitations

    - Does not evaluate the correctness of the answer, only its relevance.
    - Artificially generated questions might not always represent meaningful transformations.
    - Cosine similarity might not capture nuanced semantic differences in some contexts.
    """
    try:
        from ragas import evaluate
        from ragas.metrics import answer_relevancy
    except ImportError:
        raise ImportError("Please run `pip install validmind[llm]` to use LLM tests")

    warnings.filterwarnings(
        "ignore",
        category=FutureWarning,
        message="promote has been superseded by promote_options='default'.",
    )

    required_columns = {
        "question": question_column,
        "answer": answer_column,
        "contexts": contexts_column,
    }

    df = get_renamed_columns(dataset._df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df), metrics=[answer_relevancy], **get_ragas_config()
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["answer_relevancy"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["answer_relevancy"].to_list())

    return (
        {
            "Scores (will not be uploaded to UI)": result_df[
                ["question", "contexts", "answer", "answer_relevancy"]
            ],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df["answer_relevancy"].mean(),
                    "Median Score": result_df["answer_relevancy"].median(),
                    "Max Score": result_df["answer_relevancy"].max(),
                    "Min Score": result_df["answer_relevancy"].min(),
                    "Standard Deviation": result_df["answer_relevancy"].std(),
                    "Count": len(result_df),
                }
            ],
        },
        fig_histogram,
        fig_box,
    )
