# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from sklearn.metrics import roc_auc_score

from validmind.vm_models import UnitMetric


@dataclass
class ROC_AUC(UnitMetric):
    def __init__(
        self,
        inputs=None,
        metric_id=None,
        params=None,
        test_id="ROC_AUC Test",
    ):
        # Pass test_id and any other necessary parameters to the superclass
        super().__init__(
            test_id=test_id,
        )

        self.metric_id = metric_id
        self.metric_inputs = inputs
        self.params = params if params is not None else {}

    def run(self):
        y_true = self.metric_inputs["dataset"].y
        y_pred = self.metric_inputs["dataset"].y_pred(
            model_id=self.metric_inputs["model"].input_id
        )

        value = roc_auc_score(y_true, y_pred, **self.params)

        return self.cache_results(metric_value=value)
