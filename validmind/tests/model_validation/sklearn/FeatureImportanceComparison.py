# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd
from sklearn.inspection import permutation_importance


def FeatureImportanceComparison(datasets, models, num_features=3):
    """
    Feature Importance Comparison
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
                result[f"Feature {i + 1}"] = (
                    f"[{top_features[i][0]}; {top_features[i][1]:.4f}]"
                )
            else:
                result[f"Feature {i + 1}"] = None

        # Append the result to the list
        results_list.append(result)

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results_list)
    return results_df
