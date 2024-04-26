# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from sklearn.metrics import mean_absolute_error as _mean_absolute_error

from validmind import tags, tasks


@tags("regression", "sklearn", "unit_metric")
@tasks("regression")
def MeanAbsoluteError(model, dataset, **kwargs):
    return _mean_absolute_error(dataset.y, dataset.y_pred(model), **kwargs)
