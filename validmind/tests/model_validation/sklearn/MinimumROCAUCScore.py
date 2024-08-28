# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
from sklearn import metrics, preprocessing

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class MinimumROCAUCScore(ThresholdTest):
    """
    Validates model by checking if the ROC AUC score meets or surpasses a specified threshold.

    ### Purpose

    The Minimum ROC AUC Score test is used to determine the model's performance by ensuring that the Receiver Operating
    Characteristic Area Under the Curve (ROC AUC) score on the validation dataset meets or exceeds a predefined
    threshold. The ROC AUC score indicates how well the model can distinguish between different classes, making it a
    crucial measure in binary and multiclass classification tasks.

    ### Test Mechanism

    This test implementation calculates the multiclass ROC AUC score on the true target values and the model's
    predictions. The test converts the multi-class target variables into binary format using `LabelBinarizer` before
    computing the score. If this ROC AUC score is higher than the predefined threshold (defaulted to 0.5), the test
    passes; otherwise, it fails. The results, including the ROC AUC score, the threshold, and whether the test passed
    or failed, are then stored in a `ThresholdTestResult` object.

    ### Signs of High Risk

    - A high risk or failure in the model's performance as related to this metric would be represented by a low ROC AUC
    score, specifically any score lower than the predefined minimum threshold. This suggests that the model is
    struggling to distinguish between different classes effectively.

    ### Strengths

    - The test considers both the true positive rate and false positive rate, providing a comprehensive performance
    measure.
    - ROC AUC score is threshold-independent meaning it measures the model's quality across various classification
    thresholds.
    - Works robustly with binary as well as multi-class classification problems.

    ### Limitations

    - ROC AUC may not be useful if the class distribution is highly imbalanced; it could perform well in terms of AUC
    but still fail to predict the minority class.
    - The test does not provide insight into what specific aspects of the model are causing poor performance if the ROC
    AUC score is unsatisfactory.
    - The use of macro average for multiclass ROC AUC score implies equal weightage to each class, which might not be
    appropriate if the classes are imbalanced.
    """

    name = "roc_auc_score"
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
        The roc auc score test returns results like these:
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
                    metadata=ResultTableMetadata(title="Minimum ROC AUC Score Test"),
                )
            ]
        )

    def multiclass_roc_auc_score(self, y_test, y_pred, average="macro"):
        lb = preprocessing.LabelBinarizer()
        lb.fit(y_test)
        y_test = lb.transform(y_test)
        y_pred = lb.transform(y_pred)
        return metrics.roc_auc_score(y_test, y_pred, average=average)

    def run(self):
        y_true = self.inputs.dataset.y

        if len(np.unique(y_true)) > 2:
            class_pred = self.inputs.dataset.y_pred(self.inputs.model)
            y_true = y_true.astype(class_pred.dtype)
            roc_auc = self.multiclass_roc_auc_score(y_true, class_pred)
        else:
            y_prob = self.inputs.dataset.y_prob(self.inputs.model)
            y_true = y_true.astype(y_prob.dtype).flatten()
            roc_auc = metrics.roc_auc_score(y_true, y_prob)

        passed = roc_auc > self.params["min_threshold"]
        results = [
            ThresholdTestResult(
                passed=passed,
                values={
                    "score": roc_auc,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))
