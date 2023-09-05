# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from .ClassifierPerformance import ClassifierPerformance
from numpy import unique
import pandas as pd
from validmind.utils import format_number
from validmind.vm_models import ResultSummary, ResultTable


@dataclass
class ModelsPerformanceComparison(ClassifierPerformance):
    """
    Test that outputs the models performance comparison on the test data.
    """

    name = "models_performance_comparison"
    required_inputs = ["model", "models", "model.test_ds"]

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
        df["definition"] = df.metric.apply(lambda m: self.metric_definitions[m].format(
            target_column=self.model.train_ds.target_column))
        df["formula"] = df.metric.apply(lambda m: self.metric_formulas[m])
        return ResultSummary(
            results=[
                ResultTable(
                    data=df
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
        return self.cache_results(pd.DataFrame(results))
