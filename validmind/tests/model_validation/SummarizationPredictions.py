# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable


@dataclass
class SummarizationPredictions(Metric):
    """
    Description for Summarization Predictions
    """

    name = "summarization_predictions"
    default_params = {"display_limit": 5}
    required_inputs = ["model"]
    metadata = {
        "task_types": ["text_summarization"],
        "tags": ["summarization"],
    }

    def description(self):
        return """
        Detailed description coming soon...!
        """

    def run(self):
        display_limit = self.params["display_limit"]

        # Check model attributes
        if not hasattr(self, "model"):
            raise AttributeError("The 'model' attribute is missing.")

        y_true = self.model.y_test_true
        y_pred = self.model.y_test_predict
        text_column = self.model.test_ds.text_column
        text_input = self.model.test_ds.df[text_column]

        # Ensure consistency in lengths
        if not len(y_true) == len(y_pred) == len(text_input):
            raise ValueError(
                "Inconsistent lengths among input text, true summaries, and predicted summaries."
            )

        # Create a DataFrame with results and user-friendly column names
        df = pd.DataFrame(
            {
                "Input Text": text_input,
                "Target Text": y_true.reshape(-1),
                "Predicted Summaries": y_pred,
            }
        )

        # Limit the number of rows to display based on the display_limit
        df = df.head(display_limit)

        return self.cache_results(df.to_dict(orient="records"))

    def summary(self, metric_value):
        df = pd.DataFrame(metric_value)

        return ResultSummary(
            results=[
                ResultTable(data=df.to_dict(orient="records")),
            ]
        )
