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
class Column(str):
    """Column class for the dataset."""

    name: str
    alias: str = None

    def __init__(self, name, alias=None):
        self.name = name
        self.alias = alias

    def __str__(self):
        return self.name

    @property
    def names(self):
        return [self.name, self.alias] if self.alias else [self.name]


@dataclass
class ExtraColumns:
    """Extra columns for the dataset."""

    extras: Set[Column] = field(default_factory=set)
    group_by_column: Column = None
    prediction_columns: Dict[str, Column] = field(default_factory=dict)
    probability_columns: Dict[str, Column] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return cls()

        return cls(
            extras=set(
                [
                    Column(k)
                    for k in data.keys()
                    if k not in ["group_by", "predictions", "probabilities"]
                ]
            ),
            group_by_column=Column(data["group_by"]) if "group_by" in data else None,
            prediction_columns=(
                {k: Column(v) for k, v in data.get("predictions", {}).items()}
                if "predictions" in data
                else {}
            ),
            probability_columns=(
                {k: Column(v) for k, v in data.get("probabilities", {}).items()}
                if "probabilities" in data
                else {}
            ),
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

    def add_extra(self, column_name: str, alias: str = None) -> Column:
        column = Column(column_name, alias)
        self.extras.add(column)

        return column

    def prediction_column(
        self, model, column_name: str = None, alias: str = None
    ) -> Column:
        """Get or set the prediction column for a model."""
        if column_name:
            self.prediction_columns[model.input_id] = Column(column_name, alias)

        if not column_name and alias:
            # add alias to the existing column
            self.prediction_columns[model.input_id].alias = alias

        return self.prediction_columns.get(model.input_id)

    def probability_column(
        self, model, column_name: str = None, alias: str = None
    ) -> Column:
        """Get or set the probability column for a model."""
        if column_name:
            self.probability_columns[model.input_id] = Column(column_name, alias)

        if not column_name and alias:
            # add alias to the existing column
            self.probability_columns[model.input_id].alias = alias

        return self.probability_columns.get(model.input_id)


def as_df(series_or_frame: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
    if isinstance(series_or_frame, pd.Series):
        return series_or_frame.to_frame()
    return series_or_frame


def _is_probabilties(output):
    """Check if the output from the predict method is probabilities."""
    if not isinstance(output, np.ndarray) or output.ndim > 1:
        return False

    # This is a simple check that assumes output is probabilities if they lie between 0 and 1
    if np.all((output >= 0) & (output <= 1)):
        # Check if there is at least one element that is neither 0 nor 1
        if np.any((output > 0) & (output < 1)):
            return True

    return np.all((output >= 0) & (output <= 1)) and np.any((output > 0) & (output < 1))


def compute_predictions(model, X) -> tuple:
    probability_values = None

    try:
        logger.info("Running predict_proba()... This may take a while")
        probability_values = model.predict_proba(X)
        logger.info("Done running predict_proba()...")
    except MissingOrInvalidModelPredictFnError:
        # if not predict_proba() then its likely a regression model or a classification
        # model that doesn't support predict_proba()
        pass

    try:
        logger.info("Running predict()... This may take a while")
        prediction_values = model.predict(X)
        logger.info("Done running predict()...")
    except MissingOrInvalidModelPredictFnError:
        raise MissingOrInvalidModelPredictFnError(
            "Cannot compute predictions for model's that don't support inference. "
            "You can pass `prediction_values` or `prediction_columns` to use precomputed predictions"
        )

    # TODO: this is really not ideal/robust and should not be handled by dataset class
    if probability_values is None and _is_probabilties(prediction_values):
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
