# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import numpy as np
from sklearn.metrics import mean_squared_error

from validmind import tags, tasks


@tags("regression")
@tasks("regression")
def RootMeanSquaredError(model, dataset, **kwargs):
    return np.sqrt(
        mean_squared_error(
            dataset.y,
            dataset.y_pred(model),
            **kwargs,
        )
    )
