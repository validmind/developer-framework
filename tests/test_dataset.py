"""
Unit tests for VMDataset class
"""

import unittest
from unittest import TestCase

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from validmind.client import init_model
from validmind.vm_models.dataset import DataFrameDataset
from validmind.vm_models.model import ModelAttributes, VMModel


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
        Test that a DataFrameDataset can be initialized with a pandas DataFrame and no options
        """
        vm_dataset = DataFrameDataset(raw_dataset=self.df)

        # Pandas dataframe gets converted to numpy internally and raw_dataset is a numpy array
        np.testing.assert_array_equal(vm_dataset.raw_dataset, self.df.values)
        pd.testing.assert_frame_equal(vm_dataset.df, self.df)

    def test_init_dataset_pandas_target_column(self):
        """
        Test that a DataFrameDataset provides access to the target column
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
        Test that a DataFrameDataset allows configuring feature columns
        """
        vm_dataset = DataFrameDataset(
            raw_dataset=self.df, target_column="target", feature_columns=["col1"]
        )

        # Only one feature column "col1"
        np.testing.assert_array_equal(vm_dataset.x, self.df[["col1"]].values)

        self.assertEquals(vm_dataset.get_numeric_features_columns(), ["col1"])
        self.assertEquals(vm_dataset.get_categorical_features_columns(), [])
        self.assertEquals(vm_dataset.feature_columns, ["col1"])

    def test_assign_predictions_invalid_model(self):
        """
        Test assigning predictions to dataset with an invalid model
        """
        vm_dataset = DataFrameDataset(
            raw_dataset=self.df, target_column="target", feature_columns=["col1"]
        )

        vm_model = dict()
        with self.assertRaises(ValueError, msg="Model must be a VMModel instance"):
            vm_dataset.assign_predictions(model=vm_model)

        # If a user initializes a VMModel with no underlying model or passes attributes only
        vm_model = VMModel(input_id="1234")
        with self.assertRaises(
            AttributeError, msg="VMModel must have a valid predict method"
        ):
            vm_dataset.assign_predictions(model=vm_model)

        vm_model = VMModel(
            input_id="1234",
            attributes=ModelAttributes.from_dict(
                {
                    "architecture": "Spark",
                    "language": "Python",
                }
            ),
        )
        with self.assertRaises(
            AttributeError, msg="VMModel must have a valid predict method"
        ):
            vm_dataset.assign_predictions(model=vm_model)

    def test_assign_predictions_with_classification_model(self):
        """
        Test assigning predictions to dataset with a valid model
        """
        df = pd.DataFrame({"x1": [1, 2, 3], "x2": [4, 5, 6], "y": [0, 1, 0]})
        vm_dataset = DataFrameDataset(
            raw_dataset=df, target_column="y", feature_columns=["x1", "x2"]
        )

        # Train a simple model
        model = LogisticRegression()
        model.fit(vm_dataset.x, vm_dataset.y.ravel())

        vm_model = init_model(input_id="logreg", model=model, __log=False)
        with self.assertRaises(
            ValueError, msg="Prediction column is not linked with the given logreg"
        ):
            vm_dataset.prediction_column(vm_model)

        vm_dataset.assign_predictions(model=vm_model)
        self.assertEquals(vm_dataset.prediction_column(vm_model), "logreg_prediction")

        # Check that the predictions are assigned to the dataset
        self.assertTrue("logreg_prediction" in vm_dataset.df.columns)
        self.assertIsInstance(vm_dataset.y_pred(vm_model), np.ndarray)
        self.assertIsInstance(vm_dataset.y_pred_df(vm_model), pd.Series)

        # This model in particular will calculate probabilities as well
        self.assertTrue("logreg_probabilities" in vm_dataset.df.columns)
        self.assertIsInstance(vm_dataset.y_prob(vm_model), np.ndarray)
        self.assertIsInstance(vm_dataset.y_prob_df(vm_model), pd.Series)

    def test_assign_predictions_with_regression_model(self):
        """
        Test assigning predictions to dataset with a valid model
        """
        df = pd.DataFrame({"x1": [1, 2, 3], "x2": [4, 5, 6], "y": [0.1, 1.2, 2.3]})
        vm_dataset = DataFrameDataset(
            raw_dataset=df, target_column="y", feature_columns=["x1", "x2"]
        )

        # Train a simple model
        model = LinearRegression()
        model.fit(vm_dataset.x, vm_dataset.y.ravel())

        vm_model = init_model(input_id="linreg", model=model, __log=False)
        with self.assertRaises(
            ValueError, msg="Prediction column is not linked with the given linreg"
        ):
            vm_dataset.prediction_column(vm_model)

        vm_dataset.assign_predictions(model=vm_model)
        self.assertEquals(vm_dataset.prediction_column(vm_model), "linreg_prediction")

        # Check that the predictions are assigned to the dataset
        self.assertTrue("linreg_prediction" in vm_dataset.df.columns)
        self.assertIsInstance(vm_dataset.y_pred(vm_model), np.ndarray)
        self.assertIsInstance(vm_dataset.y_pred_df(vm_model), pd.Series)

        # Linear models do not have probabilities
        self.assertFalse("linreg_probabilities" in vm_dataset.df.columns)

    def test_assign_predictions_with_multiple_models(self):
        """
        Test assigning predictions to dataset with a valid model
        """
        df = pd.DataFrame({"x1": [1, 2, 3], "x2": [4, 5, 6], "y": [0, 1, 0]})
        vm_dataset = DataFrameDataset(
            raw_dataset=df, target_column="y", feature_columns=["x1", "x2"]
        )

        # Train simple models
        lr_model = LogisticRegression()
        lr_model.fit(vm_dataset.x, vm_dataset.y.ravel())

        rf_model = RandomForestClassifier()
        rf_model.fit(vm_dataset.x, vm_dataset.y.ravel())

        vm_lr_model = init_model(input_id="logreg", model=lr_model, __log=False)
        vm_rf_model = init_model(input_id="rf", model=rf_model, __log=False)

        vm_dataset.assign_predictions(model=vm_lr_model)
        vm_dataset.assign_predictions(model=vm_rf_model)

        self.assertEquals(
            vm_dataset.prediction_column(vm_lr_model), "logreg_prediction"
        )
        self.assertEquals(vm_dataset.prediction_column(vm_rf_model), "rf_prediction")

        # Check that the predictions are assigned to the dataset
        self.assertTrue("logreg_prediction" in vm_dataset.df.columns)
        self.assertTrue("rf_prediction" in vm_dataset.df.columns)
        self.assertIsInstance(vm_dataset.y_pred(vm_lr_model), np.ndarray)
        self.assertIsInstance(vm_dataset.y_pred_df(vm_lr_model), pd.Series)
        self.assertIsInstance(vm_dataset.y_pred(vm_rf_model), np.ndarray)
        self.assertIsInstance(vm_dataset.y_pred_df(vm_rf_model), pd.Series)

        # This model in particular will calculate probabilities as well
        self.assertTrue("logreg_probabilities" in vm_dataset.df.columns)
        self.assertTrue("rf_probabilities" in vm_dataset.df.columns)
        self.assertIsInstance(vm_dataset.y_prob(vm_lr_model), np.ndarray)
        self.assertIsInstance(vm_dataset.y_prob_df(vm_lr_model), pd.Series)
        self.assertIsInstance(vm_dataset.y_prob(vm_rf_model), np.ndarray)
        self.assertIsInstance(vm_dataset.y_prob_df(vm_rf_model), pd.Series)


if __name__ == "__main__":
    unittest.main()
