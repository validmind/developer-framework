# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import sklearn.metrics as metrics

from validmind.vm_models import UnitMetric


@dataclass
class AdjustedRSquaredScore(UnitMetric):
    required_inputs = ["dataset", "model"]

    def run(self):
        y_true = self.inputs.dataset.y
        y_pred = self.inputs.dataset.y_pred(model_id=self.inputs.model.input_id)

        X_columns = self.inputs.dataset.get_features_columns()
        row_count = len(y_true)
        feature_count = len(X_columns)
        value = 1 - (1 - metrics.r2_score(y_true, y_pred)) * (row_count - 1) / (
            row_count - feature_count
        )

        return self.cache_results(metric_value=value)
