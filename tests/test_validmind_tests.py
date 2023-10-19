"""This is a test harness to run unit tests against the ValidMind tests"""

import unittest

from validmind.tests import list_tests, load_test
from validmind.vm_models import TestContext

class TestValidMindTests(unittest.TestCase):
    pass


def create_unit_test_func(vm_test):
    def unit_test_func(self):
        result = vm_test.run()
        vm_test.test(result)

    return unit_test_func


def create_unit_test_funcs_from_vm_tests():
    test_context = TestContext()

    for vm_test_id in list_tests(pretty=False):
        # load the test class and initialize it with necessary data
        vm_test_class = load_test(vm_test_id)
        vm_test = vm_test_class(test_context=test_context, params={})

        # create a unit test function for the test class
        unit_test_func = create_unit_test_func(vm_test)
        unit_test_func_name = f'test_{vm_test_id.replace(".", "_")}'

        # add the unit test function to the unit test class
        setattr(TestValidMindTests, f'test_{unit_test_func_name}', unit_test_func)


create_unit_test_funcs_from_vm_tests()


if __name__ == "__main__":
    unittest.main()
