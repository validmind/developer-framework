# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import warnings

import plotly.express as px
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_correctness

from validmind import tags, tasks

from .utils import get_renamed_columns


@tags("ragas", "llm")
@tasks("text_qa", "text_generation", "text_summarization")
def AnswerCorrectness(
    dataset,
    question_column="question",
    answer_column="answer",
    ground_truth_column="ground_truth",
):
    """
    Evaluates the correctness of answers in a dataset with respect to the provided ground
    truths and visualizes the results in a histogram.

    The assessment of Answer Correctness involves gauging the accuracy of the generated
    answer when compared to the ground truth. This evaluation relies on the `ground truth`
    and the `answer`, with scores ranging from 0 to 1. A higher score indicates a closer
    alignment between the generated answer and the ground truth, signifying better
    correctness.

    Answer correctness encompasses two critical aspects: semantic similarity between the
    generated answer and the ground truth, as well as factual similarity. These aspects
    are combined using a weighted scheme to formulate the answer correctness score. Users
    also have the option to employ a `threshold` value to round the resulting score to
    a binary value (0 or 1) based on the threshold.

    Factual correctness quantifies the factual overlap between the generated answer and
    the ground truth answer. This is done using the concepts of:

    - TP (True Positive): Facts or statements that are present in both the ground truth
      and the generated answer.
    - FP (False Positive): Facts or statements that are present in the generated answer
      but not in the ground truth.
    - FN (False Negative): Facts or statements that are present in the ground truth but
      not in the generated answer.

    ### Configuring Columns

    This metric requires specific columns to be present in the dataset:
    - `question` (str): The text prompt or query that was input into the model.
    - `answer` (str): The text response generated by the model.
    - `ground_truth` (str): The ground truth answer that the generated answer is compared
    against.

    If the above data is not in the appropriate column, you can specify different column
    names for these fields using the parameters `question_column`, `answer_column`, and
    `ground_truth_column`.

    For example, if your dataset has this data stored in different columns, you can
    pass the following parameters:
    ```python
    params = {
        "question_column": "input_text",
        "answer_column": "output_text",
        "ground_truth_column": "human_answer",
    }
    ```

    If answer and contexts are stored as a dictionary in another column, specify the
    column and key like this:
    ```python
    pred_col = dataset.prediction_column(model)
    params = {
        "answer_column": f"{pred_col}.generated_answer",
        "ground_truth_column": f"{pred_col}.contexts",
    }
    ```

    For more complex data structures, you can use a function to extract the answers:
    ```python
    pred_col = dataset.prediction_column(model)
    params = {
        "answer_column": lambda row: "\\n\\n".join(row[pred_col]["messages"]),
        "ground_truth_column": lambda row: [row[pred_col]["context_message"]],
    }
    ```
    """
    warnings.filterwarnings(
        "ignore",
        category=FutureWarning,
        message="promote has been superseded by promote_options='default'.",
    )

    required_columns = {
        "question": question_column,
        "answer": answer_column,
        "ground_truth": ground_truth_column,
    }

    df = get_renamed_columns(dataset.df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df), metrics=[answer_correctness]
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["answer_correctness"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["answer_correctness"].to_list())

    return (
        {
            "Scores": result_df[
                ["question", "answer", "ground_truth", "answer_correctness"]
            ],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df["answer_correctness"].mean(),
                    "Median Score": result_df["answer_correctness"].median(),
                    "Max Score": result_df["answer_correctness"].max(),
                    "Min Score": result_df["answer_correctness"].min(),
                    "Standard Deviation": result_df["answer_correctness"].std(),
                    "Count": len(result_df),
                }
            ],
        },
        fig_histogram,
        fig_box,
    )