# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from validmind.vm_models.model import VMModel


class FunctionModel(VMModel):
    """
    FunctionModel class wraps a user-defined predict function

    Attributes:
        predict_fn (callable): The predict function that should take a dictionary of
            input features and return a prediction.
        input_id (str, optional): The input ID for the model. Defaults to None.
        name (str, optional): The name of the model. Defaults to the name of the predict_fn.
    """

    def __post_init__(self):
        if not getattr(self, "predict_fn") or not callable(self.predict_fn):
            raise ValueError("FunctionModel requires a callable predict_fn")

        self.name = self.name or self.predict_fn.__name__

    def predict(self, X):
        Y = []

        for x in X.to_dict(orient="records"):
            Y.append(self.predict_fn(x))

        return Y
