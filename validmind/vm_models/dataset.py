# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Dataset class wrapper
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import pandas as pd

EXTRA_COLUMNS = {
    "prediction_column": None,
    "group_by_column": None,
}


@dataclass
class VMDataset(ABC):
    """
    Abstract base class for VM datasets.
    """

    input_id: str = None

    @property
    @abstractmethod
    def raw_dataset(self):
        """
        Returns the raw dataset.
        """
        pass

    @abstractmethod
    def serialize(self):
        """
        Serializes the dataset to a dictionary.
        """
        pass


@dataclass
class NumpyDataset(VMDataset):
    """
    VM dataset implementation for NumPy arrays.
    """

    _raw_dataset: np.ndarray = None
    _index: np.ndarray = None
    _index_name: str = None
    _columns: list = None
    _target_column: str = None
    _feature_columns: list = (None,)
    _text_column: str = None
    _type: str = "generic"
    _target_class_labels: dict = None
    _df: pd.DataFrame = None
    _extra_columns: dict = None

    def __init__(
        self,
        raw_dataset,
        index=None,
        index_name=None,
        date_time_index=False,
        columns=None,
        target_column: str = None,
        feature_columns: list = None,
        text_column=None,
        extra_columns: dict = EXTRA_COLUMNS.copy(),
        target_class_labels: dict = None,
        options: dict = None,
    ):
        """
        Initializes a NumpyDataset instance.

        Args:
            raw_dataset (np.ndarray): The raw dataset as a NumPy array.
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

        if not isinstance(raw_dataset, np.ndarray):
            raise ValueError("Expected Numpy array for attribute raw_dataset")
        self._raw_dataset = raw_dataset
        if index is not None and not isinstance(index, np.ndarray):
            raise ValueError("Expected Numpy array for attribute raw_dataset")
        self._index = index
        self._index_name = index_name

        self._columns = columns or []
        if not self._columns:
            df = pd.DataFrame(self._raw_dataset).infer_objects()
            self._columns = df.columns.to_list()
        else:
            df = pd.DataFrame(self._raw_dataset, columns=self._columns).infer_objects()

        self._target_column = target_column

        if extra_columns is None:
            self._extra_columns = EXTRA_COLUMNS.copy()
        else:
            self._extra_columns = extra_columns

        self.__set_feature_columns(feature_columns)

        self._text_column = text_column
        self._target_class_labels = target_class_labels
        self.options = options

        if index is not None:
            df.set_index(pd.Index(index), inplace=True)
            df.index.name = index_name

        if date_time_index:
            df = self.__attempt_convert_index_to_datetime(df)

        self._df = df

    def __set_feature_columns(self, feature_columns):
        extra_columns_list = list(self._extra_columns.values())

        if not feature_columns:
            self._feature_columns = [
                col
                for col in self._columns
                if col != self._target_column and col not in extra_columns_list
            ]
        else:
            if not isinstance(feature_columns, list):
                raise ValueError("Expected list for attribute feature_columns")
            self._feature_columns = feature_columns

    def __attempt_convert_index_to_datetime(self, df):
        """
        Attempts to convert the index of the dataset to a datetime index
        and leaves the index unchanged if it fails.
        """
        converted_index = pd.to_datetime(df.index, errors="coerce")

        # The conversion was successful if there are no NaT values
        if not converted_index.isnull().any():
            df.index = converted_index

        return df

    @property
    def raw_dataset(self) -> np.ndarray:
        """
        Returns the raw dataset.

        Returns:
            np.ndarray: The raw dataset.
        """
        return self._raw_dataset

    @property
    def index(self) -> np.ndarray:
        """
        Returns index of the dataset.

        Returns:
            np.ndarray: The dataset index.
        """
        return self._index

    @property
    def index_name(self) -> str:
        """
        Returns index name of the dataset.

        Returns:
            str: The dataset index name.
        """
        return self._df.index.name

    @property
    def columns(self) -> list:
        """
        Returns the the list of columns in the dataset.

        Returns:
            List[str]: The columns list.
        """
        return self._columns

    @property
    def target_column(self) -> str:
        """
        Returns the target column name of the dataset.

        Returns:
            str: The target column name.
        """
        return self._target_column

    @property
    def extra_columns(self) -> list:
        """
        Returns the list of extra columns of the dataset.

        Returns:
            str: The extra columns list.
        """
        return self._extra_columns

    @property
    def prediction_column(self) -> str:
        """
        Returns the prediction column name of the dataset.

        Returns:
            str: The prediction column name.
        """
        return self._extra_columns["prediction_column"]

    @property
    def group_by_column(self) -> str:
        """
        Returns the group by column name of the dataset.

        Returns:
            str: The group by column name.
        """
        return self._extra_columns["group_by_column"]

    @property
    def feature_columns(self) -> list:
        """
        Returns the feature columns of the dataset. If _feature_columns is None,
        it returns all columns except the target column.

        Returns:
            list: The list of feature column names.
        """
        if self._feature_columns is None:
            return self.get_features_columns()
        return self._feature_columns

    @property
    def text_column(self) -> str:
        """
        Returns the text column of the dataset.

        Returns:
            str: The text column name.
        """
        return self._text_column

    @property
    def x(self) -> np.ndarray:
        """
        Returns the input features (X) of the dataset.

        Returns:
            np.ndarray: The input features.
        """
        return self.raw_dataset[
            :,
            [
                self.columns.index(name)
                for name in self.columns
                if name in self.feature_columns
            ],
        ]

    @property
    def y(self) -> np.ndarray:
        """
        Returns the target variables (y) of the dataset.

        Returns:
            np.ndarray: The target variables.
        """
        return self.raw_dataset[
            :,
            [
                self.columns.index(name)
                for name in self.columns
                if name == self.target_column
            ],
        ]

    @property
    def y_pred(self) -> np.ndarray:
        """
        Returns the prediction variable (y_pred) of the dataset.

        Returns:
            np.ndarray: The prediction variables.
        """
        return self.raw_dataset[
            :,
            [
                self.columns.index(name)
                for name in self.columns
                if name == self.prediction_column
            ],
        ]

    @property
    def type(self) -> str:
        """
        Returns the type of the dataset.

        Returns:
            str: The dataset type.
        """
        return self._type

    @property
    def df(self):
        """
        Returns the dataset as a pandas DataFrame.

        Returns:
            pd.DataFrame: The dataset as a DataFrame.
        """
        return self._df

    @property
    def copy(self):
        """
        Returns a copy of the raw_dataset dataframe.
        """
        return self._df.copy()

    def x_df(self):
        """
        Returns the non target and prediction columns.

        Returns:
            pd.DataFrame: The non target and prediction columns .
        """
        return self._df[[name for name in self.columns if name in self.feature_columns]]

    def y_df(self):
        """
        Returns the target columns (y) of the dataset.

        Returns:
            pd.DataFrame: The target columns.
        """
        return self._df[self.target_column]

    def y_pred_df(self):
        """
        Returns the target columns (y) of the dataset.

        Returns:
            pd.DataFrame: The target columns.
        """
        return self._df[self.prediction_column]

    def serialize(self):
        """
        Serializes the dataset to a dictionary.

        Returns:
            Dict: The serialized dataset.
        """
        # Dataset with no targets can be logged
        dataset_dict = {}
        dataset_dict["targets"] = {
            "target_column": self.target_column,
            "class_labels": self._target_class_labels,
        }

        return dataset_dict

    def get_feature_type(self, feature_id):
        """
        Returns the type of the specified feature.

        Args:
            feature_id (str): The ID of the feature.

        Returns:
            str: The type of the feature.
        """
        feature = self.get_feature_by_id(feature_id)
        return feature["type"]

    def get_features_columns(self):
        """
        Returns the column names of the feature variables.

        Returns:
            List[str]: The column names of the feature variables.
        """
        return self._feature_columns

    def get_numeric_features_columns(self):
        """
        Returns the column names of the numeric feature variables.

        Returns:
            List[str]: The column names of the numeric feature variables.
        """
        numerical_columns = (
            self.df[self.feature_columns]
            .select_dtypes(include=[np.number])
            .columns.tolist()
        )

        return [column for column in numerical_columns if column != self.target_column]

    def get_categorical_features_columns(self):
        """
        Returns the column names of the categorical feature variables.

        Returns:
            List[str]: The column names of the categorical feature variables.
        """

        # Extract categorical columns from the dataset
        categorical_columns = (
            self.df[self.feature_columns]
            .select_dtypes(include=[np.object, pd.Categorical])
            .columns.tolist()
        )

        return [
            column for column in categorical_columns if column != self.target_column
        ]

    def target_classes(self):
        """
        Returns the unique number of target classes for the target (Y) variable.
        """
        return [str(i) for i in np.unique(self.y)]

    def prediction_classes(self):
        """
        Returns the unique number of target classes for the target (Y) variable.
        """
        return [str(i) for i in np.unique(self.y_pred)]


@dataclass
class DataFrameDataset(NumpyDataset):
    """
    VM dataset implementation for pandas DataFrame.
    """

    def __init__(
        self,
        raw_dataset: pd.DataFrame,
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
            target_column (str, optional): The target column of the dataset. Defaults to None.
            feature_columns (list, optional): The feature columns of the dataset. Defaults to None.
            text_column (str, optional): The text column name of the dataset for nlp tasks. Defaults to None.
            target_class_labels (Dict, optional): The class labels for the target columns. Defaults to None.
        """
        index = None
        if isinstance(raw_dataset.index, pd.Index):
            index = raw_dataset.index.values

        super().__init__(
            raw_dataset=raw_dataset.values,
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


@dataclass
class TorchDataset(NumpyDataset):
    """
    VM dataset implementation for PyTorch Datasets.
    """

    def __init__(
        self,
        raw_dataset,
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
        # if we can't import torch, then it's not a PyTorch model
        try:
            import torch
        except ImportError:
            return False
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
            raw_dataset=merged_tensors,
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
