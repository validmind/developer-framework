# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from numpy import unique
from sklearn import metrics, preprocessing

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


def multiclass_roc_auc_score(y_test, y_pred, average="macro"):
    lb = preprocessing.LabelBinarizer()
    lb.fit(y_test)
    y_test = lb.transform(y_test)
    y_pred = lb.transform(y_pred)
    return metrics.roc_auc_score(y_test, y_pred, average=average)


@dataclass
class ClassifierPerformance(Metric):
    """
    Evaluates performance of binary or multiclass classification models using precision, recall, F1-Score, accuracy,
    and ROC AUC scores.

    **Purpose**: The supplied script is designed to evaluate the performance of Machine Learning classification models.
    It accomplishes this by computing precision, recall, F1-Score, and accuracy, as well as the ROC AUC (Receiver
    operating characteristic - Area under the curve) scores, thereby providing a comprehensive analytic view of the
    models' performance. The test is adaptable, handling binary and multiclass models equally effectively.

    **Test Mechanism**: The script produces a report that includes precision, recall, F1-Score, and accuracy, by
    leveraging the `classification_report` from the scikit-learn's metrics module. For multiclass models, macro and
    weighted averages for these scores are also calculated. Additionally, the ROC AUC scores are calculated and
    included in the report using the script's unique `multiclass_roc_auc_score` function. The outcome of the test
    (report format) differs based on whether the model is binary or multiclass.

    **Signs of High Risk**:
    - Low values for precision, recall, F1-Score, accuracy, and ROC AUC, indicating poor performance.
    - Imbalance in precision and recall scores. Precision highlights correct positive class predictions, while recall
    indicates the accurate identification of actual positive cases. Imbalance may indicate flawed model performance.
    - A low ROC AUC score, especially scores close to 0.5 or lower, strongly suggests a failing model.

    **Strengths**:
    - The script is versatile, capable of assessing both binary and multiclass models.
    - It uses a variety of commonly employed performance metrics, offering a comprehensive view of a model's
    performance.
    - The use of ROC-AUC as a metric aids in determining the most optimal threshold for classification, especially
    beneficial when evaluation datasets are unbalanced.

    **Limitations**:
    - The test assumes correctly identified labels for binary classification models and raises an exception if the
    positive class is not labeled as "1". However, this setup may not align with all practical applications.
    - This script is specifically designed for classification models and is not suited to evaluate regression models.
    - The metrics computed may provide limited insights in cases where the test dataset does not adequately represent
    the data the model will encounter in real-world scenarios.
    """

    name = "classifier_performance"
    metadata = {
        "task_types": ["classification", "text_classification"],
        "tags": [
            "sklearn",
            "binary_classification",
            "multiclass_classification",
            "model_performance",
        ],
    }

    def summary(self, metric_value: dict):
        """
        When building a multi-class summary we need to calculate weighted average,
        macro average and per class metrics.
        """
        classes = {str(i) for i in unique(self.y_true())}
        pr_f1_table = [
            {
                "Class": class_name,
                "Precision": metric_value[class_name]["precision"],
                "Recall": metric_value[class_name]["recall"],
                "F1": metric_value[class_name]["f1-score"],
            }
            for class_name in classes
        ]
        pr_f1_table.extend(
            [
                {
                    "Class": "Weighted Average",
                    "Precision": metric_value["weighted avg"]["precision"],
                    "Recall": metric_value["weighted avg"]["recall"],
                    "F1": metric_value["weighted avg"]["f1-score"],
                },
                {
                    "Class": "Macro Average",
                    "Precision": metric_value["macro avg"]["precision"],
                    "Recall": metric_value["macro avg"]["recall"],
                    "F1": metric_value["macro avg"]["f1-score"],
                },
            ]
        )

        acc_roc_auc_table = [
            {
                "Metric": "Accuracy" if metric_name == "accuracy" else "ROC AUC",
                "Value": metric_value[metric_name],
            }
            for metric_name in ["accuracy", "roc_auc"]
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pr_f1_table,
                    metadata=ResultTableMetadata(title="Precision, Recall, and F1"),
                ),
                ResultTable(
                    data=acc_roc_auc_table,
                    metadata=ResultTableMetadata(title="Accuracy and ROC AUC"),
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

        report = metrics.classification_report(y_true, class_pred, output_dict=True)
        report["roc_auc"] = multiclass_roc_auc_score(y_true, class_pred)

        return self.cache_results(report)
