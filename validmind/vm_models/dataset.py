# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Dataset class wrapper
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import pandas as pd

from .dataset_utils import parse_dataset_variables


@dataclass
class VMDataset(ABC):
    """
    Abstract base class for VM datasets.
    """

    @property
    @abstractmethod
    def raw_dataset(self):
        """
        Returns the raw dataset.
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
    _column_names: list = None
    _target_column: str = None
    _text_column: str = None
    _type: str = "generic"
    _target_class_labels: dict = None
    # This is list of metadata objects for each field in the dataset. It does
    # not contain the actual data for each field, just metadata about it
    fields: list = None
    _options: dict = None
    _df: pd.DataFrame = None

    def __init__(
        self,
        raw_dataset,
        index=None,
        index_name=None,
        date_time_index=False,
        column_names=None,
        target_column: str = None,
        text_column=None,
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
            column_names (List[str], optional): The column names of the dataset. Defaults to None.
            target_column (str, optional): The target column name of the dataset. Defaults to None.
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

        if (column_names is not None) and (
            not isinstance(column_names, list)
            or not all(isinstance(element, str) for element in column_names)
        ):
            raise ValueError(
                "feature_column_names does not contain an array of strings"
            )
        self._column_names = column_names

        self._target_column = target_column
        self._text_column = text_column
        self._target_class_labels = target_class_labels
        self.options = options

        df = pd.DataFrame(self._raw_dataset, columns=self._column_names).infer_objects()

        if index is not None:
            df.set_index(pd.Index(index), inplace=True)
            df.index.name = index_name

        if date_time_index:
            df = self.__attempt_convert_index_to_datetime(df)

        self._df = df
        self.fields = parse_dataset_variables(self._df, self.options)

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
    def column_names(self) -> list:
        """
        Returns the column names of the dataset.

        Returns:
            List[str]: The column names.
        """
        return self._column_names

    @property
    def target_column(self) -> str:
        """
        Returns the target column of the dataset.

        Returns:
            str: The target column name.
        """
        return self._target_column

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
                self.column_names.index(name)
                for name in self.column_names
                if name != self.target_column
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
                self.column_names.index(name)
                for name in self.column_names
                if name == self.target_column
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
        Returns the input features (X) of the dataset.

        Returns:
            pd.DataFrame: The input features.
        """
        return self._df[self.get_features_columns()]

    def y_df(self):
        """
        Returns the target columns (y) of the dataset.

        Returns:
            pd.DataFrame: The target columns.
        """
        return self._df[self.target_column]

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
        return [
            field_dic["id"]
            for field_dic in self.fields
            if (field_dic["id"] != self.target_column)
        ]

    def get_numeric_features_columns(self):
        """
        Returns the column names of the numeric feature variables.

        Returns:
            List[str]: The column names of the numeric feature variables.
        """
        numerical_columns = self.df.select_dtypes(include=[np.number]).columns.tolist()

        return [column for column in numerical_columns if column != self.target_column]

    def get_categorical_features_columns(self):
        """
        Returns the column names of the categorical feature variables.

        Returns:
            List[str]: The column names of the categorical feature variables.
        """

        # Extract categorical columns from the dataset
        categorical_columns = self.df.select_dtypes(
            include=[np.object, pd.Categorical]
        ).columns.tolist()

        return [
            column for column in categorical_columns if column != self.target_column
        ]

    def target_classes(self):
        """
        Returns the unique number of target classes for the target (Y) variable.
        """
        return [str(i) for i in np.unique(self.y)]


@dataclass
class DataFrameDataset(NumpyDataset):
    """
    VM dataset implementation for pandas DataFrame.
    """

    def __init__(
        self,
        raw_dataset: pd.DataFrame,
        target_column: str = None,
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
            column_names=raw_dataset.columns.to_list(),
            target_column=target_column,
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
        column_names=None,
        target_column: str = None,
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
            column_names (List[str]): The column names of the dataset.
            target_column (str, optional): The target column of the dataset. Defaults to None.
            text_column (str, optional): The text column name of the dataset for nlp tasks. Defaults to None.
            target_class_labels (Dict, optional): The class labels for the target columns. Defaults to None.
        """
        # Merge tensors along the column axis
        if raw_dataset.tensors[1].ndim == 1:
            tensor2 = np.expand_dims(
                raw_dataset.tensors[1], axis=1
            )  # Convert tensor to a column vector
            merged_tensors = np.concatenate((raw_dataset.tensors[0], tensor2), axis=1)
        else:
            merged_tensors = np.concatenate(
                (raw_dataset.tensors[0], raw_dataset.tensors[1]), axis=1
            )
        if column_names is None:
            n_cols = merged_tensors.shape[1]
            column_names = list(
                np.linspace(0, n_cols - 1, num=n_cols, dtype=int).astype(str)
            )
        if target_column is None:
            n_cols = merged_tensors.shape[1] - 1
            target_column = str(n_cols)

        super().__init__(
            raw_dataset=merged_tensors,
            index_name=index_name,
            index=index,
            column_names=column_names,
            target_column=target_column,
            text_column=text_column,
            target_class_labels=target_class_labels,
            options=options,
        )
