"""
Unit tests for Validmind tests module
"""
import unittest
from unittest import TestCase

from pandas.io.formats.style import Styler

from validmind.vm_models import Test
from validmind.vm_models.test_context import TestContext
from validmind.tests import list_tests, load_test, describe_test, register_test_provider


class TestTestsModule(TestCase):
    def test_list_tests(self):
        tests = list_tests(pretty=False)
        self.assertTrue(len(tests) > 0)

    def test_list_tests_filter(self):
        tests = list_tests(filter="sklearn", pretty=False)
        self.assertTrue(len(tests) > 1)

    def test_list_tests_filter_2(self):
        tests = list_tests(
            filter="validmind.model_validation.ModelMetadata", pretty=False
        )
        self.assertTrue(len(tests) == 1)

    def test_load_test(self):
        test = load_test("validmind.model_validation.ModelMetadata")
        self.assertTrue(test is not None)
        self.assertTrue(issubclass(test, Test))

    def test_describe_test(self):
        describe_test("validmind.model_validation.ModelMetadata")
        description = describe_test(
            "validmind.model_validation.ModelMetadata", raw=True
        )
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
                fake_test = Test(test_context=TestContext())
                fake_test.test_id = test_id
                return fake_test

        register_test_provider("fake", TestProvider())

        test = load_test("fake.fake_test_id")
        self.assertEqual(test.test_id, "fake.fake_test_id")


if __name__ == "__main__":
    unittest.main()
