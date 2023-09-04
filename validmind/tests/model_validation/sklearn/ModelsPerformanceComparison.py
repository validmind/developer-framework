# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from .ClassifierPerformance import ClassifierPerformance
from numpy import unique
from validmind.utils import format_number
from validmind.vm_models import ResultSummary, ResultTable


@dataclass
class ModelsPerformanceComparison(ClassifierPerformance):
    """
    Test that outputs the performance of the model on the training data.
    """

    name = "models_performance_comparison"
    required_inputs = ["model", "models", "model.test_ds"]

    def description(self):
        return """
        This section shows the performance of the model on the training data. Popular
        metrics such as the accuracy, precision, recall, F1 score, etc. are
        used to evaluate the model.
        """

    def y_true(self):
        return self.model.y_train_true

    def y_pred(self):
        return self.model.y_train_predict

    def summary(self, metric_value: dict):
        # Turns the metric value into a table of [{metric_name: value}]
        print(metric_value)
        summary_out_sample_performance = []
        for model_id, model_value in metric_value.iteritems():
            for metric, value in metric_value[model_id].iteritems():
                print(metric, value)
        
        for metric_name, metric_value in metric_value.items():
            summary_out_sample_performance.append(
                {
                    "Metric": metric_name.title(),
                    "Definition": self.metric_definitions[metric_name].format(
                        target_column=self.model.train_ds.target_column
                    ),
                    "Formula": self.metric_formulas[metric_name],
                    "Value": format_number(metric_value),
                }
            )
        print("summary_out_sample_performance", summary_out_sample_performance)
        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_out_sample_performance
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

        print(all_models)
        results = {}
        m = 0
        for model in all_models:
                
            y_true = model.y_test_true
            class_pred = model.y_test_predict
            result = {}
            metrics = self.params.get("metrics", self.default_params["metrics"])
            print("metrics", metrics)
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
                    result[metric_name] = metric_func(
                        y_true, class_pred, pos_label=unique(y_true)[0]
                    )
                else:
                    result[metric_name] = metric_func(y_true, class_pred)
            result["model_name"] = "model_" + str(m)
            results[ "model_" + str(m)] = result
            m += 1
        print(results)
        return self.cache_results(results)
