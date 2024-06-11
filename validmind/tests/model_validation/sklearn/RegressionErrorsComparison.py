# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import numpy as np
import pandas as pd
from sklearn import metrics

from validmind.logging import get_logger

logger = get_logger(__name__)


def RegressionErrorsComparison(datasets, models):
    """
    Regression Errors Comparison
    """
    results_list = []

    for dataset, model in zip(datasets, models):
        dataset_name = dataset.input_id
        model_name = model.input_id

        y_true = dataset.y
        y_pred = dataset.y_pred(model)  # Assuming dataset has X for features
        y_true = y_true.astype(y_pred.dtype)

        mae = metrics.mean_absolute_error(y_true, y_pred)
        mse = metrics.mean_squared_error(y_true, y_pred)

        if np.any(y_true == 0):
            logger.warning(
                "y_true contains zero values. Skipping MAPE calculation to avoid division by zero."
            )
            mape = None
        else:
            mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        mbd = np.mean(y_pred - y_true)

        # Append results to the list
        results_list.append(
            {
                "Model": model_name,
                "Dataset": dataset_name,
                "Mean Absolute Error (MAE)": mae,
                "Mean Squared Error (MSE)": mse,
                "Mean Absolute Percentage Error (MAPE)": mape,
                "Mean Bias Deviation (MBD)": mbd,
            }
        )

    # Convert results list to a DataFrame
    results_df = pd.DataFrame(results_list)
    return results_df
