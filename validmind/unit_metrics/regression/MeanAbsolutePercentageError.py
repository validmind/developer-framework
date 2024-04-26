# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import numpy as np

from validmind import tags, tasks


@tags("regression", "unit_metric")
@tasks("regression")
def MeanAbsolutePercentageError(model, dataset):
    y_true = dataset.y
    y_pred = dataset.y_pred(model)

    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
