"""
Unit tests for the framewor's init() method
"""
import unittest

import validmind as vm


class TestFrameworkInit(unittest.TestCase):
    def test_no_args(self):
        """
        Test that init() raises a TypeError when no arguments are passed.
        """
        with self.assertRaises(TypeError) as err:
            vm.init()

        self.assertEqual(
            str(err.exception),
            "init() missing 1 required positional argument: 'project'",
        )

    def test_project_id_only(self):
        """
        Test that init() raises a ValueError when only a project is passed.
        """
        with self.assertRaises(ValueError) as err:
            vm.init(project="test")

        self.assertIn("API key", str(err.exception))
