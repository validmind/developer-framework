# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from sklearn.metrics import r2_score as _r2_score

from validmind import tags, tasks


@tags("regression", "sklearn", "unit_metric")
@tasks("regression")
def AdjustedRSquaredScore(model, dataset):
    r2_score = _r2_score(
        dataset.y,
        dataset.y_pred(model),
    )

    row_count = len(dataset.y)
    feature_count = len(dataset.get_features_columns())

    return 1 - (1 - r2_score) * (row_count - 1) / (row_count - feature_count)
