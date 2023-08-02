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
