# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

# gui/components.py

import json

from IPython.display import HTML, display


class Component:
    def __init__(self, **props):
        self.name = self.__class__.__name__.lower()
        self.props = props

    def to_html(self):
        return f"""
<h1>{self.name}</h1>
<{self.name} id="{self.name}">
</{self.name}>
<script>
document.getElementById("{self.name}").data = {self.to_json()};
</script>
"""

    def to_json(self):
        return json.dumps(self.props)

    def display(self):
        display(HTML(self.to_html()))


class Grid(Component):
    def __init__(self, *children):
        self.children = children
        super().__init__(
            components=[
                {"type": child.__class__.__name__.lower(), "props": child.props}
                for child in children
            ]
        )

    def to_json(self):
        return json.dumps(
            {
                "components": [child.to_json() for child in self.children],
                "comm_id": self.comm_id,
            }
        ).replace('"', "&quot;")


class MarkdownEditor(Component):
    _props = ["initialContent"]


class DataTable(Component):
    _props = ["data"]


class PlotlyComponent(Component):
    _props = ["figure"]
