# This software is proprietary and confidential. Unauthorized copying,
# modification, distribution or use of this software is strictly prohibited.
# Please refer to the LICENSE file in the root directory of this repository
# for more information.
#
# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List
import numpy as np

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
class MinimumF1Score(ThresholdTest):
    """
    Test that the model's F1 score on the validation dataset meets or
    exceeds a predefined threshold.
    """

    category = "model_performance"
    name = "f1_score"
    required_context = ["model"]
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
        if self.model.is_pytorch_model:
            import torch
        if (
            self.model.device_type
            and self.model.is_pytorch_model
            and not self.model.device_type == "gpu"
        ):

            y_true = np.array(torch.tensor(self.model.test_ds.y).cpu())
        else:
            y_true = np.array(self.model.test_ds.y)

        class_pred = self.model.y_test_predict
        y_true = y_true.astype(class_pred.dtype)

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
