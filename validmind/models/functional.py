# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from validmind.vm_models.model import VMModel


class FunctionalModel(VMModel):
    """
    FunctionalModel class wraps a user-defined predict function

    Attributes:
        predict_fn (callable): The predict function that should take a prompt as input
          and return the result from the model
        input_id (str, optional): The input ID for the model. Defaults to None.
        name (str, optional): The name of the model. Defaults to the name of the predict_fn.
    """

    def __post_init__(self):
        if not getattr(self, "predict_fn") or not callable(self.predict_fn):
            raise ValueError("FunctionalModel requires a callable predict_fn")

        self.name = self.name or self.predict_fn.__name__

    def predict(self, X, *args, **kwargs):
        return [
            (
                self.predict_fn(*x, *args, **kwargs)
                if isinstance(x, (list, tuple))
                else self.predict_fn(x, *args, **kwargs)
            )
            for x in X
        ]
