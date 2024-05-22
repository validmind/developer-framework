# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Dataset class wrapper
"""

import warnings

import numpy as np
import pandas as pd
import polars as pl

from validmind.logging import get_logger
from validmind.models import FunctionModel, PipelineModel
from validmind.vm_models.model import VMModel

from .utils import ExtraColumns, as_df, compute_predictions, convert_index_to_datetime

logger = get_logger(__name__)


class VMDataset:
    """Base class for VM datasets

    Child classes should be used to support new dataset types (tensor, polars etc)
    by converting the user's dataset into a numpy array collecting metadata like
    column names and then call this (parent) class `__init__` method.

    This way we can support multiple dataset types but under the hood we only
    need to work with numpy arrays and pandas dataframes in this class.

    Attributes:
        raw_dataset (np.ndarray): The raw dataset as a NumPy array.
        input_id (str): Identifier for the dataset.
        index (np.ndarray): The raw dataset index as a NumPy array.
        columns (Set[str]): The column names of the dataset.
        target_column (str): The target column name of the dataset.
        feature_columns (List[str]): The feature column names of the dataset.
        feature_columns_numeric (List[str]): The numeric feature column names of the dataset.
        feature_columns_categorical (List[str]): The categorical feature column names of the dataset.
        text_column (str): The text column name of the dataset for NLP tasks.
        target_class_labels (Dict): The class labels for the target columns.
        df (pd.DataFrame): The dataset as a pandas DataFrame.
        extra_columns (Dict): Extra columns to include in the dataset.
    """

    def __init__(
        self,
        raw_dataset: np.ndarray,
        input_id: str = None,
        model: VMModel = None,
        index: np.ndarray = None,
        index_name: str = None,
        date_time_index: bool = False,
        columns: list = None,
        target_column: str = None,
        feature_columns: list = None,
        text_column: str = None,
        extra_columns: dict = None,
        target_class_labels: dict = None,
        options: dict = None,
    ):
        """
        Initializes a VMDataset instance.

        Args:
            raw_dataset (np.ndarray): The raw dataset as a NumPy array.
            input_id (str): Identifier for the dataset.
            model (VMModel): Model associated with the dataset.
            index (np.ndarray): The raw dataset index as a NumPy array.
            index_name (str): The raw dataset index name as a NumPy array.
            date_time_index (bool): Whether the index is a datetime index.
            columns (List[str], optional): The column names of the dataset. Defaults to None.
            target_column (str, optional): The target column name of the dataset. Defaults to None.
            feature_columns (str, optional): The feature column names of the dataset. Defaults to None.
            text_column (str, optional): The text column name of the dataset for nlp tasks. Defaults to None.
            target_class_labels (Dict, optional): The class labels for the target columns. Defaults to None.
            options (Dict, optional): Additional options for the dataset. Defaults to None.
        """
        # initialize input_id
        self.input_id = input_id

        # initialize raw dataset
        if not isinstance(raw_dataset, np.ndarray):
            raise ValueError("Expected Numpy array for attribute raw_dataset")
        self._raw_dataset = raw_dataset

        # initialize index and index name
        if index is not None and not isinstance(index, np.ndarray):
            raise ValueError("Expected Numpy array for attribute raw_dataset")
        self.index = index

        self.df = pd.DataFrame(self._raw_dataset, columns=columns).infer_objects()
        # set index to dataframe
        if index is not None:
            self.df.set_index(pd.Index(index), inplace=True)
            self.df.index.name = index_name
        # attempt to convert index to datatime
        if date_time_index:
            self.df = convert_index_to_datetime(self.df)

        self.options = options

        self.columns = columns or []
        self.column_aliases = {}
        self.target_column = target_column
        self.text_column = text_column
        self.target_class_labels = target_class_labels
        self.extra_columns = ExtraColumns.from_dict(extra_columns)
        self._set_feature_columns(feature_columns)

        if model:
            self.assign_predictions(model)

    def _set_feature_columns(self, feature_columns=None):
        if feature_columns is not None and (
            not isinstance(feature_columns, list)
            or not all(isinstance(col, str) for col in feature_columns)
        ):
            raise ValueError("Expected list of column names for `feature_columns`")

        if feature_columns:
            self.feature_columns = feature_columns
        else:
            excluded = [self.target_column, *self.extra_columns.flatten()]
            self.feature_columns = [col for col in self.columns if col not in excluded]

        self.feature_columns_numeric = (
            self.df[self.feature_columns]
            .select_dtypes(include=[np.number])
            .columns.tolist()
        )
        self.feature_columns_categorical = (
            self.df[self.feature_columns]
            .select_dtypes(include=[object, pd.Categorical])
            .columns.tolist()
        )

    def _add_column(self, column_name, column_values):
        if len(column_values) != len(self.df):
            raise ValueError(
                "Length of values doesn't match number of rows in the DataFrame."
            )

        self.columns.append(column_name)
        self.df[column_name] = column_values

    def _validate_assign_predictions(
        self,
        model: VMModel,
        prediction_column: str,
        prediction_values: list,
        probability_column: str,
        probability_values: list,
    ):
        if not isinstance(model, VMModel):
            raise ValueError("Expected VMModel instance for argument `model`")

        if prediction_column and prediction_values is not None:
            raise ValueError(
                "Only one of the following arguments can be provided: "
                "`prediction_column`, `prediction_values`"
            )

        if probability_column and probability_values is not None:
            raise ValueError(
                "Only one of the following arguments can be provided: "
                "`probability_column`, `probability_values`"
            )

        if prediction_column and prediction_column not in self.columns:
            raise ValueError(
                f"Prediction column {prediction_column} doesn't exist in the dataset"
            )

        if probability_column and probability_column not in self.columns:
            raise ValueError(
                f"Probability column {probability_column} doesn't exist in the dataset"
            )

        if (probability_column or probability_values is not None) and (
            not prediction_column and prediction_values is None
        ):
            raise ValueError(
                "Cannot use precomputed probabilities without precomputed predictions"
            )

    def assign_predictions(
        self,
        model: VMModel,
        prediction_column: str = None,
        prediction_values: list = None,
        probability_column: str = None,
        probability_values: list = None,
        prediction_probabilities: list = None,  # DEPRECATED: use probability_values
    ):
        if prediction_probabilities is not None:
            warnings.warn(
                "The `prediction_probabilities` argument is deprecated. Use `probability_values` instead.",
                DeprecationWarning,
            )
            probability_values = prediction_probabilities

        self._validate_assign_predictions(
            model,
            prediction_column,
            prediction_values,
            probability_column,
            probability_values,
        )

        if self.prediction_column(model):
            logger.warning("Model predictions already assigned... Overwriting.")

        if self.probability_column(model):
            logger.warning("Model probabilities already assigned... Overwriting.")

        # if the user passes a column name, we assume it has precomputed predictions
        if prediction_column:
            prediction_values = self.df[prediction_column].values

            if probability_column:
                probability_values = self.df[probability_column].values

        if prediction_values is None:
            X = self.df if isinstance(model, (FunctionModel, PipelineModel)) else self.x
            probability_values, prediction_values = compute_predictions(model, X)

        prediction_column = prediction_column or f"{model.input_id}_prediction"
        self._add_column(prediction_column, prediction_values)
        self.prediction_column(model, prediction_column)

        if probability_values is not None:
            probability_column = probability_column or f"{model.input_id}_probabilities"
            self._add_column(probability_column, probability_values)
            self.probability_column(model, probability_column)
        else:
            logger.info(
                "No probabilities computed or provided. "
                "Not adding probability column to the dataset."
            )

    def prediction_column(self, model: VMModel, column_name: str = None) -> str:
        """Get or set the prediction column for a model."""
        if column_name and column_name not in self.columns:
            raise ValueError("{column_name} doesn't exist in the dataset")

        if column_name and column_name in self.feature_columns:
            self.feature_columns.remove(column_name)

        return self.extra_columns.prediction_column(model, column_name)

    def probability_column(self, model: VMModel, column_name: str = None) -> str:
        """Get or set the probability column for a model."""
        if column_name and column_name not in self.columns:
            raise ValueError("{column_name} doesn't exist in the dataset")

        if column_name and column_name in self.feature_columns:
            self.feature_columns.remove(column_name)

        return self.extra_columns.probability_column(model, column_name)

    def add_extra_column(self, column_name, column_values=None):
        """Adds an extra column to the dataset without modifying the dataset `features` and `target` columns.

        Args:
            column_name (str): The name of the extra column.
            column_values (np.ndarray, optional): The values of the extra column.
        """
        if column_name not in self.columns and (
            column_values is None or len(column_values) == 0
        ):
            raise ValueError(
                "Column values must be provided when the column doesn't exist in the dataset"
            )

        # some warnings to let the user know what's happening
        if column_name in self.extra_columns:
            logger.warning(f"{column_name} is already an extra column. Overwriting...")
        elif column_name in self.columns and column_values:
            logger.warning(
                f"{column_name} already exists in the dataset but `column_values` were passed. Overwriting..."
            )

        self.extra_columns.extras.add(column_name)
        self._add_column(column_name, column_values)

        # reset feature columns to exclude the new extra column
        self._set_feature_columns()

        logger.info(
            f"Extra column {column_name} with {len(column_values)} values added to the dataset"
        )

    @property
    def x(self) -> np.ndarray:
        """
        Returns the input features (X) of the dataset.

        Returns:
            np.ndarray: The input features.
        """
        return self.df[self.feature_columns].to_numpy()

    @property
    def y(self) -> np.ndarray:
        """
        Returns the target variables (y) of the dataset.

        Returns:
            np.ndarray: The target variables.
        """
        return self.df[self.target_column].to_numpy()

    def y_pred(self, model) -> np.ndarray:
        """Returns the predictions for a given model.

        Attempts to stack complex prediction types (e.g., embeddings) into a single,
        multi-dimensional array.

        Args:
            model (VMModel): The model whose predictions are sought.

        Returns:
            np.ndarray: The predictions for the model
        """
        return np.stack(self.df[self.prediction_column(model)].values)

    def y_prob(self, model) -> np.ndarray:
        """Returns the probabilities for a given model.

        Args:
            model (str): The ID of the model whose predictions are sought.

        Returns:
            np.ndarray: The probability variables.
        """
        return self.df[self.probability_column(model)].values

    def x_df(self):
        """Returns a dataframe containing only the feature columns"""
        return as_df(self.df[self.feature_columns])

    def y_df(self) -> pd.DataFrame:
        """Returns a dataframe containing the target column"""
        return as_df(self.df[self.target_column])

    def y_pred_df(self, model) -> pd.DataFrame:
        """Returns a dataframe containing the predictions for a given model"""
        return as_df(self.df[self.prediction_column(model)])

    def y_prob_df(self, model) -> pd.DataFrame:
        """Returns a dataframe containing the probabilities for a given model"""
        return as_df(self.df[self.probability_column(model)])

    def target_classes(self):
        """Returns the unique number of target classes for the target (Y) variable"""
        return [str(i) for i in np.unique(self.y)]

    def __str__(self):
        return (
            f"=================\n"
            f"VMDataset object: \n"
            f"=================\n"
            f"Input ID: {self.input_id}\n"
            f"Target Column: {self.target_column}\n"
            f"Feature Columns: {self.feature_columns}\n"
            f"Text Column: {self.text_column}\n"
            f"Extra Columns: {self.extra_columns}\n"
            f"Target Class Labels: {self.target_class_labels}\n"
            f"Columns: {self.columns}\n"
            f"Index: {self.index}\n"
            f"=================\n"
        )


class DataFrameDataset(VMDataset):
    """
    VM dataset implementation for pandas DataFrame.
    """

    def __init__(
        self,
        raw_dataset: pd.DataFrame,
        input_id: str = None,
        model: VMModel = None,
        target_column: str = None,
        extra_columns: dict = None,
        feature_columns: list = None,
        text_column: str = None,
        target_class_labels: dict = None,
        options: dict = None,
        date_time_index: bool = False,
    ):
        """
        Initializes a DataFrameDataset instance.

        Args:
            raw_dataset (pd.DataFrame): The raw dataset as a pandas DataFrame.
            input_id (str, optional): Identifier for the dataset. Defaults to None.
            model (VMModel, optional): Model associated with the dataset. Defaults to None.
            target_column (str, optional): The target column of the dataset. Defaults to None.
            extra_columns (dict, optional): Extra columns to include in the dataset. Defaults to None.
            feature_columns (list, optional): The feature columns of the dataset. Defaults to None.
            text_column (str, optional): The text column name of the dataset for NLP tasks. Defaults to None.
            target_class_labels (dict, optional): The class labels for the target columns. Defaults to None.
            options (dict, optional): Additional options for the dataset. Defaults to None.
            date_time_index (bool, optional): Whether to use date-time index. Defaults to False.
        """
        index = None
        if isinstance(raw_dataset.index, pd.Index):
            index = raw_dataset.index.values

        super().__init__(
            raw_dataset=raw_dataset.values,
            input_id=input_id,
            model=model,
            index_name=raw_dataset.index.name,
            index=index,
            columns=raw_dataset.columns.to_list(),
            target_column=target_column,
            extra_columns=extra_columns,
            feature_columns=feature_columns,
            text_column=text_column,
            target_class_labels=target_class_labels,
            options=options,
            date_time_index=date_time_index,
        )


class PolarsDataset(VMDataset):
    """
    VM dataset implementation for Polars DataFrame.
    """

    def __init__(
        self,
        raw_dataset: pl.DataFrame,
        input_id: str = None,
        model: VMModel = None,
        target_column: str = None,
        extra_columns: dict = None,
        feature_columns: list = None,
        text_column: str = None,
        target_class_labels: dict = None,
        options: dict = None,
        date_time_index: bool = False,
    ):
        """
        Initializes a PolarsDataset instance.

        Args:
            raw_dataset (pl.DataFrame): The raw dataset as a Polars DataFrame.
            input_id (str, optional): Identifier for the dataset. Defaults to None.
            model (VMModel, optional): Model associated with the dataset. Defaults to None.
            target_column (str, optional): The target column of the dataset. Defaults to None.
            extra_columns (dict, optional): Extra columns to include in the dataset. Defaults to None.
            feature_columns (list, optional): The feature columns of the dataset. Defaults to None.
            text_column (str, optional): The text column name of the dataset for NLP tasks. Defaults to None.
            target_class_labels (dict, optional): The class labels for the target columns. Defaults to None.
            options (dict, optional): Additional options for the dataset. Defaults to None.
            date_time_index (bool, optional): Whether to use date-time index. Defaults to False.
        """
        super().__init__(
            raw_dataset=raw_dataset.to_numpy(),
            input_id=input_id,
            model=model,
            index_name=None,
            index=None,
            columns=raw_dataset.columns,
            target_column=target_column,
            extra_columns=extra_columns,
            feature_columns=feature_columns,
            text_column=text_column,
            target_class_labels=target_class_labels,
            options=options,
            date_time_index=date_time_index,
        )


class TorchDataset(VMDataset):
    """
    VM dataset implementation for PyTorch Datasets.
    """

    def __init__(
        self,
        raw_dataset,
        input_id: str = None,
        model: VMModel = None,
        index_name=None,
        index=None,
        columns=None,
        target_column: str = None,
        extra_columns: dict = None,
        feature_columns: list = None,
        text_column: str = None,
        target_class_labels: dict = None,
        options: dict = None,
    ):
        """
        Initializes a TorchDataset instance.

        Args:
            raw_dataset (torch.utils.data.Dataset): The raw dataset as a PyTorch Dataset.
            index_name (str): The raw dataset index name.
            index (np.ndarray): The raw dataset index as a NumPy array.
            columns (List[str]): The column names of the dataset.
            target_column (str, optional): The target column of the dataset. Defaults to None.
            feature_columns (list, optional): The feature columns of the dataset. Defaults to None.
            text_column (str, optional): The text column name of the dataset for nlp tasks. Defaults to None.
            target_class_labels (Dict, optional): The class labels for the target columns. Defaults to None.
        """

        try:
            import torch
        except ImportError:
            raise ImportError(
                "PyTorch is not installed, please run `pip install validmind[pytorch]`"
            )

        columns = []

        for id, tens in zip(range(0, len(raw_dataset.tensors)), raw_dataset.tensors):
            if id == 0 and feature_columns is None:
                n_cols = tens.shape[1]
                feature_columns = [
                    "x" + feature_id
                    for feature_id in np.linspace(
                        0, n_cols - 1, num=n_cols, dtype=int
                    ).astype(str)
                ]
                columns.append(feature_columns)

            elif id == 1 and target_column is None:
                target_column = "y"
                columns.append(target_column)

            elif id == 2 and extra_columns is None:
                extra_columns.prediction_column = "y_pred"
                columns.append(extra_columns.prediction_column)

        merged_tensors = torch.cat(raw_dataset.tensors, dim=1).numpy()

        super().__init__(
            input_id=input_id,
            raw_dataset=merged_tensors,
            model=model,
            index_name=index_name,
            index=index,
            columns=columns,
            target_column=target_column,
            feature_columns=feature_columns,
            text_column=text_column,
            extra_columns=extra_columns,
            target_class_labels=target_class_labels,
            options=options,
        )
