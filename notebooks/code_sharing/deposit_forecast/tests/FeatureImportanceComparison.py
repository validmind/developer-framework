# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial


import pandas as pd
from sklearn.inspection import permutation_importance


def FeatureImportanceComparison(datasets, models):
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
        pfi = {}
        for i, column in enumerate(x.columns):
            pfi[column] = pfi_values["importances_mean"][i]

        # Sort features by their importance
        sorted_features = sorted(pfi.items(), key=lambda item: item[1], reverse=True)

        # Extract the top 4 features
        top_features = sorted_features[:4]

        # Prepare the result for the current model and dataset
        result = {
            "Model": model.input_id,
            "Dataset": dataset.input_id,
            "First Feature": (
                f"[{top_features[0][0]}; {top_features[0][1]:.4f}]"
                if len(top_features) > 0
                else None
            ),
            "Second Feature": (
                f"[{top_features[1][0]}; {top_features[1][1]:.4f}]"
                if len(top_features) > 1
                else None
            ),
            "Third Feature": (
                f"[{top_features[2][0]}; {top_features[2][1]:.4f}]"
                if len(top_features) > 2
                else None
            ),
            "Fourth Feature": (
                f"[{top_features[3][0]}; {top_features[3][1]:.4f}]"
                if len(top_features) > 3
                else None
            ),
        }

        # Append the result to the list
        results_list.append(result)

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results_list)
    return results_df
