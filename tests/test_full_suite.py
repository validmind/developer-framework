# this will run a test suite while simulating the event loop that runs in a jupyter notebook
# between this file and test_full_suite.py, we test running in a notebook and running in a script

import unittest
from unittest.mock import patch

import xgboost as xgb

from validmind.datasets.classification import customer_churn as demo_dataset


class TestFullTestSuite(unittest.TestCase):
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

    @patch.multiple(
        "validmind.api_client",
        log_dataset=unittest.mock.DEFAULT,
        log_figure=unittest.mock.DEFAULT,
        log_metadata=unittest.mock.DEFAULT,
        log_metrics=unittest.mock.DEFAULT,
        log_test_result=unittest.mock.DEFAULT,
    )
    def test_run_full_suite(self, **mocks):
        import validmind as vm
        from validmind.vm_models.dataset import VMDataset
        from validmind.vm_models.model import VMModel
        from validmind.vm_models.test_suite import TestSuite

        self.vm_dataset = vm.init_dataset(
            dataset=self.df,
            target_column=demo_dataset.target_column,
            class_labels=demo_dataset.class_labels,
        )
        self.assertIsInstance(self.vm_dataset, VMDataset)

        vm_train_ds = vm.init_dataset(
            dataset=self.train_df,
            target_column=demo_dataset.target_column,
        )
        self.assertIsInstance(vm_train_ds, VMDataset)

        self.vm_test_ds = vm.init_dataset(
            dataset=self.test_df,
            target_column=demo_dataset.target_column,
        )
        self.assertIsInstance(self.vm_test_ds, VMDataset)

        self.vm_model = vm.init_model(
            self.model,
            train_ds=vm_train_ds,
            test_ds=self.vm_test_ds,
        )
        self.assertIsInstance(self.vm_model, VMModel)

        result = vm.run_test_suite(
            "binary_classifier_full_suite",
            dataset=self.vm_dataset,
            model=self.vm_model,
        )

        self.assertIsInstance(result, TestSuite)
        self.assertTrue(len(result.results) > 0)


if __name__ == "__main__":
    unittest.main()
