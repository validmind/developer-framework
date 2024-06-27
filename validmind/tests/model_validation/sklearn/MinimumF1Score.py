# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from typing import List

import pandas as pd
from numpy import unique
from sklearn import metrics

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class MinimumF1Score(ThresholdTest):
    """
    Evaluates if the model's F1 score on the validation set meets a predefined minimum threshold.

    **Purpose:**
    The main objective of this test is to ensure that the F1 score, a balanced measure of precision and recall, of the
    model meets or surpasses a predefined threshold on the validation dataset. The F1 score is highly useful for
    gauging model performance in classification tasks, especially in cases where the distribution of positive and
    negative classes is skewed.

    **Test Mechanism:**
    The F1 score for the validation dataset is computed through the scikit-learn's metrics in Python. The scoring
    mechanism differs based on the classification problem: for multi-class problems, macro averaging is used (metrics
    are calculated separately and their unweighted mean is found), and for binary classification, the built-in f1_score
    calculation is used. The obtained F1 score is then assessed against the predefined minimum F1 score that is
    expected from the model.

    **Signs of High Risk:**

    - If a model returns an F1 score that is less than the established threshold, it is regarded as high risk.
    - A low F1 score might suggest that the model is not finding an optimal balance between precision and recall, see:
    it isn't successfully identifying positive classes while minimizing false positives.

    **Strengths:**

    - This metric gives a balanced measure of a model's performance by accounting for both false positives and false
    negatives.
    - It has a particular advantage in scenarios with imbalanced class distribution, where an accuracy measure can be
    misleading.
    - The flexibility of setting the threshold value allows for tailoring the minimum acceptable performance.

    **Limitations:**

    - The testing method may not be suitable for all types of models and machine learning tasks.
    - Although the F1 score gives a balanced view of a model's performance, it presupposes an equal cost for false
    positives and false negatives, which may not always be true in certain real-world scenarios. As a consequence,
    practitioners might have to rely on other metrics such as precision, recall, or the ROC-AUC score that align more
    closely with their specific requirements.
    """

    name = "f1_score"
    required_inputs = ["model", "dataset"]
    default_params = {"min_threshold": 0.5}
    tasks = ["classification", "text_classification"]
    tags = [
        "sklearn",
        "binary_classification",
        "multiclass_classification",
        "model_performance",
    ]

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
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
        y_true = self.inputs.dataset.y
        class_pred = self.inputs.dataset.y_pred(self.inputs.model)
        y_true = y_true.astype(class_pred.dtype)

        if len(unique(y_true)) > 2:
            f1_score = metrics.f1_score(y_true, class_pred, average="macro")
        else:
            f1_score = metrics.f1_score(y_true, class_pred)

        passed = f1_score > self.params["min_threshold"]
        results = [
            ThresholdTestResult(
                passed=passed,
                values={
                    "score": f1_score,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))
