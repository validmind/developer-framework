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
    Test that outputs the performance of the model on the training or test data.
    """

    name = "classifier_performance"

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
