# Copyright © 2023 ValidMind Inc. All rights reserved.

import itertools
from dataclasses import dataclass

import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable


@dataclass
class SummarizationPredictions(Metric):
    """
    **Purpose:**
    The SummarizationPredictions metric provides a comparison between predicted text summaries and the
    actual target texts. Intended primarily for models focusing on the text summarization task, this metric
    offers insights into the effectiveness and accuracy of generated summaries relative to their original content.

    **Visualization:**
    The primary representation is tabular, where the input text, its target summary, and the model's predicted
    summary are juxtaposed for direct comparison. This tabulated data allows for a clear, side-by-side analysis
    of the model's performance against ground truth summaries.

    **Test Mechanism:**
    The metric fetches data from specific text columns—namely input text, target text (true summary), and the
    predicted summary. After ensuring consistent lengths and data integrity among these columns, the relevant
    segments are extracted and tabulated.

    **Signs of High Risk:**
    Discrepancies between target summaries and predicted summaries might indicate model inaccuracies or lack
    of training. If predicted summaries consistently deviate from their target counterparts or don't capture
    the essence of the input text, there are potential issues in the model's summarization capabilities.

    **Strengths:**
    The tabular representation enables a direct, at-a-glance comparison of model predictions with target data.
    This kind of visualization is invaluable for stakeholders or researchers keen on understanding the model's
    real-world performance, especially in terms of fidelity and coherence.

    **Limitations:**
    While the table provides a snapshot comparison, it does not delve into specific reasons for discrepancies
    between predicted and target summaries. Also, the metric's output might be limited by the `display_limit`
    parameter, which means not all data points might be showcased. For more detailed error analysis or reasons
    for divergence, further specialized metrics or evaluation might be needed.
    """

    name = "summarization_predictions"
    default_params = {"display_limit": 5}
    required_inputs = ["model"]
    metadata = {
        "task_types": [
            "text_classification",
            "text_summarization",
        ],
        "tags": ["summarization_predictions"],
    }

    def _get_datasets(self):
        # Check model attributes
        if not hasattr(self, "model"):
            raise AttributeError("The 'model' attribute is missing.")

        y_true = list(itertools.chain.from_iterable(self.model.y_test_true))
        y_pred = self.model.y_test_predict
        input_text = self.model.test_ds.df[self.model.test_ds.text_column]

        # Ensure consistency in lengths
        if not len(y_true) == len(y_pred) == len(input_text):
            raise ValueError(
                "Inconsistent lengths among input text, true summaries, and predicted summaries."
            )

        return input_text, y_true, y_pred

    def summary(self, metric_value):
        df = pd.DataFrame(metric_value)

        return ResultSummary(
            results=[
                ResultTable(data=df.to_dict(orient="records")),
            ]
        )

    def run(self):
        display_limit = self.params["display_limit"]

        input_text, y_true, y_pred = self._get_datasets()

        # Create a DataFrame with results and user-friendly column names
        df = pd.DataFrame(
            {
                "Input Text": input_text,
                "Target Text": y_true,
                "Predicted Summaries": y_pred,
            }
        )

        # Limit the number of rows to display based on the display_limit
        df = df.head(display_limit)

        return self.cache_results(df.to_dict(orient="records"))
