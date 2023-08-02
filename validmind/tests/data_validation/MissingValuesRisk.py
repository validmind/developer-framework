# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class MissingValuesRisk(Metric):
    """
    Analyzes the risk associated with missing values in a tabular dataset, providing
    two risk measures:
    1) Percentage of missing values in the dataset
    2) Percentage of variables with missing values.
    """

    name = "missing_values_risk"
    required_context = ["dataset"]

    def description(self):
        return """
        This section provides an analysis of the risk associated with missing values in the dataset, providing two risk measures: 1) Percentage of missing values in the dataset 2) Percentage of variables with missing values.
        """

    def run(self):
        total_cells = self.dataset.df.size
        total_missing = self.dataset.df.isnull().sum().sum()
        total_columns = self.dataset.df.shape[1]
        columns_with_missing = self.dataset.df.isnull().any().sum()

        risk_measures = {
            "Missing Values in the Dataset": round(
                (total_missing / total_cells) * 100, 2
            ),
            "Variables with Missing Values": round(
                (columns_with_missing / total_columns) * 100, 2
            ),
        }

        return self.cache_results(risk_measures)

    def summary(self, metric_value):
        risk_measures_table = [
            {"Risk Metric": measure, "Value (%)": value}
            for measure, value in metric_value.items()
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=risk_measures_table,
                    metadata=ResultTableMetadata(title="Missing Values Risk Measures"),
                ),
            ]
        )
