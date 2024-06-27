# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""Test Module Utils"""

import inspect


def test_description(test_class, truncate=True):
    description = inspect.getdoc(test_class).strip()

    if truncate and len(description.split("\n")) > 5:
        return description.strip().split("\n")[0] + "..."

    return description
