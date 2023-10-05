# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

import pandas as pd
from sklearn import metrics

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class MinimumAccuracy(ThresholdTest):
    """
    **Purpose**: The purpose of the Minimum Accuracy test is to validate that the model's prediction accuracy on a
    given dataset meets or exceeds a predefined minimum threshold. Accuracy is the fraction of predictions our model
    got right and is an essential metric to understand how well our model is performing. In the context of both binary
    and multiclass classifications, accurate labeling is crucial.

    **Test Mechanism**: The mechanism of this threshold test involves comparing the model's accuracy score against the
    minimum threshold value specified (default value is 0.7). The accuracy score is calculated by using the sklearn's
    `accuracy_score` method between true label `y_true` and predicted label `class_pred`. If the accuracy score exceeds
    the threshold, the test is marked as passed. The test result is returned along with the accuracy score and the
    threshold used for the test.

    **Signs of High Risk**: Signs of high risk within this test present themselves when the model is unable to meet or
    exceed the specified score threshold. If the model's accuracy score is consistently falling below the set
    threshold, it indicates a high risk of inaccurate predictions, which can reduce the model's effectiveness and
    dependability.

    **Strengths**: The strength of the Minimum Accuracy test lies in its simplicity. It provides a straightforward
    measure of overall model performance across all classes. It's particularly advantageous when the classes are
    balanced. The test is also versatile and can be used with both binary and multiclass classification tasks.

    **Limitations**: This test's limitations surface when dealing with imbalanced datasets. If the classes in the
    dataset are highly skewed, the accuracy score could be misleading, potentially favoring the majority class and
    providing a false sense of model performance. Another limitation is it does not provide a measure of the model's
    precision, recall, or ability to manage false positives and false negatives. It primarily focuses on overall
    correctness, which might not be sufficient for all types of model analytics.
    """

    category = "model_performance"
    name = "accuracy_score"
    required_inputs = ["model"]
    default_params = {"min_threshold": 0.7}
    metadata = {
        "task_types": ["classification", "text_classification"],
        "tags": [
            "sklearn",
            "binary_classification",
            "multiclass_classification",
            "model_performance",
        ],
    }

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
        """
        The accuracy score test returns results like these:
        [{"values": {"score": 0.734375, "threshold": 0.7}, "passed": true}]
        """
        result = results[0]
        results_table = [
            {
                "Score": result.values["score"],
                "Threshold": result.values["threshold"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pd.DataFrame(results_table),
                    metadata=ResultTableMetadata(
                        title="Minimum Accuracy Test on Test Data"
                    ),
                )
            ]
        )

    def run(self):
        y_true = self.model.y_test_true
        class_pred = self.model.y_test_predict
        y_true = y_true.astype(class_pred.dtype)

        accuracy_score = metrics.accuracy_score(y_true, class_pred)

        passed = accuracy_score > self.params["min_threshold"]
        results = [
            ThresholdTestResult(
                passed=passed,
                values={
                    "score": accuracy_score,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))
