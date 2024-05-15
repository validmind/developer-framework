# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

# gui/result.py


class Result:
    def __init__(self):
        self.data = {}

    def update(self, key, value):
        self.data[key] = value

    def save(self):
        # Implement the save logic here, e.g., save to a file or database
        print(f"Saving data: {self.data}")
