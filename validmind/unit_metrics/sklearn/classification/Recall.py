# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from sklearn.metrics import recall_score

from validmind.vm_models import UnitMetric


@dataclass
class Recall(UnitMetric):
    def run(self):
        y_true = self.inputs.dataset.y
        y_pred = self.inputs.dataset.y_pred(model_id=self.inputs.model.input_id)

        value = recall_score(y_true, y_pred, **self.params)

        return self.cache_results(metric_value=value)