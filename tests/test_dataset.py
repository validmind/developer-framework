"""
Unit tests for VMDataset class
"""

import unittest
from unittest import mock, TestCase

import pandas as pd
import numpy as np

from validmind.vm_models.dataset import DataFrameDataset


class TestTabularDataset(TestCase):
    def setUp(self):
        """
        Create a sample dataset for testing
        """
        self.df = pd.DataFrame(
            {"col1": [1, 2, 3], "col2": ["a", "b", "c"], "target": [0, 1, 0]}
        )

    def test_init_dataset_pandas_no_options(self):
        """
        Assert that a DataFrameDataset can be initialized with a pandas DataFrame and no options
        """
        vm_dataset = DataFrameDataset(raw_dataset=self.df)

        # Pandas dataframe gets converted to numpy internally and raw_dataset is a numpy array
        np.testing.assert_array_equal(vm_dataset.raw_dataset, self.df.values)
        pd.testing.assert_frame_equal(vm_dataset.df, self.df)

    def test_init_dataset_pandas_target_column(self):
        """
        Assert that a DataFrameDataset provides access to the target column
        """
        vm_dataset = DataFrameDataset(raw_dataset=self.df, target_column="target")

        self.assertEquals(vm_dataset.target_column, "target")
        np.testing.assert_array_equal(vm_dataset.y, self.df[["target"]].values)
        pd.testing.assert_series_equal(vm_dataset.y_df(), self.df["target"])

        # Feature columns should be all columns except the target column
        self.assertEquals(vm_dataset.get_numeric_features_columns(), ["col1"])
        self.assertEquals(vm_dataset.get_categorical_features_columns(), ["col2"])
        self.assertEquals(vm_dataset.feature_columns, ["col1", "col2"])

    def test_init_dataset_pandas_feature_columns(self):
        """
        Assert that a DataFrameDataset allows configuring feature columns
        """
        vm_dataset = DataFrameDataset(
            raw_dataset=self.df, target_column="target", feature_columns=["col1"]
        )

        # Only one feature column "col1"
        np.testing.assert_array_equal(vm_dataset.x, self.df[["col1"]].values)

        self.assertEquals(vm_dataset.get_numeric_features_columns(), ["col1"])
        self.assertEquals(vm_dataset.get_categorical_features_columns(), [])
        self.assertEquals(vm_dataset.feature_columns, ["col1"])


if __name__ == "__main__":
    unittest.main()
