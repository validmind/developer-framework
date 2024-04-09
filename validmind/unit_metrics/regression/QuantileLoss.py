# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np

from validmind.vm_models import UnitMetric


@dataclass
class QuantileLoss(UnitMetric):
    required_inputs = ["dataset", "model"]

    def run(self):
        y_true = self.inputs.dataset.y
        y_pred = self.inputs.dataset.y_pred(model_id=self.inputs.model.input_id)

        error = y_true - y_pred
        # Quantile value (between 0 and 1).
        quantile = 0.5
        value = np.mean(np.maximum(quantile * error, (quantile - 1) * error))

        return self.cache_results(metric_value=value)
