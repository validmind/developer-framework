# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from functools import partial
from numpy import unique

from sklearn import metrics

from validmind.utils import format_number
from validmind.vm_models import Metric, ResultSummary, ResultTable


@dataclass
class ClassifierPerformance(Metric):
    """
    Test that outputs the performance of the model on the training or test data.
    """

    default_params = {"metrics": ["accuracy", "precision", "recall", "f1", "roc_auc"]}
    default_metrics = {
        "accuracy": metrics.accuracy_score,
        "precision": partial(metrics.precision_score, zero_division=0),
        "recall": partial(metrics.recall_score, zero_division=0),
        "f1": partial(metrics.f1_score, zero_division=0),
        "roc_auc": metrics.roc_auc_score,
    }

    # This will need to be moved to the backend
    metric_definitions = {
        "accuracy": "Overall, how often is the model correct?",
        "precision": 'When the model predicts "{target_column}", how often is it correct?',
        "recall": 'When it\'s actually "{target_column}", how often does the model predict "{target_column}"?',
        "f1": "Harmonic mean of precision and recall",
        "roc_auc": "Area under the Receiver Operating Characteristic curve",
    }

    metric_formulas = {
        "accuracy": "TP + TN / (TP + TN + FP + FN)",
        "precision": "TP / (TP + FP)",
        "recall": "TP / (TP + FN)",
        "f1": "2 x (Precision x Recall) / (Precision + Recall)",
        "roc_auc": "TPR / FPR",
    }

    def summary(self, metric_value: dict):
        # Turns the metric value into a table of [{metric_name: value}]
        summary_in_sample_performance = []
        for metric_name, metric_value in metric_value.items():
            summary_in_sample_performance.append(
                {
                    "Metric": metric_name.title(),
                    "Definition": self.metric_definitions[metric_name].format(
                        target_column=self.model.train_ds.target_column
                    ),
                    "Formula": self.metric_formulas[metric_name],
                    "Value": format_number(metric_value),
                }
            )

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_in_sample_performance,
                ),
            ]
        )

    def y_true(self):
        raise NotImplementedError

    def y_pred(self):
        raise NotImplementedError

    def run(self):
        y_true = self.y_true()
        class_pred = self.y_pred()
        results = {}

        metrics = self.params.get("metrics", self.default_params["metrics"])
        for metric_name in metrics:
            if metric_name not in self.default_metrics:
                raise ValueError(f"Metric {metric_name} not supported.")
            metric_func = self.default_metrics[metric_name]
            y_true = y_true.astype(class_pred.dtype)
            if (
                metric_name == "precision"
                or metric_name == "recall"
                or metric_name == "f1"
            ):
                results[metric_name] = metric_func(
                    y_true, class_pred, pos_label=unique(y_true)[0]
                )
            else:
                results[metric_name] = metric_func(y_true, class_pred)

        return self.cache_results(results)
