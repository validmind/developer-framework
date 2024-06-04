# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd


def DatasetSplitComparison(datasets):
    """
    Dataset Split Comparison
    """
    train_datasets, test_datasets = datasets
    description = []

    # Calculate the total size of all datasets
    total_train_size = sum(len(dataset.df) for dataset in train_datasets)
    total_test_size = sum(len(dataset.df) for dataset in test_datasets)
    total_size = total_train_size + total_test_size

    for dataset in train_datasets:
        dataset_size = len(dataset.df)
        proportion = dataset_size / total_size if total_size != 0 else 0

        metrics = {
            "Training Dataset": dataset.input_id,
            "Training Size": dataset_size,
            "Training Proportion": f"{proportion:.2%}",
            "Total Size": total_size,
        }

        description.append(metrics)

    for dataset in test_datasets:
        dataset_size = len(dataset.df)
        proportion = dataset_size / total_size if total_size != 0 else 0

        metrics = {
            "Test Dataset": dataset.input_id,
            "Test Size": dataset_size,
            "Test Proportion": f"{proportion:.2%}",
            "Total Size": total_size,
        }

        description.append(metrics)

    description_df = pd.DataFrame(description)

    return description_df
