# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd

from validmind.vm_models.model import ModelAttributes

from .sklearn import SKlearnModel


class StatsModelsModel(SKlearnModel):
    """
    An Statsmodels model class that wraps a trained model instance and its associated data.

    Attributes:
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
        model (object, optional): The trained model instance. Defaults to None.
        device_type(str, optional) The device where model is trained
    """

    def __init__(
        self,
        model: object = None,  # Trained model instance
        input_id: str = None,
        attributes: ModelAttributes = None,
    ):
        super().__init__(
            model=model,
            input_id=input_id,
            attributes=attributes,
        )

    def model_class(self):
        """
        Returns the model class name
        """
        return "statsmodels"

    def regression_coefficients(self):
        """
        Returns the regression coefficients summary of the model
        """
        raw_summary = self.model.summary()

        table = raw_summary.tables[1].data
        headers = table.pop(0)
        headers[0] = "Feature"

        return pd.DataFrame(table, columns=headers)
