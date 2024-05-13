# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.express as px
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_relevancy

from validmind import tags, tasks

from .utils import get_renamed_columns


@tags("ragas", "llm", "rag_performance")
@tasks("text_qa", "text_generation", "text_summarization")
def AnswerRelevance(
    dataset,
    question_column="question",
    answer_column="answer",
    contexts_column="contexts",
):
    """
    Assesses how pertinent the generated answer is to the given prompt.

    The evaluation metric, Answer Relevancy, focuses on assessing how pertinent the
    generated answer is to the given prompt. A lower score is assigned to answers that
    are incomplete or contain redundant information and higher scores indicate better
    relevancy. This metric is computed using the `question`, the `contexts` and the
    `answer`.

    The Answer Relevancy is defined as the mean cosine similartiy of the original
    `question` to a number of artifical questions, which are generated (reverse-engineered)
    based on the `answer`:

    $$
    \\text{answer relevancy} = \\frac{1}{N} \sum_{i=1}^{N} cos(E_{g_i}, E_o)
    $$
    $$
    \\text{answer relevancy} = \\frac{1}{N} \sum_{i=1}^{N} \\frac{E_{g_i} \cdot E_o}{\|E_{g_i}\|\|E_o\|}
    $$

    Where:
    - $E_{g_i}$ is the embedding of the generated question $i$.
    - $E_o$ is the embedding of the original question.
    - $N$ is the number of generated questions - 3 by default.

    **Note**: *This is a reference-free metric, meaning that it does not require a
    `ground_truth` answer to compare against. A similar metric that does evaluate the
    correctness of a generated answser with respect to a `ground_truth` answer is
    `validmind.model_validation.ragas.AnswerCorrectness`.*
    """
    required_columns = {
        question_column: "question",
        answer_column: "answer",
        contexts_column: "contexts",
    }

    df = get_renamed_columns(dataset.df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df[list(required_columns.values())]),
        metrics=[answer_relevancy],
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["answer_relevancy"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["answer_relevancy"].to_list())

    return (
        {
            "Scores": result_df[["question", "contexts", "answer", "answer_relevancy"]],
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
