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
    **Purpose**: The provided script assesses the performance of Machine Learning classification models. The
    performance is calculated by determining the precision, recall, F1-Score, accuracy, and the ROC AUC (Receiver
    operating characteristic - Area under the curve) scores. The test accepts both binary and multiclass models.

    **Test Mechanism**: The script generates a report that includes precision, recall, F1-Score, and accuracy using the
    `classification_report` method from the scikit-learn's metrics module. For multiclass models, weighted and macro
    averages for these scores are also computed. Additionally, the script calculates and includes the ROC AUC scores
    for the model using a custom method, `multiclass_roc_auc_score`. The output of the test is a structured report that
    differs depending on whether the model is binary or multiclass.

    **Signs of High Risk**: Indicators of high risk or a failing model include low values for the metrics used -
    precision, recall, F1-Score, accuracy, and ROC AUC. An imbalanced precision and recall score can also indicate a
    high-risk model, as precision focuses on the correct prediction of the positive class, while recall focuses on the
    number of correctly identified actual positive cases. A low ROC AUC score, particularly when it is close to 0.5 or
    below, is a strong indicator of a failing model.

    **Strengths**: This metric excels in its versatility by being capable of handling both binary and multiclass
    models. It computes several commonly used performance metrics, providing a comprehensive view of the model's
    performance. Using ROC-AUC as a metric can help in identifying the best threshold for classification, especially
    when datasets are unbalanced.

    **Limitations**: The test relies on labels being correctly identified for binary classification models, raising an
    exception if the positive class is not labeled as "1", which might not always be the case in practical
    applications. Furthermore, this script is designed only for classification models and cannot evaluate regression
    models. The calculated metrics might not be informative in situations where the test dataset is not representative
    of the data the model will encounter.
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

    def binary_summary(self, metric_value: dict):
        """
        When building a binary classification summary we take the positive class
        metrics as the global metrics.
        """
        # Assume positive class is "1" and throw an error if that's not the case
        if "1.0" not in metric_value:
            raise ValueError(
                "Positive class not found in the metrics. Please make sure the positive class is labeled as '1' when testing a binary classifier."
            )

        table = []
        for metric_name in ["precision", "recall", "f1-score"]:
            table.append(
                {
                    "Metric": metric_name.capitalize()
                    if metric_name != "f1-score"
                    else "F1",
                    "Value": metric_value["1.0"][metric_name],
                }
            )

        table.extend(
            [
                {
                    "Metric": "Accuracy" if metric_name == "accuracy" else "ROC AUC",
                    "Value": metric_value[metric_name],
                }
                for metric_name in ["accuracy", "roc_auc"]
            ]
        )

        return ResultSummary(
            results=[
                ResultTable(
                    data=table,
                    metadata=ResultTableMetadata(title="Classification Report"),
                ),
            ]
        )

    def multiclass_summary(self, metric_value: dict):
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

    def summary(self, metric_value: list):
        """
        This summary varies depending if we're evaluating a binary or multi-class model
        """
        if len(unique(self.y_true())) > 2:
            return self.multiclass_summary(metric_value)

        return self.binary_summary(metric_value)

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
