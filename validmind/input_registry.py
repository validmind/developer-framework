# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Central class to register inputs
"""

from .errors import InvalidInputError


class InputRegistry:
    def __init__(self):
        self.registry = {}

    def add(self, key, obj):
        self.registry[key] = obj

    def get(self, key):
        input_obj = self.registry.get(key)
        if not input_obj:
            raise InvalidInputError(
                f"There's no such input with given ID '{key}'. "
                "Please pass valid input ID"
            )
        return input_obj

    def list_input_objects(self):
        return self.registry.keys()


input_registry = InputRegistry()
