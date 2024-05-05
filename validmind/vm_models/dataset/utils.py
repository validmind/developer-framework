# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass, field
from typing import Dict, List, Set, Union

import numpy as np
import pandas as pd

from validmind.errors import MissingOrInvalidModelPredictFnError
from validmind.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ExtraColumns:
    """Extra columns for the dataset."""

    extras: Set[str] = field(default_factory=set)
    group_by_column: str = None
    prediction_columns: Dict[str, str] = field(default_factory=dict)
    probability_columns: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            extras=set(
                [
                    k
                    for k in data.keys()
                    if k not in ["group_by", "predictions", "probabilities"]
                ]
            ),
            group_by_column=data.get("group_by"),
            prediction_columns=data.get("predictions", {}),
            probability_columns=data.get("probabilities", {}),
        )

    # mimic dictionary behaviour but only for the extras
    def __contains__(self, key):
        return key in self.flatten()

    def flatten(self) -> List[str]:
        """Get a list of all column names"""
        return [
            self.group_by_column,
            *self.extras,
            *self.prediction_columns.values(),
            *self.probability_columns.values(),
        ]

    def prediction_column(self, model, column_name: str = None) -> str:
        """Get or set the prediction column for a model."""
        if column_name:
            self.prediction_columns[model.input_id] = column_name
            return column_name

        try:
            return self.prediction_columns[model.input_id]
        except KeyError:
            raise ValueError(f"No prediction column found for model {model.input_id}")

    def probability_column(self, model, column_name: str = None) -> str:
        """Get or set the probability column for a model."""
        if column_name:
            self.probability_columns[model.input_id] = column_name
            return column_name

        try:
            return self.probability_columns[model.input_id]
        except KeyError:
            raise ValueError(f"No probability column found for model {model.input_id}")


def is_probabilties(output):
    """Check if the output from the predict method is probabilities."""
    # This is a simple check that assumes output is probabilities if they lie between 0 and 1
    if np.all((output >= 0) & (output <= 1)):
        # Check if there is at least one element that is neither 0 nor 1
        if np.any((output > 0) & (output < 1)):
            return True
    return np.all((output >= 0) & (output <= 1)) and np.any((output > 0) & (output < 1))


def as_df(series_or_frame: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
    if isinstance(series_or_frame, pd.Series):
        return series_or_frame.to_frame()
    return series_or_frame


def compute_predictions(model, X) -> tuple:
    try:
        # call predict_proba() to raise if not implemented
        model.predict_proba()
        logger.info("Running predict_proba()... This may take a while")
        probability_values = np.array(model.predict_proba(X))
        logger.info("Done running predict_proba()...")
    except MissingOrInvalidModelPredictFnError:
        # if not predict_proba() then its likely a regression model or a classification
        # model that doesn't support predict_proba()
        pass
    try:
        logger.info("Running predict()... This may take a while")
        prediction_values = np.array(model.predict(X))
        logger.info("Done running predict()...")
    except MissingOrInvalidModelPredictFnError:
        raise TypeError(
            "Cannot compute predictions for model's that don't support inference. "
            "You can pass `prediction_values` or `prediction_columns` to use precomputed predictions"
        )
    # TODO: this is really not ideal/robust and should not be handled by dataset class
    if not probability_values and is_probabilties(prediction_values):
        logger.info(
            "Predict method returned probabilities instead of direct labels or regression values. "
            "This implies the model is likely configured for a classification task with probability output."
        )
        threshold = 0.5
        logger.info(
            f"Converting probabilties to binary classes using thresholding with `{threshold=}`."
        )
        return prediction_values, (prediction_values > threshold).astype(int)
    return probability_values, prediction_values


def convert_index_to_datetime(df):
    """
    Attempts to convert the index of the dataset to a datetime index
    and leaves the index unchanged if it fails.
    """
    converted_index = pd.to_datetime(df.index, errors="coerce")

    # The conversion was successful if there are no NaT values
    if not converted_index.isnull().any():
        df.index = converted_index

    return df
