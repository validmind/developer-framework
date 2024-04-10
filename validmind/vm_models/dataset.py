# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Dataset class wrapper
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
import polars as pl

from validmind.logging import get_logger
from validmind.vm_models.model import VMModel

logger = get_logger(__name__)


def is_supported_dataset_type(dataset):
    """
    Checks if the dataset is a supported type.

    Args:
        dataset (object): The dataset to check.

    Returns:
        bool: True if the dataset is a supported type, False otherwise.
    """
    return isinstance(dataset, (pd.DataFrame, pl.DataFrame, np.ndarray))


def init_anonymous_dataset(raw_dataset, input_id=None, **kwargs):
    """
    Initializes an anonymous VM dataset object based on the type of the raw dataset.
    This interface is used internally by ValidMind to create dataset objects that
    are not logged as inputs to the API since the end user is not utilizing the
    `init_dataset` interface to initialize a VMDataset object.

    Args:
        raw_dataset (object): The raw dataset.
        input_id (str, optional): The input ID of the dataset. Defaults to None.
        kwargs (dict): Additional keyword arguments.

    Returns:
        VMDataset: The dataset object.
    """
    from ..client import init_dataset

    return init_dataset(raw_dataset, input_id=input_id, **kwargs)


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
    def assign_predictions(
        self,
        model,
        prediction_values: list = None,
        prediction_column=None,
    ):
        """
        Assigns predictions to the dataset for a given model or prediction values.
        The dataset is updated with a new column containing the predictions.
        """
        pass

    @abstractmethod
    def get_extra_column(self, column_name):
        """
        Returns the values of the specified extra column.

        Args:
            column_name (str): The name of the extra column.

        Returns:
            np.ndarray: The values of the extra column.
        """
        pass

    @abstractmethod
    def add_extra_column(self, column_name, column_values=None):
        """
        Adds an extra column to the dataset without modifying the dataset `features` and `target` columns.

        Args:
            column_name (str): The name of the extra column.
            column_values (np.ndarray, optional): The values of the extra column.
        """
        pass

    @property
    @abstractmethod
    def input_id(self) -> str:
        """
        Returns input id of dataset.

        Returns:
            str: input_id.
        """
        return self.input_id

    @property
    @abstractmethod
    def columns(self) -> list:
        """
        Returns the the list of columns in the dataset.

        Returns:
            List[str]: The columns list.
        """
        pass

    @property
    @abstractmethod
    def target_column(self) -> str:
        """
        Returns the target column name of the dataset.

        Returns:
            str: The target column name.
        """
        pass

    @property
    @abstractmethod
    def feature_columns(self) -> list:
        """
        Returns the feature columns of the dataset. If _feature_columns is None,
        it returns all columns except the target column.

        Returns:
            list: The list of feature column names.
        """
        pass

    @property
    @abstractmethod
    def text_column(self) -> str:
        """
        Returns the text column of the dataset.

        Returns:
            str: The text column name.
        """
        pass

    @property
    @abstractmethod
    def x(self) -> np.ndarray:
        """
        Returns the input features (X) of the dataset.

        Returns:
            np.ndarray: The input features.
        """
        pass

    @property
    @abstractmethod
    def y(self) -> np.ndarray:
        """
        Returns the target variables (y) of the dataset.

        Returns:
            np.ndarray: The target variables.
        """
        pass

    @abstractmethod
    def y_pred(self, model_id) -> np.ndarray:
        """
        Returns the prediction values (y_pred) of the dataset for a given model_id.

        Returns:
            np.ndarray: The prediction values.
        """
        pass

    @property
    @abstractmethod
    def df(self):
        """
        Returns the dataset as a pandas DataFrame.

        Returns:
            pd.DataFrame: The dataset as a DataFrame.
        """
        pass

    @property
    @abstractmethod
    def copy(self):
        """
        Returns a copy of the raw_dataset dataframe.
        """
        pass

    @abstractmethod
    def x_df(self):
        """
        Returns the non target and prediction columns.

        Returns:
            pd.DataFrame: The non target and prediction columns .
        """
        pass

    @abstractmethod
    def y_df(self):
        """
        Returns the target columns (y) of the dataset.

        Returns:
            pd.DataFrame: The target columns.
        """
        pass

    @abstractmethod
    def y_pred_df(self, model_id):
        """
        Returns the target columns (y) of the dataset.

        Returns:
            pd.DataFrame: The target columns.
        """
        pass

    @abstractmethod
    def prediction_column(self, model_id) -> str:
        """
        Returns the prediction column name of the dataset.

        Returns:
            str: The prediction column name.
        """
        pass

    @abstractmethod
    def get_features_columns(self):
        """
        Returns the column names of the feature variables.

        Returns:
            List[str]: The column names of the feature variables.
        """
        pass

    @abstractmethod
    def get_numeric_features_columns(self):
        """
        Returns the column names of the numeric feature variables.

        Returns:
            List[str]: The column names of the numeric feature variables.
        """
        pass

    @abstractmethod
    def get_categorical_features_columns(self):
        """
        Returns the column names of the categorical feature variables.

        Returns:
            List[str]: The column names of the categorical feature variables.
        """
        pass


