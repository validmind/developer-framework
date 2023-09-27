# Copyright © 2023 ValidMind Inc. All rights reserved.
from typing import List

from ..test.test import Test
from .tests import LoadTestError, load_test


class TestLoader:
    """TestLoader class that handles loading individual tests for test suites"""

    def load_test(self, test_id: str, test_props: dict = None):
        try:
            test_class = load_test(test_id)

            if test_props:
                for key, val in test_props.items():
                    setattr(test_class, key, val)

            return test_class

        except LoadTestError as e:
            print(f"Failed to load test {test_id}: {e}")
            return None

    def init_tests(self, test_defs: List[str or dict]):
        tests = []

        for test_def in test_defs:
            if isinstance(test_def, dict):
                test_id = test_def["test_id"]
                props = {k: v for k, v in test_def.items() if k != "test_id"}
            else:
                test_id = test_def
                props = None

            test_class = self.load_test(test_id, props)
            if test_class:
                tests.append(test_class)

        return tests

    def get_required_inputs(self, tests: List[Test]) -> List[str]:
        required = set()
        for test in tests:
            required.update(test.required_inputs or [])
        return list(required)
