# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from functools import partial

from numpy import unique
from sklearn import metrics, preprocessing

from validmind.utils import format_number
from validmind.vm_models import Metric, ResultSummary, ResultTable


def multiclass_roc_auc_score(y_test, y_pred, average="macro"):
    lb = preprocessing.LabelBinarizer()
    lb.fit(y_test)
    y_test = lb.transform(y_test)
    y_pred = lb.transform(y_pred)
    return metrics.roc_auc_score(y_test, y_pred, average=average)


@dataclass
class ClassifierPerformance(Metric):
    """
    Test that outputs the performance of the model on the training or test data.
    """

    name = "classifier_performance"
    default_params = {"metrics": ["accuracy", "precision", "recall", "f1", "roc_auc"]}

    default_metrics = {
        "accuracy": {
            "func": metrics.accuracy_score,
            "name": "Accuracy",
            "definition": "Overall, how often is the model correct?",
            "formula": "TP + TN / (TP + TN + FP + FN)",
        },
        "precision": {
            "func": partial(metrics.precision_score, zero_division=0, average="micro"),
            "name": "Precision",
            "definition": 'When the model predicts "{target_column}", how often is it correct?',
            "formula": "TP / (TP + FP)",
        },
        "recall": {
            "func": partial(metrics.recall_score, zero_division=0, average="micro"),
            "name": "Recall",
            "definition": 'When it\'s actually "{target_column}", how often does the model predict "{target_column}"?',
            "formula": "TP / (TP + FN)",
        },
        "f1": {
            "func": partial(metrics.f1_score, zero_division=0, average="micro"),
            "name": "F1",
            "definition": "Harmonic mean of precision and recall",
            "formula": "2 x (Precision x Recall) / (Precision + Recall)",
        },
        "roc_auc": {
            "func": partial(multiclass_roc_auc_score),
            "name": "ROC AUC",
            "definition": "Area under the Receiver Operating Characteristic curve",
            "formula": "TPR / FPR",
        },
    }

    def metrics(self):
        """
        Resolves the metrics to be used in the test by filtering out any default
        metric that is ommitted via params
        """
        metrics_names = self.params.get("metrics", self.default_params["metrics"])
        metrics = {
            metric_name: self.default_metrics[metric_name]
            for metric_name in metrics_names
        }

        return metrics

    def summary(self, metric_value: dict):
        # Get the target column from any of the datasets available
        ds = self.model.train_ds or self.model.test_ds
        target_column = ds.target_column

        metrics = self.metrics()

        # Turns the metric value into a table of [{metric_name: value}]
        summary_in_sample_performance = []
        for metric_name, metric_value in metric_value.items():
            metric_dict = metrics[metric_name]
            summary_in_sample_performance.append(
                {
                    "Metric": metric_dict["name"],
                    "Definition": metric_dict["definition"].format(
                        target_column=target_column
                    ),
                    "Formula": metric_dict["formula"],
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

        metrics = self.metrics()

        for metric_name, metric_dict in metrics.items():
            metric_func = metric_dict["func"]
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