@dataclass
class NumpyDataset(VMDataset):
    """
    VM dataset implementation for NumPy arrays.
    """

    _input_id: str = (None,)
    _raw_dataset: np.ndarray = None
    _index: np.ndarray = None
    _index_name: str = None
    _columns: list = field(init=True, default=None)
    _target_column: str = field(init=True, default=None)
    _feature_columns: list = field(init=True, default=None)
    _text_column: str = field(init=True, default=None)
    _type: str = "generic"
    _target_class_labels: dict = field(init=True, default=None)
    _df: pd.DataFrame = field(init=True, default=None)
    _extra_columns: dict = field(
        default_factory=lambda: {
            "prediction_columns": {},
            "group_by_column": None,
        }
    )

    def __init__(
        self,
        raw_dataset,
        input_id: str = None,
        model: VMModel = None,
        index=None,
        index_name=None,
        date_time_index=False,
        columns=None,
        target_column: str = None,
        feature_columns: list = None,
        text_column=None,
        extra_columns: dict = None,
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
        # initialize input_id
        self._input_id = input_id

        # initialize raw dataset
        if not isinstance(raw_dataset, np.ndarray):
            raise ValueError("Expected Numpy array for attribute raw_dataset")
        self._raw_dataset = raw_dataset

        # initialize index and index name
        if index is not None and not isinstance(index, np.ndarray):
            raise ValueError("Expected Numpy array for attribute raw_dataset")
        self._index = index
        self._index_name = index_name

        # initialize columns and df
        self._columns = columns or []
        if not self._columns:
            df = pd.DataFrame(self._raw_dataset).infer_objects()
            self._columns = df.columns.to_list()
        else:
            df = pd.DataFrame(self._raw_dataset, columns=self._columns).infer_objects()

        # set index to dataframe
        if index is not None:
            df.set_index(pd.Index(index), inplace=True)
            df.index.name = index_name

        # attempt to convert index to datatime
        if date_time_index:
            df = self.__attempt_convert_index_to_datetime(df)

        # initialize dataframe
        self._df = df

        # initialize target column
        self._target_column = target_column
        # initialize extra columns
        self.__set_extra_columns(extra_columns)
        # initialize feature columns
        self.__set_feature_columns(feature_columns)
        # initialize text column, target class labels and options
        self._text_column = text_column
        self._target_class_labels = target_class_labels
        self.options = options
        if model:
            self.assign_predictions(model)

    def __set_extra_columns(self, extra_columns):
        if extra_columns is None:
            extra_columns = {
                "prediction_columns": {},
                "group_by_column": None,
            }
        self._extra_columns = extra_columns

    def __set_feature_columns(self, feature_columns):
        ex_columns = []

        if self._extra_columns.get("prediction_columns"):
            ex_columns.extend(self._extra_columns["prediction_columns"].values())

        if self._extra_columns.get("group_by_column"):
            ex_columns.extend(self._extra_columns["group_by_column"])

        extra_columns_list = ex_columns if not feature_columns else []

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

    def __model_id_in_prediction_columns(self, model, prediction_column):
        return model.input_id in self._extra_columns.get("prediction_columns", {})

    def __assign_prediction_values(self, model, pred_column, prediction_values):
        # Link the prediction column with the model
        self._extra_columns.setdefault("prediction_columns", {})[
            model.input_id
        ] = pred_column

        # Check if the predictions are multi-dimensional (e.g., embeddings)
        is_multi_dimensional = (
            isinstance(prediction_values, np.ndarray) and prediction_values.ndim > 1
        )

        if is_multi_dimensional:
            # For multi-dimensional outputs, convert to a list of lists to store in DataFrame
            self._df[pred_column] = list(map(list, prediction_values))
        else:
            # If not multi-dimensional or a standard numpy array, reshape for compatibility
            self._raw_dataset = np.hstack(
                (self._raw_dataset, np.array(prediction_values).reshape(-1, 1))
            )
            self._df[pred_column] = prediction_values

        # Update the dataset columns list
        if pred_column not in self._columns:
            self._columns.append(pred_column)

    def assign_predictions(  # noqa: C901 - we need to simplify this method
        self,
        model,
        prediction_values: list = None,
        prediction_column=None,
    ):
        if not model:
            raise ValueError(
                "Model must be provided to link prediction column with the dataset"
            )

        if prediction_column:
            if prediction_column not in self.columns:
                raise ValueError(
                    f"Prediction column {prediction_column} doesn't exist in the dataset"
                )
            if self.__model_id_in_prediction_columns(
                model=model, prediction_column=prediction_column
            ):
                raise ValueError(
                    f"Prediction column {prediction_column} already linked to the VM model"
                )
            self._extra_columns.setdefault("prediction_columns", {})[
                model.input_id
            ] = prediction_column
        elif prediction_values is not None:
            if len(prediction_values) != self.df.shape[0]:
                raise ValueError(
                    "Length of prediction values doesn't match number of rows of the dataset"
                )
            pred_column = f"{model.input_id}_prediction"
            if pred_column in self.columns:
                raise ValueError(
                    f"Prediction column {pred_column} already exists in the dataset"
                )
            self.__assign_prediction_values(model, pred_column, prediction_values)
        elif not self.__model_id_in_prediction_columns(
            model=model, prediction_column=prediction_column
        ):
            pred_column = f"{model.input_id}_prediction"
            if pred_column in self.columns:
                logger.info(
                    f"Prediction column {pred_column} already exist in the dataset. Linking the model with the {pred_column} column"
                )
                return

            logger.info("Running predict()... This may take a while")

            # If the model is a FoundationModel, we need to pass the DataFrame to
            # the predict method since it requires column names in order to format
            # the input prompt with its template variables
            x_only = (
                self.x_df() if model.model_library() == "FoundationModel" else self.x
            )

            prediction_values = np.array(model.predict(x_only))
            self.__assign_prediction_values(model, pred_column, prediction_values)
        else:
            logger.info(
                f"Prediction column {self._extra_columns['prediction_columns'][model.input_id]} already linked to the {model.input_id}"
            )

    def get_extra_column(self, column_name):
        """
        Returns the values of the specified extra column.

        Args:
            column_name (str): The name of the extra column.

        Returns:
            np.ndarray: The values of the extra column.
        """
        if column_name not in self.extra_columns:
            raise ValueError(f"Column {column_name} is not an extra column")

        return self._df[column_name]

    def add_extra_column(self, column_name, column_values=None):
        """
        Adds an extra column to the dataset without modifying the dataset `features` and `target` columns.

        Args:
            column_name (str): The name of the extra column.
            column_values (np.ndarray, optional): The values of the extra column.
        """
        if column_name in self.extra_columns:
            logger.info(f"Column {column_name} already registered as an extra column")
            return

        # The column name already exists in the dataset so we just assign the extra column
        if column_name in self.columns:
            self._extra_columns[column_name] = column_name
            logger.info(
                f"Column {column_name} exists in the dataset, registering as an extra column"
            )
            return

        if column_values is None:
            raise ValueError(
                "Column values must be provided when the column doesn't exist in the dataset"
            )

        if len(column_values) != self.df.shape[0]:
            raise ValueError(
                "Length of column values doesn't match number of rows of the dataset"
            )

        self._raw_dataset = np.hstack(
            (self._raw_dataset, np.array(column_values).reshape(-1, 1))
        )
        self._columns.append(column_name)
        self._df[column_name] = column_values
        self._extra_columns[column_name] = column_name
        logger.info(f"Column {column_name} added as an extra column")

    @property
    def raw_dataset(self) -> np.ndarray:
        """
        Returns the raw dataset.

        Returns:
            np.ndarray: The raw dataset.
        """
        return self._raw_dataset

    @property
    def input_id(self) -> str:
        """
        Returns input id of dataset.

        Returns:
            str: input_id.
        """
        return self._input_id

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
        return self._feature_columns or []

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

    def y_pred(self, model_id) -> np.ndarray:
        """
        Returns the prediction variables for a given model_id, accommodating
        both scalar predictions and multi-dimensional outputs such as embeddings.

        Args:
            model_id (str): The ID of the model whose predictions are sought.

        Returns:
            np.ndarray: The prediction variables, either as a flattened array for
            scalar predictions or as an array of arrays for multi-dimensional outputs.
        """
        pred_column = self.prediction_column(model_id)

        # First, attempt to retrieve the prediction data from the DataFrame
        if hasattr(self, "_df") and pred_column in self._df.columns:
            predictions = self._df[pred_column].to_numpy()

            # Check if the predictions are stored as objects (e.g., lists for embeddings)
            if self._df[pred_column].dtype == object:
                # Attempt to convert lists to a numpy array
                try:
                    predictions = np.stack(predictions)
                except ValueError as e:
                    # Handling cases where predictions cannot be directly stacked
                    raise ValueError(f"Error stacking prediction arrays: {e}")
        else:
            # Fallback to using the raw numpy dataset if DataFrame is not available or suitable
            try:
                predictions = self.raw_dataset[
                    :, self.columns.index(pred_column)
                ].flatten()
            except IndexError as e:
                raise ValueError(
                    f"Prediction column '{pred_column}' not found in raw dataset: {e}"
                )

        return predictions

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

    def y_pred_df(self, model_id):
        """
        Returns the target columns (y) of the dataset.

        Returns:
            pd.DataFrame: The target columns.
        """
        return self._df[self.prediction_column(model_id=model_id)]

    def prediction_column(self, model_id) -> str:
        """
        Returns the prediction column name of the dataset.

        Returns:
            str: The prediction column name.
        """
        pred_column = self._extra_columns.get("prediction_columns", {}).get(model_id)
        if pred_column is None:
            raise ValueError(
                f"Prediction column is not linked with the given {model_id}"
            )
        return pred_column

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
        return self.feature_columns

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
            .select_dtypes(include=[object, pd.Categorical])
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

    def __str__(self):
        return (
            f"=================\n"
            f"VMDataset object: \n"
            f"=================\n"
            f"Input ID: {self._input_id}\n"
            f"Target Column: {self._target_column}\n"
            f"Feature Columns: {self._feature_columns}\n"
            f"Text Column: {self._text_column}\n"
            f"Extra Columns: {self._extra_columns}\n"
            f"Type: {self._type}\n"
            f"Target Class Labels: {self._target_class_labels}\n"
            f"Columns: {self._columns}\n"
            f"Index Name: {self._index_name}\n"
            f"Index: {self._index}\n"
            f"=================\n"
        )


@dataclass
class DataFrameDataset(NumpyDataset):
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


@dataclass
class PolarsDataset(NumpyDataset):
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


@dataclass
class TorchDataset(NumpyDataset):
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
