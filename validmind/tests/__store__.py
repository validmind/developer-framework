# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""Module for storing loaded tests and test providers"""

from .test_providers import TestProvider

__tests = {}
__custom_tests = {}

__test_providers = {}


def register_test(test_id: str, test_class: object = None):
    """Register a test class"""
    __tests[test_id] = test_class


def register_custom_test(test_id: str, test_class: object):
    """Register a single one-off custom test"""
    __custom_tests[test_id] = test_class


def register_test_provider(namespace: str, test_provider: TestProvider) -> None:
    """Register an external test provider

    Args:
        namespace (str): The namespace of the test provider
        test_provider (TestProvider): The test provider
    """
    __test_providers[namespace] = test_provider
