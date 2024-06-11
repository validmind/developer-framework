# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd
from sklearn import metrics

from validmind.tests.model_validation.statsmodels.statsutils import adj_r2_score


def RegressionR2SquareComparison(datasets, models):
    """
    Regression R2 Square Comparison
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
