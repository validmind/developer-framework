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
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class MinimumF1Score(ThresholdTest):
    """
    **Purpose**:
    The primary purpose of this test is to ensure that the model's F1 score - a balanced reflection of both precision
    and recall - meets or surpasses a predetermined threshold on the validation dataset. This F1 score is a valuable
    measure of model performance in classification tasks, particularly where the proportion of positive and negative
    classes is imbalanced.

    **Test Mechanism**:
    The model's F1 score is calculated for the validation dataset via python's scikit-learn metrics. The scoring
    differs according to the classification problem: for multi-class, it uses macro averaging (calculating metrics
    separately then finding their unweighted mean), and for binary classification, it uses inherent f1_score
    calculation. The computed F1 score is then compared against the predetermined threshold - a minimum F1 score the
    model is expected to achieve.

    **Signs of High Risk**:
    Any model that returns an F1 score lower than the set threshold is considered high risk. A low F1 score could
    indicate that the model is not striking a desirable balance between precision and recall, or in simpler terms, it
    is not doing well in correctly identifying positive classes and limiting false positives.

    **Strengths**:
    This metric provides the advantage of being a balanced measure of a model's performance by considering both false
    positives and false negatives. It is particularly useful in scenarios with imbalanced class distribution, where
    accuracy can be misleading. It also allows for customization of the minimum acceptable performance by setting the
    threshold value.

    **Limitations**:
    This testing method may not be appropriate for all types of models and machine learning tasks. Also, while the F1
    score captures a balanced view of a model's performance, it assumes equal cost for false positives and false
    negatives, which may not always be the case in certain real world scenarios. This limitation may compel
    practitioners to choose other metrics such as precision, recall, or the ROC-AUC score that align better with their
    specific needs.
    """

    category = "model_performance"
    name = "f1_score"
    required_inputs = ["model"]
    default_params = {"min_threshold": 0.5}
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
            ThresholdTestResult(
                passed=passed,
                values={
                    "score": f1_score,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))
