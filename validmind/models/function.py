# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from validmind.vm_models.model import VMModel


# semi-immutable dict
class Input(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._new = set()

    def __setitem__(self, key, value):
        self._new.add(key)
        super().__setitem__(key, value)

    def __delitem__(self, _):
        raise TypeError("Cannot delete keys from Input")

    def get_new(self):
        return {k: self[k] for k in self._new}


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

    def predict(self, X, return_alias=False):
        """Compute predictions for the input (X)

        Args:
            X (pandas.DataFrame): The input features to predict on
            return_alias (bool, optional): Whether to return the alias for the predictions.
                Defaults to False to be consistent with most "predict" methods.

        Returns:
            list: The predictions
        """
        Y = []

        for x in X.to_dict(orient="records"):
            # if any value in x is a dictionary, "spread" it as a new key
            for v in list(x.values()):
                if isinstance(v, dict):
                    x.update(v)

            input = Input(x)
            output = self.predict_fn(input)

            if input != output:
                raise ValueError(
                    "FunctionModel `predict_fn` must return the input dictionary"
                )

            Y.append(output.get_new())

        # if return_alias:
        #     return alias, Y

        return Y
