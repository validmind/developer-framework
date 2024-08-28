# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from functools import partial
from typing import List

import pandas as pd
from numpy import unique
from sklearn import metrics, preprocessing

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


def multiclass_roc_auc_score(y_test, y_pred, average="macro"):
    lb = preprocessing.LabelBinarizer()
    lb.fit(y_test)
    y_test = lb.transform(y_test)
    y_pred = lb.transform(y_pred)
    return metrics.roc_auc_score(y_test, y_pred, average=average)


@dataclass
class TrainingTestDegradation(ThresholdTest):
    """
    Tests if model performance degradation between training and test datasets exceeds a predefined threshold.

    ### Purpose

    The `TrainingTestDegradation` class serves as a test to verify that the degradation in performance between the
    training and test datasets does not exceed a predefined threshold. This test measures the model's ability to
    generalize from its training data to unseen test data, assessing key classification metrics such as accuracy,
    precision, recall, and f1 score to verify the model's robustness and reliability.

    ### Test Mechanism

    The code applies several predefined metrics, including accuracy, precision, recall, and f1 scores, to the model's
    predictions for both the training and test datasets. It calculates the degradation as the difference between the
    training score and test score divided by the training score. The test is considered successful if the degradation
    for each metric is less than the preset maximum threshold of 10%. The results are summarized in a table showing
    each metric's train score, test score, degradation percentage, and pass/fail status.

    ### Signs of High Risk

    - A degradation percentage that exceeds the maximum allowed threshold of 10% for any of the evaluated metrics.
    - A high difference or gap between the metric scores on the training and the test datasets.
    - The 'Pass/Fail' column displaying 'Fail' for any of the evaluated metrics.

    ### Strengths

    - Provides a quantitative measure of the model's ability to generalize to unseen data, which is key for predicting
    its practical real-world performance.
    - By evaluating multiple metrics, it takes into account different facets of model performance and enables a more
    holistic evaluation.
    - The use of a variable predefined threshold allows the flexibility to adjust the acceptability criteria for
    different scenarios.

    ### Limitations

    - The test compares raw performance on training and test data but does not factor in the nature of the data. Areas
    with less representation in the training set might still perform poorly on unseen data.
    - It requires good coverage and balance in the test and training datasets to produce reliable results, which may
    not always be available.
    - The test is currently only designed for classification tasks.
    """

    name = "training_test_degradation"
    required_inputs = ["model", "datasets"]

    default_params = {
        "metrics": ["accuracy", "precision", "recall", "f1"],
        "max_threshold": 0.10,  # Maximum 10% degradation
    }

    tasks = ["classification", "text_classification"]
    tags = [
        "sklearn",
        "binary_classification",
        "multiclass_classification",
        "model_performance",
        "visualization",
    ]

    default_metrics = {
        "accuracy": metrics.accuracy_score,
        "precision": partial(metrics.precision_score, zero_division=0, average="micro"),
        "recall": partial(metrics.recall_score, zero_division=0, average="micro"),
        "f1": partial(metrics.f1_score, zero_division=0, average="micro"),
    }

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
        """
        The training test degradation test returns results like these:
        [{"values":
            {"test_score": 0.7225, "train_score": 0.7316666666666667, "degradation": 0.012528473804100214}, "test_name": "accuracy", "passed": true}, ...]
        """
        results_table = [
            {
                "Class": result.values["class"],
                "Metric": result.test_name.title(),
                "Train Score": result.values["train_score"],
                "Test Score": result.values["test_score"],
                "Degradation (%)": result.values["degradation"] * 100,
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pd.DataFrame(results_table),
                    metadata=ResultTableMetadata(
                        title="Training-Test Degradation Test"
                    ),
                )
            ]
        )

    def run(self):
        y_train_true = self.inputs.datasets[0].y
        y_train_pred = self.inputs.datasets[0].y_pred(self.inputs.model)
        y_train_true = y_train_true.astype(y_train_pred.dtype)

        y_test_true = self.inputs.datasets[1].y
        y_test_pred = self.inputs.datasets[1].y_pred(self.inputs.model)
        y_test_true = y_test_true.astype(y_test_pred.dtype)

        report_train = metrics.classification_report(
            y_train_true, y_train_pred, output_dict=True, zero_division=0
        )
        report_train["roc_auc"] = multiclass_roc_auc_score(y_train_true, y_train_pred)

        report_test = metrics.classification_report(
            y_test_true, y_test_pred, output_dict=True, zero_division=0
        )
        report_test["roc_auc"] = multiclass_roc_auc_score(y_test_true, y_test_pred)

        classes = {str(i) for i in unique(y_train_true)}

        test_results = []
        for class_name in classes:
            for metric_name in ["precision", "recall", "f1-score"]:
                train_score = report_train[class_name][metric_name]
                test_score = report_test[class_name][metric_name]

                # If training score is 0, degradation is assumed to be 100%
                if train_score == 0:
                    degradation = 1.0
                else:
                    degradation = (train_score - test_score) / train_score

                passed = degradation < self.params["max_threshold"]
                test_results.append(
                    ThresholdTestResult(
                        test_name=metric_name,
                        passed=passed,
                        values={
                            "class": class_name,
                            "test_score": test_score,
                            "train_score": train_score,
                            "degradation": degradation,
                        },
                    )
                )
        return self.cache_results(
            test_results, passed=all(r.passed for r in test_results)
        )
