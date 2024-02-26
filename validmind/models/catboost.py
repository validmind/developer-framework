# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from validmind.vm_models.model import ModelAttributes

from .sklearn import SKlearnModel


class CatBoostModel(SKlearnModel):
    """
    An CatBoost model class that wraps a trained model instance and its associated data.

    Attributes:
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
        model (object, optional): The trained model instance. Defaults to None.
        device_type(str, optional) The device where model is trained
    """

    def __init__(
        self,
        input_id: str = None,
        model: object = None,  # Trained model instance
        attributes: ModelAttributes = None,
    ):
        """
        Initialize CatBoostModel
        """
        super().__init__(
            input_id=input_id,
            model=model,
            attributes=attributes,
        )
