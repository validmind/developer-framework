# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd
from sklearn import metrics

from validmind import tags, tasks
from validmind.tests.model_validation.statsmodels.statsutils import adj_r2_score


@tags("model_performance", "sklearn")
@tasks("regression", "time_series_forecasting")
def RegressionR2SquareComparison(datasets, models):
    """
    Compare R-Squared and Adjusted R-Squared values for each model and generate a summary table
    with the results.

    **Purpose**: The purpose of this function is to compare the R-Squared and Adjusted R-Squared values for different models applied to various datasets.

    **Test Mechanism**: The function iterates through each dataset-model pair, calculates the R-Squared and Adjusted R-Squared values, and generates a summary table with these results.

    **Signs of High Risk**:
    - If the R-Squared values are significantly low, it could indicate that the model is not explaining much of the variability in the dataset.
    - A significant difference between R-Squared and Adjusted R-Squared values might indicate that the model includes irrelevant features.

    **Strengths**:
    - Provides a quantitative measure of model performance in terms of variance explained.
    - Adjusted R-Squared accounts for the number of predictors, making it a more reliable measure when comparing models with different numbers of features.

    **Limitations**:
    - Assumes that the dataset is provided as a DataFrameDataset object with `y`, `y_pred`, and `feature_columns` attributes.
    - The function relies on `adj_r2_score` from the `statsmodels.statsutils` module, which should be correctly implemented and imported.
    - Requires that `dataset.y_pred(model)` returns the predicted values for the model.

    """
    results_list = []

    for dataset, model in zip(datasets, models):
        dataset_name = dataset.input_id
        model_name = model.input_id

        y_true = dataset.y
        y_pred = dataset.y_pred(model)  # Assuming dataset has X for features
        y_true = y_true.astype(y_pred.dtype)

        r2s = metrics.r2_score(y_true, y_pred)
        X_columns = dataset.feature_columns
        adj_r2 = adj_r2_score(y_true, y_pred, len(y_true), len(X_columns))

        # Append results to the list
        results_list.append(
            {
                "Model": model_name,
                "Dataset": dataset_name,
                "R-Squared": r2s,
                "Adjusted R-Squared": adj_r2,
            }
        )

    # Convert results list to a DataFrame
    results_df = pd.DataFrame(results_list)
    return results_df
