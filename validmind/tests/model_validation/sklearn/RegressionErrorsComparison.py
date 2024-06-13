# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import numpy as np
import pandas as pd
from sklearn import metrics

from validmind import tags, tasks
from validmind.logging import get_logger

logger = get_logger(__name__)


@tags("model_performance", "sklearn")
@tasks("regression", "time_series_forecasting")
def RegressionErrorsComparison(datasets, models):
    """
    Compare regression error metrics for each model and generate a summary table
    with the results.

    **Purpose**: The purpose of this function is to compare the regression errors for different models applied to various datasets.

    **Test Mechanism**: The function iterates through each dataset-model pair, calculates various error metrics (MAE, MSE, MAPE, MBD), and generates a summary table with these results.

    **Signs of High Risk**:
    - High Mean Absolute Error (MAE) or Mean Squared Error (MSE) indicates poor model performance.
    - High Mean Absolute Percentage Error (MAPE) suggests large percentage errors, especially problematic if the true values are small.
    - Mean Bias Deviation (MBD) significantly different from zero indicates systematic overestimation or underestimation by the model.

    **Strengths**:
    - Provides multiple error metrics to assess model performance from different perspectives.
    - Includes a check to avoid division by zero when calculating MAPE.

    **Limitations**:
    - Assumes that the dataset is provided as a DataFrameDataset object with `y`, `y_pred`, and `feature_columns` attributes.
    - The function relies on the `logger` from `validmind.logging` to warn about zero values in `y_true`, which should be correctly implemented and imported.
    - Requires that `dataset.y_pred(model)` returns the predicted values for the model.
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
