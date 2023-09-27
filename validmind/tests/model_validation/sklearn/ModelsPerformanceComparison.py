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
    **Purpose**: This metric test is intended to evaluate and compare the performance of multiple Machine Learning
    models on test data. It uses a number of metrics including accuracy, precision, recall, and F1 score among others,
    to measure model performance and aid in the selection of the most effective model for the given task.

    **Test Mechanism**: This test involves using Scikit-learn’s performance metrics to assess model's performance in
    both binary and multiclass classification tasks. To compare the performances, it evaluates each model on the test
    dataset and produces a detailed classification report. This includes the aforesaid metrics, along with the roc_auc
    score. Depending on whether the task at hand is binary or multiclass classification, it calculates metrics globally
    for the "positive" class or their weighted averages, macro averages, and per class metrics respectively. If no
    models are provided, the test is skipped.

    **Signs of High Risk**: High risk or poor model performance might be indicated by low accuracy, precision, recall,
    and/or F1 scores, or a low area under the Receiver Operating Characteristic (ROC) curve (roc_auc). If the metrics'
    scores are significantly lower than alternative models, it might suggest a high failure risk.

    **Strengths**: This test allows for straightforward performance comparison of multiple models, accommodating both
    binary and multiclass classification tasks. It provides a comprehensive report of key performance metrics, offering
    a holistic view of model performance. It also includes ROC AUC, a robust performance metric that is capable of
    dealing effectively with class imbalance issues.

    **Limitations**: This test may not be comprehensive for more complex performance evaluations that consider other
    factors, such as speed of prediction, computational cost, or specific business constraints. It's also reliant on
    the provided test dataset, so the chosen models' performance could differ on unseen data or when the data
    distribution changes. The ROC AUC score isn't necessarily meaningful for multilabel/multiclass tasks, and can be
    hard to interpret in such contexts.
    """

    name = "models_performance_comparison"
    required_inputs = ["model", "models", "model.test_ds"]
    metadata = {
        "task_types": ["classification", "text_classification"],
        "tags": [
            "sklearn",
            "binary_classification",
            "multiclass_classification",
            "model_performance",
            "model_comparison",
        ],
    }

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
