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
def ContextUtilization(
    dataset,
    question_column: str = "question",
    contexts_column: str = "contexts",
    answer_column: str = "answer",
):  # noqa: B950
    """
    Context Precision is a reference(ground-truth)-free version of `validmind.model_validation.ragas.ContextPrecision.
    It evaluates whether all of the answer-relevant items present in the `contexts` are ranked higher or not. Ideally,
    all the relevant chunks of context should appear at the top ranks. This metric is computed using the `question`,
    `answer` and the `contexts` columns, with values ranging between 0 and 1, where higher scores are better.

    $$
    \\text{Context Utilization@K} = \\frac{\\sum_{k=1}^{K} \\left( \\text{Precision@k} \\times v_k \\right)}{\\text{Total number of relevant items in the top } K \\text{ results}}
    $$
    $$
    \\text{Precision@k} = {\\text{true positives@k} \\over  (\\text{true positives@k} + \\text{false positives@k})}
    $$

    Where $K$ is the total number of chunks in `contexts` and $v_k \\in \\{0, 1\\}$ is the relevance indicator at rank $k$.

    ### Configuring Columns

    This metric requires the following columns in your dataset:

    - `question` (str): The text query that was input into the model.
    - `contexts` (List[str]): A list of text contexts which are retrieved and which will be evaluated to
       make sure they contain relevant info in the correct order.
    - `answer` (str): The llm-generated response for the input `question`.

    If the above data is not in the appropriate column, you can specify different column
    names for these fields using the parameters `question_column`, `contexts_column`
    and `ground_truth_column`.

    For example, if your dataset has this data stored in different columns, you can
    pass the following parameters:
    ```python
    {
        "question_column": "question",
        "contexts_column": "context_info"
        "ground_truth_column": "my_ground_truth_col",
    }
    ```

    If the data is stored as a dictionary in another column, specify the column and key
    like this:
    ```python
    pred_col = dataset.prediction_column(model)
    params = {
        "contexts_column": f"{pred_col}.contexts",
        "ground_truth_column": "my_ground_truth_col",
    }
    ```

    For more complex situations, you can use a function to extract the data:
    ```python
    pred_col = dataset.prediction_column(model)
    params = {
        "contexts_column": lambda x: [x[pred_col]["context_message"]],
        "ground_truth_column": "my_ground_truth_col",
    }
    ```
    """
    try:
        from ragas import evaluate
        from ragas.metrics import context_utilization
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
        "answer": answer_column,
    }

    df = get_renamed_columns(dataset._df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df), metrics=[context_utilization], **get_ragas_config()
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["context_utilization"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["context_utilization"].to_list())

    return (
        {
            # "Scores (will not be uploaded to UI)": result_df[
            #     ["question", "contexts", "answer", "context_utilization"]
            # ],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df["context_utilization"].mean(),
                    "Median Score": result_df["context_utilization"].median(),
                    "Max Score": result_df["context_utilization"].max(),
                    "Min Score": result_df["context_utilization"].min(),
                    "Standard Deviation": result_df["context_utilization"].std(),
                    "Count": result_df.shape[0],
                }
            ],
        },
        fig_histogram,
        fig_box,
    )
