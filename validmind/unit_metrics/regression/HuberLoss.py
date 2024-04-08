# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np

from validmind.vm_models import UnitMetric


@dataclass
class HuberLoss(UnitMetric):

    required_inputs = ["dataset", "model"]

    def run(self):
        y_true = self.inputs.dataset.y
        y_pred = self.inputs.dataset.y_pred(model_id=self.inputs.model.input_id)

        # delta - Threshold for the squared error to be linear or quadratic.
        delta = 1.0
        error = y_true - y_pred
        quadratic_part = np.minimum(np.abs(error), delta)
        linear_part = np.abs(error) - quadratic_part
        value = np.mean(0.5 * quadratic_part**2 + delta * linear_part)

        return self.cache_results(metric_value=value)
