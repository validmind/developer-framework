# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from numpy import unique
from sklearn import metrics

from validmind.errors import SkipTestError
from validmind.vm_models import ResultSummary, ResultTable, ResultTableMetadata

from .ClassifierPerformance import ClassifierPerformance, multiclass_roc_auc_score


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
        return self.model.y_test_true

    def y_pred(self):
        return self.model.y_test_predict

    def binary_summary(self, metric_value: dict):
        """
        When building a binary classification summary for all the models. We take the positive class
        metrics as the global metrics.
        """
        results = []
        for m, m_v in metric_value.items():
            result = super().binary_summary(m_v)
            results.append(
                ResultTable(
                    data=result.results[0].data,
                    metadata=ResultTableMetadata(
                        title=f"{result.results[0].metadata.title}: {m}"
                    ),
                )
            )
        return ResultSummary(results=results)

    def multiclass_summary(self, metric_value: dict):
        """
        The multi-class summary method that calculates weighted average,
        macro average and per class metrics of all the models.
        """
        results = []
        for m, m_v in metric_value.items():
            result = super().multiclass_summary(m_v)
            results.append(
                ResultTable(
                    data=result.results[0].data,
                    metadata=ResultTableMetadata(
                        title=f"{result.results[0].metadata.title}: {m}"
                    ),
                )
            )
            results.append(
                ResultTable(
                    data=result.results[1].data,
                    metadata=ResultTableMetadata(
                        title=f"{result.results[1].metadata.title}: {m}"
                    ),
                )
            )
        return ResultSummary(results=results)

    def summary(self, metric_value: dict):
        """
        This summary varies depending if we're evaluating a binary or multi-class model
        """
        if len(unique(self.y_true())) > 2:
            return self.multiclass_summary(metric_value)

        return self.binary_summary(metric_value)

    def run(self):
        # Check models list is not empty
        if not self.models:
            raise SkipTestError(
                "List of models must be provided as a `models` parameter to compare perforance"
            )

        all_models = [self.model]

        if self.models is not None:
            all_models.extend(self.models)
        results = {}
        for idx, model in enumerate(all_models):
            y_true = model.y_test_true
            class_pred = model.y_test_predict
            report = metrics.classification_report(y_true, class_pred, output_dict=True)
            report["roc_auc"] = multiclass_roc_auc_score(y_true, class_pred)
            results["model_" + str(idx)] = report
        return self.cache_results(results)
