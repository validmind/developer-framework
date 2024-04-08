# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np

from validmind.vm_models import UnitMetric


@dataclass
class KolmogorovSmirnovStatistic(UnitMetric):

    required_inputs = ["dataset", "model"]

    def run(self):
        y_true = self.inputs.dataset.y.flatten()
        y_pred = self.inputs.dataset.y_pred(model_id=self.inputs.model.input_id)

        # Sort true values and corresponding predicted values
        idx_true = np.argsort(y_true)
        idx_pred = np.argsort(y_pred)
        y_true_sorted = y_true[idx_true]
        y_pred_sorted = y_pred[idx_pred]

        # Compute cumulative distribution functions (CDFs)
        cdf_true = np.arange(1, len(y_true_sorted) + 1) / len(y_true_sorted)
        cdf_pred = np.arange(1, len(y_pred_sorted) + 1) / len(y_pred_sorted)

        # Compute absolute differences between CDFs
        diff_cdf = np.abs(cdf_true - cdf_pred)

        # Find maximum absolute difference
        ks_statistic = np.max(diff_cdf)

        return self.cache_results(metric_value=ks_statistic)
