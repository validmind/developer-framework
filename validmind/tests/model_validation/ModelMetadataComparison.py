# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd
from validmind.utils import get_model_info


def ModelMetadataComparison(models):
    """
    Model Metadata Comparison
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
