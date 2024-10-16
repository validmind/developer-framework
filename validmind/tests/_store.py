# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""Module for storing loaded tests and test providers"""


def singleton(cls):
    """Decorator to make a class a singleton"""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class TestProviderStore:
    """Singleton class for storing test providers"""

    def __init__(self):
        self.test_providers = {}

    def has_test_provider(self, namespace: str) -> bool:
        """Check if a test provider exists by namespace

        Args:
            namespace (str): The namespace of the test provider

        Returns:
            bool: True if the test provider exists
        """
        return namespace in self.test_providers

    def get_test_provider(self, namespace: str):
        """Get a test provider by namespace

        Args:
            namespace (str): The namespace of the test provider

        Returns:
            TestProvider: The test provider
        """
        return self.test_providers.get(namespace)

    def register_test_provider(self, namespace: str, test_provider) -> None:
        """Register an external test provider

        Args:
            namespace (str): The namespace of the test provider
            test_provider (TestProvider): The test provider
        """
        self.test_providers[namespace] = test_provider


class TestStore:
    """Singleton class for storing loaded tests"""

    def __init__(self):
        self.tests = {}
        self.custom_tests = {}

    def get_test(self, test_id: str):
        """Get a test by test ID

        Args:
            test_id (str): The test ID

        Returns:
            object: The test class or function
        """
        return self.tests.get(test_id)

    def get_custom_test(self, test_id: str):
        """Get a custom test by test ID

        Args:
            test_id (str): The test ID

        Returns:
            object: The test class or function
        """
        return self.custom_tests.get(test_id)

    def get_test_ids(self) -> list:
        """Get all registered test IDs"""
        return list(self.tests.keys())

    def register_test(self, test_id: str, test: object = None):
        """Register a test"""
        self.tests[test_id] = test

    def register_custom_test(self, test_id: str, test: object):
        """Register a single one-off custom test"""
        self.custom_tests[test_id] = test


test_store = TestStore()
test_provider_store = TestProviderStore()
