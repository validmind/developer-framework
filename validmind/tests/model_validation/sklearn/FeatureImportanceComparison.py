# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd
from sklearn.inspection import permutation_importance

from validmind import tags, tasks


@tags("model_explainability", "sklearn")
@tasks("regression", "time_series_forecasting")
def FeatureImportanceComparison(datasets, models, num_features=3):
    """
    Compare feature importance scores for each model and generate a summary table
    with the top important features.

    **Purpose**: The purpose of this function is to compare the feature importance scores for different models applied to various datasets.

    **Test Mechanism**: The function iterates through each dataset-model pair, calculates permutation feature importance (PFI) scores, and generates a summary table with the top `num_features` important features for each model.

    **Signs of High Risk**:
    - If key features expected to be important are ranked low, it could indicate potential issues with model training or data quality.
    - High variance in feature importance scores across different models may suggest instability in feature selection.

    **Strengths**:
    - Provides a clear comparison of the most important features for each model.
    - Uses permutation importance, which is a model-agnostic method and can be applied to any estimator.

    **Limitations**:
    - Assumes that the dataset is provided as a DataFrameDataset object with `x_df` and `y_df` methods to access feature and target data.
    - Requires that `model.model` is compatible with `sklearn.inspection.permutation_importance`.
    - The function's output is dependent on the number of features specified by `num_features`, which defaults to 3 but can be adjusted.


    """
    results_list = []

    for dataset, model in zip(datasets, models):
        x = dataset.x_df()
        y = dataset.y_df()

        pfi_values = permutation_importance(
            model.model,
            x,
            y,
            random_state=0,
            n_jobs=-2,
        )

        # Create a dictionary to store PFI scores
        pfi = {
            column: pfi_values["importances_mean"][i]
            for i, column in enumerate(x.columns)
        }

        # Sort features by their importance
        sorted_features = sorted(pfi.items(), key=lambda item: item[1], reverse=True)

        # Extract the top `num_features` features
        top_features = sorted_features[:num_features]

        # Prepare the result for the current model and dataset
        result = {
            "Model": model.input_id,
            "Dataset": dataset.input_id,
        }

        # Dynamically add feature columns to the result
        for i in range(num_features):
            if i < len(top_features):
                result[
                    f"Feature {i + 1}"
                ] = f"[{top_features[i][0]}; {top_features[i][1]:.4f}]"
            else:
                result[f"Feature {i + 1}"] = None

        # Append the result to the list
        results_list.append(result)

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results_list)
    return results_df
