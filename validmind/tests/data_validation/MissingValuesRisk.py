# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class MissingValuesRisk(Metric):
    """
    **Purpose**: This metric, Missing Values Risk, is intended to evaluate and quantify the risk associated with
    missing values in the data set being used for machine learning model training. This metric determines two specific
    risk measures: 1) what percentage of total data in the dataset are missing values, and 2) what percentage of total
    variables (i.e., columns) in the dataset have at least some missing values.

    **Test Mechanism**: The metric tests the dataset by first calculating the total number of datapoints in the data
    set and the total count of missing values. Then, it examines each column(variable) to find out how many contain at
    least one missing data point. By meticulously counting missing data points across the whole dataset and then within
    each variable(column), the metric determines the percentage of missing values in the total dataset and the
    percentage of columns(variables) with missing values.

    **Signs of High Risk**: High percentages in either of the risk measures could indicate a high risk. If the dataset
    has a high percentage of missing values, then it can significantly affect the performance and reliability of the
    model. Similarly, if a lot of variables (columns) in the dataset have missing values, the model might be prone to
    bias or overfitting.

    **Strengths**: This metric provides invaluable insight into the dataset's readiness for model training, as missing
    values can severely impact both the model's performance and its predictions. Quantifying the risk posed by missing
    values allows for targeted methods to handle these values properly, either through deletion, imputation, or other
    strategies. The metric is flexible and can be applied to both classification and regression tasks, thereby
    maintaining its utility across a broad range of models and scenarios.

    **Limitations**: This metric only identifies and quantifies the risk of missing values but does not offer any
    solutions to mitigate this risk. More specifically, it does not infer whether the missingness is random or linked
    to some underlying issue in data collection or preprocessing. Nonetheless, identifying the presence and extent of
    missingness is the essential first step in data-quality improvement.
    """

    name = "missing_values_risk"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "data_quality", "risk_analysis"],
    }

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
