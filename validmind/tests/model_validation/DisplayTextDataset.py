# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable


@dataclass
class DisplayTextDataset(Metric):
    """
    **Purpose:**
    The DisplayTextDataset metric provides a tabulated visualization of a text dataset. Geared towards tasks
    such as text summarization and text generation, this metric aims to showcase the primary contents of the dataset,
    particularly the input text and the corresponding target text.

    **Test Mechanism:**
    The metric extracts data from the given dataset, specifically the input text and target text columns. It then
    verifies the consistency in the lengths of these columns to ensure accurate visualization and data integrity.
    The extracted data is presented in a structured table format. The main representation of this metric is a table that juxtaposes the input text with its associated target text.
    This visualization provides a straightforward way to observe and understand the data structure and the relationships
    between inputs and outputs.

    **Signs of High Risk:**
    Mismatches or inconsistencies between the input text and target text can indicate potential issues with the dataset's
    quality or construction. Any discrepancies, missing data, or data anomalies highlighted by the metric might point to
    deeper issues requiring dataset cleanup or re-evaluation.

    **Strengths:**
    The structured table layout offers an intuitive, clear snapshot of the dataset's content, making it easier for stakeholders
    or developers to review the data at a glance. This metric aids in data understanding, verification, and potentially even
    error spotting at the data level.

    **Limitations:**
    The metric provides a surface-level view, based on the `display_limit` parameter, and may not showcase the entire dataset.
    While the table format aids in quick reviews, it doesn't offer deeper insights into potential data biases, quality, or
    other advanced dataset properties. For more nuanced analysis, additional metrics or tools might be necessary.
    """

    name = "display_text_dataset"
    default_params = {"display_limit": 5}
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["text_summarization", "text_generation"],
        "tags": ["display_text_dataset"],
    }

    def _get_datasets(self):
        # Check dataset attributes
        if not hasattr(self, "dataset"):
            raise AttributeError("The 'dataset' attribute is missing.")

        input_text = self.dataset.df[self.dataset.text_column]
        y_true = self.dataset.df[self.dataset.target_column]

        # Ensure consistency in lengths
        if not len(y_true) == len(input_text):
            raise ValueError(
                "Inconsistent lengths among input text and true summaries."
            )

        return input_text, y_true

    def summary(self, metric_value):
        df = pd.DataFrame(metric_value)

        return ResultSummary(
            results=[
                ResultTable(data=df.to_dict(orient="records")),
            ]
        )

    def run(self):
        input_text, y_true = self._get_datasets()

        display_limit = self.params["display_limit"]

        df = pd.DataFrame(
            {
                "Input Text": input_text,
                "Target Text": y_true,
            }
        )

        # Limit the number of rows to display based on the display_limit
        df = df.head(display_limit)

        return self.cache_results(df.to_dict(orient="records"))
