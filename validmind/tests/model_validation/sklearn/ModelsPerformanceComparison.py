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
    **Purpose**: This metric test aims to evaluate and compare the performance of various Machine Learning models using
    test data. It employs multiple metrics such as accuracy, precision, recall, and the F1 score, among others, to
    assess model performance and assist in selecting the most effective model for the designated task.

    **Test Mechanism**: The test employs Scikit-learn’s performance metrics to evaluate each model's performance for
    both binary and multiclass classification tasks. To compare performances, the test runs each model against the test
    dataset, then produces a comprehensive classification report. This report includes metrics such as accuracy,
    precision, recall, and the F1 score. Based on whether the task at hand is binary or multiclass classification, it
    calculates metrics globally for the "positive" class or, alternatively, their weighted averages, macro averages,
    and per class metrics. The test will be skipped if no models are supplied.

    **Signs of High Risk**:
    - Low scores in accuracy, precision, recall, and F1 metrics indicate a potentially high risk.
    - A low area under the Receiver Operating Characteristic (ROC) curve (roc_auc score) is another possible indicator
    of high risk.
    - If the metrics scores are significantly lower than alternative models, this might suggest a high risk of failure.

    **Strengths**:
    - The test provides a simple way to compare the performance of multiple models, accommodating both binary and
    multiclass classification tasks.
    - It provides a holistic view of model performance through a comprehensive report of key performance metrics.
    - The inclusion of the ROC AUC score is advantageous, as this robust performance metric can effectively handle
    class imbalance issues.

    **Limitations**:
    - This test may not be suitable for more complex performance evaluations that consider factors such as prediction
    speed, computational cost, or business-specific constraints.
    - The test's reliability depends on the provided test dataset; hence, the selected models' performance could vary
    with unseen data or changes in the data distribution.
    - The ROC AUC score might not be as meaningful or easily interpretable for multilabel/multiclass tasks.
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
