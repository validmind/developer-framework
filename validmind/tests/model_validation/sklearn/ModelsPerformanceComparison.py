# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from functools import partial
from numpy import unique
import pandas as pd
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
class ModelsPerformanceComparison(Metric):
    """
    Test that outputs the models performance comparison on the test data.
    """

    name = "models_performance_comparison"
    required_inputs = ["model", "models", "model.test_ds"]
    default_params = {"metrics": ["accuracy", "precision", "recall", "f1", "roc_auc"]}
    default_metrics = {
        "accuracy": metrics.accuracy_score,
        "precision": partial(metrics.precision_score, zero_division=0, average="micro"),
        "recall": partial(metrics.recall_score, zero_division=0, average="micro"),
        "f1": partial(metrics.f1_score, zero_division=0, average="micro"),
        "roc_auc": partial(multiclass_roc_auc_score),
    }

    def description(self):
        return """
        This section shows the models performance comparison on the training data. Popular
        metrics such as the accuracy, precision, recall, F1 score, etc. are
        used to evaluate the models.
        """

    def y_true(self):
        return self.model.y_train_true

    def y_pred(self):
        return self.model.y_train_predict

    def summary(self, metric_value: dict):
        df = pd.DataFrame(metric_value)
        df.index.name = 'metric'
        df = df.reset_index()

        return ResultSummary(
            results=[
                ResultTable(
                    data=df.to_dict("records")
                ),
            ]
        )

    def run(self):

        # Check models list is not empty
        if not self.models:
            raise ValueError("List of models must be provided in the models parameter to compare")

        all_models = [self.model]

        if self.models is not None:
            all_models.extend(self.models)
        results = {}
        m = 0
        for model in all_models:
            y_true = model.y_test_true
            class_pred = model.y_test_predict
            result = {}
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
                    result[metric_name] = format_number(metric_func(
                        y_true, class_pred, pos_label=unique(y_true)[0])
                    )
                else:
                    result[metric_name] = format_number(metric_func(y_true, class_pred))
            results["model_" + str(m)] = result
            m += 1
        return self.cache_results(results)
