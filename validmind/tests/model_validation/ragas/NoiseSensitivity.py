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
def NoiseSensitivity(
    dataset,
    answer_column="answer",
    contexts_column="contexts",
    ground_truth_column="ground_truth",
):
    """
    Noise sensitivity measures how often an LLM provides incorrect responses when utilizing relevant retrieved
    contextual information. The score ranges from 0 to 1, with lower values indicating better performance.

    Noise sensitivity is computed using the question, ground truth, answer, and the retrieved context.

    To estimate the sensitivity of a model to the noise in the retrieved documents (i.e. context chunks that
    contain relevant information), then an LLM extracts "claims" from the answer and ground truth that can be
    attributed to information in the relevant retrieved context. If the answer contains claims that are not
    present in the ground truth then that claim is considered incorrect. The final score is calculated using
    the following formula:

    $$
    \\text{noise sensitivity} = {|\\text{Number of incorrect claims in answer}| \\over |\\text{Number of total claims in answer}|}
    $$

    This score can be interpreted as "sensitivity to noise" since it measures how well the llm is able to
    "identify" the information in the context that it should use to generate an answer. This metric is really
    only useful when the ground truth is an answer that was also generated from the same contexts.

    ### Configuring Columns

    This metric requires the following columns in your dataset:

    - `contexts` (List[str]): A list of text contexts which are retrieved to generate
    the answer.
    - `answer` (str): The response generated by the model
    - `ground_truth` (str): The "correct" answer to the question

    If the above data is not in the appropriate column, you can specify different column
    names for these fields using the parameters `contexts_column` and `answer_column`.

    For example, if your dataset has this data stored in different columns, you can
    pass the following parameters:
    ```python
    {
        "contexts_column": "context_info"
        "answer_column": "my_answer_col",
    }
    ```

    If the data is stored as a dictionary in another column, specify the column and key
    like this:
    ```python
    pred_col = dataset.prediction_column(model)
    params = {
        "contexts_column": f"{pred_col}.contexts",
        "answer_column": f"{pred_col}.answer",
    }
    ```

    For more complex situations, you can use a function to extract the data:
    ```python
    pred_col = dataset.prediction_column(model)
    params = {
        "contexts_column": lambda row: [row[pred_col]["context_message"]],
        "answer_column": lambda row: "\\n\\n".join(row[pred_col]["messages"]),
    }
    ```
    """
    try:
        from ragas import evaluate
        from ragas.metrics import noise_sensitivity_relevant
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
        "ground_truth": ground_truth_column,
    }

    df = get_renamed_columns(dataset._df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df),
        metrics=[noise_sensitivity_relevant],
        **get_ragas_config(),
    ).to_pandas()

    fig_histogram = px.histogram(
        x=result_df["noise_sensitivity_relevant"].to_list(), nbins=10
    )
    fig_box = px.box(x=result_df["noise_sensitivity_relevant"].to_list())

    return (
        {
            # "Scores (will not be uploaded to UI)": result_df[
            #     ["contexts", "answer", "ground_truth", "noise_sensitivity_relevant"]
            # ],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df["noise_sensitivity_relevant"].mean(),
                    "Median Score": result_df["noise_sensitivity_relevant"].median(),
                    "Max Score": result_df["noise_sensitivity_relevant"].max(),
                    "Min Score": result_df["noise_sensitivity_relevant"].min(),
                    "Standard Deviation": result_df["noise_sensitivity_relevant"].std(),
                    "Count": result_df.shape[0],
                }
            ],
        },
        fig_histogram,
        fig_box,
    )