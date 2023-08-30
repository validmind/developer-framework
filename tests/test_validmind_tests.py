"""
Unit tests for Validmind tests module
"""
import unittest
from unittest import TestCase

from pandas.io.formats.style import Styler

from validmind.vm_models import Test
from validmind.tests import (
    list_tests, load_test, describe_test, register_test_provider
)


class TestTestsModule(TestCase):
    def test_list_tests(self):
        tests = list_tests(pretty=False)
        self.assertTrue(len(tests) > 0)

    def test_list_tests_filter(self):
        tests = list_tests(filter="sklearn", pretty=False)
        self.assertTrue(len(tests) > 1)

    def test_list_tests_filter_2(self):
        tests = list_tests(filter="validmind.model_validation.ModelMetadata", pretty=False)
        self.assertTrue(len(tests) == 1)

    def test_load_test(self):
        test = load_test("validmind.model_validation.ModelMetadata")
        self.assertTrue(test is not None)
        self.assertTrue(issubclass(test, Test))

    def test_load_test_legacy(self):
        actual_test = load_test("validmind.model_validation.ModelMetadata")
        test = load_test("model_metadata")
        self.assertTrue(test is not None)
        self.assertTrue(issubclass(test, Test))
        self.assertEqual(test, actual_test)

    def test_describe_test(self):
        description = describe_test("validmind.model_validation.ModelMetadata")
        self.assertIsInstance(description, Styler)
        description = describe_test("validmind.model_validation.ModelMetadata", raw=True)
        self.assertIsInstance(description, dict)
        # check if description dict has "ID", "Name", "Description", "Test Type", "Required Inputs" and "Params" keys
        self.assertTrue("ID" in description)
        self.assertTrue("Name" in description)
        self.assertTrue("Description" in description)
        self.assertTrue("Test Type" in description)
        self.assertTrue("Required Inputs" in description)
        self.assertTrue("Params" in description)

    def test_describe_test_legacy(self):
        description = describe_test("model_metadata")
        self.assertIsInstance(description, Styler)
        description = describe_test("model_metadata", raw=True)
        self.assertIsInstance(description, dict)
        # check if description dict has "ID", "Name", "Description", "Test Type", "Required Inputs" and "Params" keys
        self.assertTrue("ID" in description)
        self.assertTrue("Name" in description)
        self.assertTrue("Description" in description)
        self.assertTrue("Test Type" in description)
        self.assertTrue("Required Inputs" in description)
        self.assertTrue("Params" in description)

    def test_describe_test_name(self):
        description = describe_test("ModelMetadata")
        self.assertIsInstance(description, Styler)
        description = describe_test("ModelMetadata", raw=True)
        self.assertIsInstance(description, dict)
        # check if description dict has "ID", "Name", "Description", "Test Type", "Required Inputs" and "Params" keys
        self.assertTrue("ID" in description)
        self.assertTrue("Name" in description)
        self.assertTrue("Description" in description)
        self.assertTrue("Test Type" in description)
        self.assertTrue("Required Inputs" in description)
        self.assertTrue("Params" in description)

    def test_test_provider_registration(self):
        class TestProvider:
            def load_test(self, test_id):
                return "FakeTest"

        register_test_provider("fake", TestProvider())

        test = load_test("fake.test_id")
        self.assertEqual(test, "FakeTest")

if __name__ == "__main__":
    unittest.main()
