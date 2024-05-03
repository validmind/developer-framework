# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from inspect import signature

import pandas as pd

from validmind.vm_models.model import VMModel


def get_getter(col, default=None):
    def getter(row):
        if col in row:
            return row[col]

        if not default:
            raise ValueError(f"Column `{col}` not found in input dataframe")

        return default

    return getter


class FunctionModel(VMModel):
    """
    FunctionModel class wraps a user-defined predict function

    Attributes:
        predict_fn (callable): The predict function that should take a prompt as input
          and return the result from the model
        predict_args (dict, optional): A dictionary where the keys are the arguments for
          the predict function and the values are either a string or a function. If a string,
          the column matching the string will be passed as the argument. If its a function,
          the function will be called with the row of the input dataframe as the argument
          and the return value of this function will be passed to `predict_fn`. If not provided,
          the names of the arguments of `predict_fn` will be used to match a column in the
          input dataframe.
        predict_col (str, optional): The output column name where predictions are stored.
          Defaults to the `input_id` plus `_prediction`.
        input_id (str, optional): The input ID for the model. Defaults to None.
        name (str, optional): The name of the model. Defaults to the name of the predict_fn.
    """

    predict_args: dict = None
    _predict_args: dict = None  # internal copy where values noramlized to all functions

    def __post_init__(self):
        if not getattr(self, "predict_fn") or not callable(self.predict_fn):
            raise ValueError("FunctionModel requires a callable predict_fn")

        self.name = self.name or self.predict_fn.__name__
        self._predict_args = self._build_predict_args()

    def _build_predict_args(self) -> dict:
        # infer from signature of predict_fn - keys of dict will be argument names
        # if an arg has no default, then value will just be the arg name
        # if an arg has a default, then value will be a lambda that returns
        # the column if it exists, else the default value from the signature

        col_map = {}

        # attempt to infer the arguments from the signature of the predict_fn
        for param in signature(self.predict_fn).parameters.values():
            if param.default is param.empty:
                col_map[param.name] = get_getter(param.name)

            else:
                col_map[param.name] = get_getter(param.name, default=param.default)

        if not self.predict_args:
            return col_map

        # add any user-provided predict_args to the col_map
        for key, value in self.predict_args.items():
            if not callable(value):
                col_map[key] = get_getter(value)
            else:
                col_map[key] = value

        return col_map

    def _get_args(self, x):
        return {key: value(x) for key, value in self._predict_args.items()}

    def predict(self, X):
        if isinstance(X, pd.Series):
            X = X.to_frame()

        Y = []

        for x in X.to_dict(orient="records"):
            Y.append(self.predict_fn(**self._get_args(x)))

        return Y
