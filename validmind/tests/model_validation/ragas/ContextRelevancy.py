# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import warnings

import plotly.express as px
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_relevancy

from validmind import tags, tasks

from .utils import get_ragas_config, get_renamed_columns


@tags("ragas", "llm", "retrieval_performance")
@tasks("text_qa", "text_generation", "text_summarization", "text_classification")
def ContextRelevancy(
    dataset,
    question_column: str = "question",
    contexts_column: str = "contexts",
):
    """
    Evaluates the context relevancy metric for entries in a dataset and visualizes the
    results.

    This metric gauges the relevancy of the retrieved context, calculated based on both
    the `question` and `contexts`. The values fall within the range of (0, 1), with
    higher values indicating better relevancy.

    Ideally, the retrieved context should exclusively contain essential information to
    address the provided query. To compute this, we initially estimate the value of by
    identifying sentences within the retrieved context that are relevant for answering
    the given question. The final score is determined by the following formula:

    $$
    \\text{context relevancy} = {|S| \\over |\\text{Total number of sentences in retrieved context}|}
    $$

    ### Configuring Columns

    This metric requires the following columns in your dataset:
    - `question` (str): The text query that was input into the model.
    - `contexts` (List[str]): A list of text contexts which are retrieved and which
    will be evaluated to make sure they are relevant to the question.

    If the above data is not in the appropriate column, you can specify different column
    names for these fields using the parameters `question_column` and `contexts_column`.

    For example, if your dataset has this data stored in different columns, you can
    pass the following parameters:
    ```python
    {
        "question_column": "question",
        "contexts_column": "context_info"
    }
    ```

    If the data is stored as a dictionary in another column, specify the column and key
    like this:
    ```python
    pred_col = dataset.prediction_column(model)
    params = {
        "contexts_column": f"{pred_col}.contexts",
    }
    ```

    For more complex situations, you can use a function to extract the data:
    ```python
    pred_col = dataset.prediction_column(model)
    params = {
        "contexts_column": lambda x: [x[pred_col]["context_message"]],
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
        "contexts": contexts_column,
    }

    df = get_renamed_columns(dataset.df, required_columns)

    result_df = evaluate(
        Dataset.from_pandas(df), metrics=[context_relevancy], **get_ragas_config()
    ).to_pandas()

    fig_histogram = px.histogram(x=result_df["context_relevancy"].to_list(), nbins=10)
    fig_box = px.box(x=result_df["context_relevancy"].to_list())

    return (
        {
            "Scores (will not be uploaded to UI)": result_df[
                ["question", "contexts", "context_relevancy"]
            ],
            "Aggregate Scores": [
                {
                    "Mean Score": result_df["context_relevancy"].mean(),
                    "Median Score": result_df["context_relevancy"].median(),
                    "Max Score": result_df["context_relevancy"].max(),
                    "Min Score": result_df["context_relevancy"].min(),
                    "Standard Deviation": result_df["context_relevancy"].std(),
                    "Count": len(result_df),
                }
            ],
        },
        fig_histogram,
        fig_box,
    )
