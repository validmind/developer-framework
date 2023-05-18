# TODO: this is a monolithic test for running a full suite... We should implement actual unit tests for each component

import validmind as vm
import xgboost as xgb
from validmind.datasets.classification import customer_churn as demo_dataset
from validmind.vm_models.dataset import Dataset
from validmind.vm_models.model import Model
from validmind.vm_models.test_suite import TestSuite

import unittest


class TestValidmind(unittest.TestCase):
    def setUp(self):
        self.df = demo_dataset.load_data()

        self.train_df, validation_df, self.test_df = demo_dataset.preprocess(self.df)

        x_train = self.train_df.drop(demo_dataset.target_column, axis=1)
        y_train = self.train_df[demo_dataset.target_column]
        x_val = validation_df.drop(demo_dataset.target_column, axis=1)
        y_val = validation_df[demo_dataset.target_column]

        self.model = xgb.XGBClassifier(early_stopping_rounds=10)
        self.model.set_params(
            eval_metric=["error", "logloss", "auc"],
        )
        self.model.fit(
            x_train,
            y_train,
            eval_set=[(x_val, y_val)],
            verbose=False,
        )

    def test_run_full_suite(self):
        self.vm_dataset = vm.init_dataset(
            dataset=self.df,
            target_column=demo_dataset.target_column,
            class_labels=demo_dataset.class_labels,
        )
        self.assertIsInstance(self.vm_dataset, Dataset)

        vm_train_ds = vm.init_dataset(
            dataset=self.train_df,
            type="generic",
            target_column=demo_dataset.target_column,
        )
        self.assertIsInstance(vm_train_ds, Dataset)

        self.vm_test_ds = vm.init_dataset(
            dataset=self.test_df,
            type="generic",
            target_column=demo_dataset.target_column,
        )
        self.assertIsInstance(self.vm_test_ds, Dataset)

        self.vm_model = vm.init_model(
            self.model,
            train_ds=vm_train_ds,
            test_ds=self.vm_test_ds,
        )
        self.assertIsInstance(self.vm_model, Model)

        result = vm.run_test_suite(
            "binary_classifier_full_suite",
            dataset=self.vm_dataset,
            model=self.vm_model,
            send=False,  # TODO: test sending to API
        )
        self.assertIsInstance(result, TestSuite)
        self.assertTrue(len(result.results) > 0)


if __name__ == "__main__":
    unittest.main()
