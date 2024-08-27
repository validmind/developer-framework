# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

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
    Checks if the model's prediction accuracy meets or surpasses a specified threshold.

    ### Purpose

    The Minimum Accuracy test’s objective is to verify whether the model's prediction accuracy on a specific dataset
    meets or surpasses a predetermined minimum threshold. Accuracy, which is simply the ratio of correct predictions to
    total predictions, is a key metric for evaluating the model's performance. Considering binary as well as multiclass
    classifications, accurate labeling becomes indispensable.

    ### Test Mechanism

    The test mechanism involves contrasting the model's accuracy score with a preset minimum threshold value, with the
    default being 0.7. The accuracy score is computed utilizing sklearn’s `accuracy_score` method, where the true
    labels `y_true` and predicted labels `class_pred` are compared. If the accuracy score is above the threshold, the
    test receives a passing mark. The test returns the result along with the accuracy score and threshold used for the
    test.

    ### Signs of High Risk

    - Model fails to achieve or surpass the predefined score threshold.
    - Persistent scores below the threshold, indicating a high risk of inaccurate predictions.

    ### Strengths

    - Simplicity, presenting a straightforward measure of holistic model performance across all classes.
    - Particularly advantageous when classes are balanced.
    - Versatile, as it can be implemented on both binary and multiclass classification tasks.

    ### Limitations

    - Misleading accuracy scores when classes in the dataset are highly imbalanced.
    - Favoritism towards the majority class, giving an inaccurate perception of model performance.
    - Inability to measure the model's precision, recall, or capacity to manage false positives or false negatives.
    - Focused on overall correctness and may not be sufficient for all types of model analytics.
    """

    name = "accuracy_score"
    required_inputs = ["model", "dataset"]
    default_params = {"min_threshold": 0.7}
    tasks = ["classification", "text_classification"]
    tags = [
        "sklearn",
        "binary_classification",
        "multiclass_classification",
        "model_performance",
    ]

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
        y_true = self.inputs.dataset.y
        class_pred = self.inputs.dataset.y_pred(self.inputs.model)
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

    def test(self):
        # Test that there is a result and it's not None
        assert self.result is not None
        # Test that results are contained in a list
        assert isinstance(self.result.test_results.results, list)
        # Verify that there is exactly one result
        assert len(self.result.test_results.results) == 1
        # Extract the single result for clarity
        test_result = self.result.test_results.results[0]
        # Check the 'passed' condition logic against the test outcome
        assert test_result.passed == (
            test_result.values["score"] >= test_result.values["threshold"]
        )
