"""
Unit tests for high-level ValidMind client methods
"""
import unittest
from dataclasses import dataclass
from unittest import mock, TestCase

import pandas as pd
import numpy as np
import sklearn

import validmind
from validmind import (
    init_dataset,
    init_model,
    get_test_suite,
    preview_template,
    run_documentation_tests,
)


@dataclass
class MockedConfig:
    documentation_template = {
        "template_id": "binary_classification_v2",
        "template_name": "Binary classification",
        "description": "Template for binary classification models.",
        "version": "3.0.0",
        "sections": [
            {
                "id": "test_section_1",
                "title": "Test Section",
                "index_only": True,
                "order": 0,
            },
            {
                "id": "test_subsection_1",
                "title": "Test Subsection",
                "parent_section": "test_section_1",
                "contents": [
                    {
                        "content_type": "test",
                        "content_id": "class_imbalance",
                    },
                ],
            },
            {
                "id": "test_section_2",
                "title": "Test Section 2",
                "index_only": True,
                "order": 1,
            },
            {
                "id": "test_subsection_2",
                "title": "Test Subsection 2",
                "parent_section": "test_section_2",
                "contents": [
                    {
                        "content_id": "dataset_split",
                        "content_type": "metric",
                    },
                ],
            },
        ],
    }


class TestInitDataset(TestCase):
    def test_init_dataset_pandas(self):
        # Test initializing a Pandas DataFrame
        df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
        vm_dataset = init_dataset(df, target_column="col1")
        self.assertIsInstance(vm_dataset._df, pd.DataFrame)
        self.assertTrue(vm_dataset._df.equals(df))

    def test_init_dataset_numpy(self):
        # Test initializing a numpy ndarray
        arr = np.array([[1, 2, 3], [4, 5, 6]])
        vm_dataset = init_dataset(arr, target_column=2)
        self.assertIsInstance(vm_dataset._df, pd.DataFrame)
        self.assertTrue(vm_dataset._df.equals(pd.DataFrame(arr)))

    # TODO: Test initializing a PyTorch tensor


class TestInitModel(TestCase):
    def test_init_model(self):
        # Test initializing an SKLearn model
        model = sklearn.linear_model.LinearRegression()
        vm_model = init_model(model)
        self.assertEqual(vm_model.model, model)


# Run methods are tested in test_full_suite_nb.py and test_full_suite.py


class TestGetTestSuite(TestCase):
    def test_get_specfic_suite(self):
        test_suite = get_test_suite("classifier_full_suite")
        self.assertIsInstance(test_suite, validmind.vm_models.TestSuite)

    @mock.patch(
        "validmind.client_config.client_config.documentation_template",
        MockedConfig.documentation_template,
    )
    def test_get_project_test_suite(self):
        test_suite = get_test_suite()
        self.assertIsInstance(test_suite, validmind.vm_models.TestSuite)
        self.assertEqual(len(test_suite._test_plan_classes), 2)


# TODO: Fix this test
# class TestPreviewTemplate(TestCase):
#     @mock.patch(
#         "validmind.client_config.client_config.documentation_template",
#         MockedConfig.documentation_template,
#     )
#     @mock.patch("validmind.utils.is_notebook")
#     @mock.patch("IPython.display.display")
#     def test_preview_template(self, mock_is_notebook, mock_display):
#         mock_is_notebook.return_value = True
#         preview_template()
#         mock_is_notebook.assert_called_once()
#         mock_display.assert_called_once()


class TestRunDocumentationTests(TestCase):
    @mock.patch(
        "validmind.client_config.client_config.documentation_template",
        MockedConfig.documentation_template,
    )
    def test_run_documentation_tests(self):
        # create a very simple logistic regression model
        model = sklearn.linear_model.LogisticRegression()
        dataset = pd.DataFrame([[1, 1], [1, 0], [0, 1], [0, 0]], columns=["x", "y"])
        model.fit(dataset[["x"]], dataset["y"])
        vm_dataset = init_dataset(dataset, target_column="y")
        vm_model = init_model(model, train_ds=vm_dataset, test_ds=vm_dataset)

        test_suite = run_documentation_tests(
            model=vm_model, dataset=vm_dataset, send=False
        )

        self.assertIsInstance(test_suite, validmind.vm_models.TestSuite)
        self.assertEqual(len(test_suite._test_plan_classes), 2)
        self.assertEqual(len(test_suite.results), 2)


if __name__ == "__main__":
    unittest.main()
