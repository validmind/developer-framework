# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable, VMDataset


@dataclass
class DisplayTextDataset(Metric):
    """
    Description for ...
    """

    name = "display_text_dataset"
    default_params = {"display_limit": 5, "text_columns": None}
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["text_summarization", "text_generation"],
        "tags": ["summarization"],
    }

    def description(self):
        return """
        Detailed description coming soon...!
        """

    def run(self):
        if not isinstance(self.dataset, VMDataset):
            raise ValueError("TextDescretion requires a validmind Dataset object")

        display_limit = self.params["display_limit"]
        text_columns = self.params["text_columns"]

        text_column = self.dataset.text_column
        text_column_values = self.dataset.df[text_column]

        data_dict = {"Input Text": text_column_values}

        if hasattr(self.dataset, "target_column"):
            target_column = self.dataset.target_column
            target_column_values = self.dataset.df[target_column]
            data_dict["Target Text"] = target_column_values

        # If text_columns are passed, use those
        if text_columns:
            missing_columns = [
                col for col in text_columns if col not in self.dataset.df.columns
            ]
            if missing_columns:
                raise ValueError(
                    f"The following columns are missing from 'test_ds': {', '.join(missing_columns)}"
                )

            data_dict = {col: self.dataset.df[col] for col in text_columns}

        df = pd.DataFrame(data_dict)

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
