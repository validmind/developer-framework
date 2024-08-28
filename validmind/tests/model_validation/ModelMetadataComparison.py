# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd

from validmind import tags, tasks
from validmind.utils import get_model_info


@tags("model_training", "metadata")
@tasks("regression", "time_series_forecasting")
def ModelMetadataComparison(models):
    """
    Assesses the metadata of various models to ensure consistency and compatibility, which is essential for effective
    model deployment and management.

    ### Purpose

    The Model Metadata Comparison test is designed to assess and compare the metadata of different models. This
    includes comparing information such as the model's architecture, framework, framework version, and programming
    language to ensure consistency and identify potential issues in model documentation or management.

    ### Test Mechanism

    The test retrieves metadata for each model using the `get_model_info` function. It then renames the columns based
    on a predefined set of labels and compiles this information into a summary table. The key steps include:

    - Retrieving metadata for each model.
    - Renaming columns to align with standardized labels.
    - Compiling and presenting the information in a summary table for comparison.

    ### Signs of High Risk

    - Inconsistent or missing metadata across models, indicating potential issues in documentation or model management.
    - Significant differences in framework versions or programming languages, which could lead to integration and
    deployment challenges.

    ### Strengths

    - Provides a clear, standardized comparison of essential model metadata.
    - Facilitates easier interpretation and comparison by standardizing metadata labels.
    - Helps identify potential compatibility or consistency issues across different models.

    ### Limitations

    - Assumes the `get_model_info` function returns all necessary metadata fields.
    - Relies on the correctness and completeness of the metadata provided by each model.
    - Focuses on high-level metadata and does not include detailed parameter information.
    """
    column_labels = {
        "architecture": "Modeling Technique",
        "framework": "Modeling Framework",
        "framework_version": "Framework Version",
        "language": "Programming Language",
    }

    description = []

    for model in models:
        model_info = get_model_info(model)

        # Rename columns based on provided labels
        model_info_renamed = {
            column_labels.get(k, k): v for k, v in model_info.items() if k != "params"
        }

        # Add model name or identifier if available
        model_info_renamed = {"Model Name": model.input_id, **model_info_renamed}

        description.append(model_info_renamed)

    description_df = pd.DataFrame(description)

    return description_df
