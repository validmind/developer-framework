# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

import pandas as pd
from numpy import unique
from sklearn import metrics

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
)


@dataclass
class MinimumF1Score(ThresholdTest):
    """
    Test that the model's F1 score on the validation dataset meets or
    exceeds a predefined threshold.
    """

    category = "model_performance"
    name = "f1_score"
    required_inputs = ["model"]
    default_params = {"min_threshold": 0.5}

    def summary(self, results: List[TestResult], all_passed: bool):
        """
        The f1 score test returns results like these:
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
                    metadata=ResultTableMetadata(title="Minimum F1 Score Test"),
                )
            ]
        )

    def run(self):
        y_true = self.model.y_test_true
        class_pred = self.model.y_test_predict
        y_true = y_true.astype(class_pred.dtype)

        if len(unique(y_true)) > 2:
            f1_score = metrics.f1_score(y_true, class_pred, average="macro")
        else:
            f1_score = metrics.f1_score(y_true, class_pred)

        passed = f1_score > self.params["min_threshold"]
        results = [
            TestResult(
                passed=passed,
                values={
                    "score": f1_score,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))
