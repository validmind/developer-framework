# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np

from validmind.vm_models import UnitMetric


@dataclass
class MeanAbsolutePercentageError(UnitMetric):

    required_inputs = ["dataset", "model"]

    def run(self):
        y_true = self.inputs.dataset.y
        y_pred = self.inputs.dataset.y_pred(model_id=self.inputs.model.input_id)

        value = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

        return self.cache_results(metric_value=value)
