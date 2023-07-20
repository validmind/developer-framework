# This software is proprietary and confidential. Unauthorized copying,
# modification, distribution or use of this software is strictly prohibited.
# Please refer to the LICENSE file in the root directory of this repository
# for more information.
#
# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
from sklearn.metrics import r2_score


def adj_r2_score(
    actual: np.ndarray, predicted: np.ndarray, rowcount: int, featurecount: int
):
    """
    Adjusted R2 Score
    """
    return 1 - (1 - r2_score(actual, predicted)) * (rowcount - 1) / (
        rowcount - featurecount
    )
