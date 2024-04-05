from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class LogRegPerformanceTable(Metric):
    """
    Evaluates logistic regression model performance using F1, Accuracy, Recall, and Precision metrics for multiple datasets,
    allowing for the adjustment of the classification threshold.

    **Purpose**: Tailored for logistic regression models, this enhanced class calculates F1 score, Accuracy, Recall, and Precision
    for any number of datasets, using probability thresholds to convert model outputs to binary classifications. The `cut_off_threshold`
    parameter enables precision in class differentiation based on probability scores, making it invaluable for nuanced performance assessment.

    **Test Mechanism**: Leverages a dictionary for storing metrics across datasets, calculating them through sklearn.metrics functions
    after converting predicted probabilities to binary outcomes via the provided threshold. The results are compiled into a pandas DataFrame,
    facilitating straightforward analysis and visualization.

    **Strengths**:
    - Designed for logistic regression models, offering detailed performance insights.
    - Adjustable classification threshold caters to varied analysis requirements, optimizing model evaluation.

    **Limitations**:
    - Primarily suited for binary classification, with potential need for adjustments in multi-class or imbalanced dataset scenarios.
    """

    name = "log_reg_performance_table"
    required_inputs = ["model", "datasets"]
    metadata = {
        "task_types": ["binary_classification"],
        "tags": ["visualization", "model_performance", "logistic_regression"],
    }

    default_params = {
        "cut_off_threshold": 0.5,  # Default cutoff threshold
    }

    def run(self):
        cut_off_threshold = self.params["cut_off_threshold"]

        summary_metrics = self.compute_metrics(cut_off_threshold)

        return self.cache_results(
            {
                "metrics_summary": summary_metrics.to_dict(orient="records"),
            }
        )

    def summary(self, metric_value):
        summary_metrics_table = metric_value["metrics_summary"]
        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_metrics_table,
                    metadata=ResultTableMetadata(
                        title="Performance Metrics",
                    ),
                )
            ]
        )

    def compute_metrics(self, cut_off_threshold):
        """Computes F1, Accuracy, Recall, and Precision for datasets using a specified cutoff threshold."""
        metrics_dict = {
            "Dataset": [],
            "F1": [],
            "Accuracy": [],
            "Recall": [],
            "Precision": [],
        }

        for dataset in self.inputs.datasets:
            dataset_id = dataset.input_id
            y_true = dataset.y
            y_pred_prob = dataset.y_pred(self.inputs.model.input_id)

            # Convert probabilities to binary outcomes based on the cutoff threshold
            y_pred = np.where(y_pred_prob > cut_off_threshold, 1, 0)

            # Compute metrics
            accuracy = accuracy_score(y_true, y_pred)
            recall = recall_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred)
            f1 = f1_score(y_true, y_pred)

            # Add the metrics to the dictionary
            metrics_dict["Dataset"].append(dataset_id)
            metrics_dict["Accuracy"].append(accuracy)
            metrics_dict["Recall"].append(recall)
            metrics_dict["Precision"].append(precision)
            metrics_dict["F1"].append(f1)

        metrics_df = pd.DataFrame(metrics_dict)
        return metrics_df
