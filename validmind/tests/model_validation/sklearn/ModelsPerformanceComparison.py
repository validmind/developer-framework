# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from numpy import unique
from sklearn.metrics import classification_report

from validmind.errors import SkipTestError
from validmind.vm_models import ResultSummary, ResultTable, ResultTableMetadata

from .ClassifierPerformance import ClassifierPerformance, multiclass_roc_auc_score


@dataclass
class ModelsPerformanceComparison(ClassifierPerformance):
    """
    Evaluates and compares the performance of multiple Machine Learning models using various metrics like accuracy,
    precision, recall, and F1 score.

    ### Purpose

    The Models Performance Comparison test aims to evaluate and compare the performance of various Machine Learning
    models using test data. It employs multiple metrics such as accuracy, precision, recall, and the F1 score, among
    others, to assess model performance and assist in selecting the most effective model for the designated task.

    ### Test Mechanism

    The test employs Scikit-learn’s performance metrics to evaluate each model's performance for both binary and
    multiclass classification tasks. To compare performances, the test runs each model against the test dataset, then
    produces a comprehensive classification report. This report includes metrics such as accuracy, precision, recall,
    and the F1 score. Based on whether the task at hand is binary or multiclass classification, it calculates metrics
    for all the classes and their weighted averages, macro averages, and per-class metrics. The test will be skipped if
    no models are supplied.

    ### Signs of High Risk

    - Low scores in accuracy, precision, recall, and F1 metrics indicate a potentially high risk.
    - A low area under the Receiver Operating Characteristic (ROC) curve (roc_auc score) is another possible indicator
    of high risk.
    - If the metrics scores are significantly lower than alternative models, this might suggest a high risk of failure.

    ### Strengths

    - Provides a simple way to compare the performance of multiple models, accommodating both binary and multiclass
    classification tasks.
    - Offers a holistic view of model performance through a comprehensive report of key performance metrics.
    - The inclusion of the ROC AUC score is advantageous, as this robust performance metric can effectively handle
    class imbalance issues.

    ### Limitations

    - May not be suitable for more complex performance evaluations that consider factors such as prediction speed,
    computational cost, or business-specific constraints.
    - The test's reliability depends on the provided test dataset; hence, the selected models' performance could vary
    with unseen data or changes in the data distribution.
    - The ROC AUC score might not be as meaningful or easily interpretable for multilabel/multiclass tasks.
    """

    name = "models_performance_comparison"
    required_inputs = ["dataset", "models"]
    tasks = ["classification", "text_classification"]
    tags = [
        "sklearn",
        "binary_classification",
        "multiclass_classification",
        "model_performance",
        "model_comparison",
    ]

    def summary(self, metric_value: dict):
        """
        This summary varies depending if we're evaluating a binary or multi-class model
        """
        results = []
        prf_table = []
        classes = {str(i) for i in unique(self.inputs.dataset.y)}

        for class_name in classes:
            prf_dict = {}
            prf_dict["Class"] = class_name
            for m, _ in metric_value.items():
                prf_dict[f"Precision- {m}"] = metric_value[m][class_name]["precision"]
                prf_dict[f"Recall- {m}"] = metric_value[m][class_name]["recall"]
                prf_dict[f"F1- {m}"] = metric_value[m][class_name]["f1-score"]
            prf_table.append(prf_dict)

        avg_metrics = ["weighted avg", "macro avg"]
        for class_name in avg_metrics:
            avg_dict = {}
            avg_dict["Class"] = class_name
            for m, _ in metric_value.items():
                avg_dict[f"Precision- {m}"] = metric_value[m][class_name]["precision"]
                avg_dict[f"Recall- {m}"] = metric_value[m][class_name]["recall"]
                avg_dict[f"F1- {m}"] = metric_value[m][class_name]["f1-score"]
            prf_table.append(avg_dict)
        results.append(
            ResultTable(
                data=prf_table,
                metadata=ResultTableMetadata(
                    title="Precision, Recall, and F1 Comparison"
                ),
            )
        )

        acc_roc_auc_table = []
        for metric_name in ["accuracy", "roc_auc"]:
            acc_roc_auc_dict = {}
            acc_roc_auc_dict["Metric"] = metric_name
            for m, _ in metric_value.items():
                acc_roc_auc_dict[f"accuracy- {m}"] = metric_value[m]["accuracy"]
                acc_roc_auc_dict[f"roc_auc- {m}"] = metric_value[m]["roc_auc"]
            acc_roc_auc_table.append(acc_roc_auc_dict)
        results.append(
            ResultTable(
                data=acc_roc_auc_table,
                metadata=ResultTableMetadata(title="Accuracy and ROC AUC Comparison"),
            )
        )
        return ResultSummary(results=results)

    def run(self):
        # Check models list is not empty
        if not self.inputs.models:
            raise SkipTestError(
                "List of models must be provided as a `models` parameter to compare performance"
            )

        all_models = self.inputs.models

        results = {}
        for idx, model in enumerate(all_models):
            y_true = self.inputs.dataset.y
            y_pred = self.inputs.dataset.y_pred(model)
            report = classification_report(y_true, y_pred, output_dict=True)
            report["roc_auc"] = multiclass_roc_auc_score(y_true, y_pred)
            results["model_" + str(idx)] = report

        return self.cache_results(results)
