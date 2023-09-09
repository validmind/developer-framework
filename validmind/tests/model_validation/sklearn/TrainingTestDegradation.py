# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from functools import partial
from typing import List

import pandas as pd
from sklearn import metrics

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
)


@dataclass
class TrainingTestDegradation(ThresholdTest):
    """
    Test that the degradation in performance between the training and test datasets
    does not exceed a predefined threshold.
    """

    category = "model_performance"
    name = "training_test_degradation"
    required_inputs = ["model", "model.train_ds", "model.test_ds"]

    default_params = {
        "metrics": ["accuracy", "precision", "recall", "f1"],
        "max_threshold": 0.10,  # Maximum 10% degradation
    }
    default_metrics = {
        "accuracy": metrics.accuracy_score,
        "precision": partial(metrics.precision_score, zero_division=0, average="micro"),
        "recall": partial(metrics.recall_score, zero_division=0, average="micro"),
        "f1": partial(metrics.f1_score, zero_division=0, average="micro"),
    }

    def summary(self, results: List[TestResult], all_passed: bool):
        """
        The training test degradation test returns results like these:
        [{"values":
            {"test_score": 0.7225, "train_score": 0.7316666666666667, "degradation": 0.012528473804100214}, "test_name": "accuracy", "passed": true}, ...]
        """
        results_table = [
            {
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
        y_test_true = self.model.y_test_true
        y_train_true = self.model.y_train_true
        train_class_pred = self.model.y_train_predict
        y_train_true = y_train_true.astype(train_class_pred.dtype)
        test_class_pred = self.model.y_test_predict
        y_test_true = y_test_true.astype(test_class_pred.dtype)

        metrics_to_compare = self.params["metrics"]
        test_results = []
        for metric in metrics_to_compare:
            metric_fn = self.default_metrics[metric]

            train_score = metric_fn(y_train_true, train_class_pred)
            test_score = metric_fn(y_test_true, test_class_pred)
            degradation = (train_score - test_score) / train_score

            passed = degradation < self.params["max_threshold"]
            test_results.append(
                TestResult(
                    test_name=metric,
                    passed=passed,
                    values={
                        "test_score": test_score,
                        "train_score": train_score,
                        "degradation": degradation,
                    },
                )
            )

        return self.cache_results(
            test_results, passed=all([r.passed for r in test_results])
        )
