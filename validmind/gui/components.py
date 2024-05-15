# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import json
import os

from IPython.display import HTML, display

JS_BUNDLE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "js/bundle.js"
)

COMPONENT_BOILERPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; padding: 0; }}
        #root {{ width: 100%; height: 100%; }}
    </style>
</head>
<body>
    <div id="root"></div>
</body>

<script>
{js}
(function() {{
    const props = {props};
    console.log(VMComponents.{name});
    console.log(props);
    ReactDOM.render(React.createElement(VMComponents.{name}, props), document.getElementById('root'));
}})();
</script>
</html>
"""

IFRAME_BOILERPLATE = """
<iframe srcdoc="{html}" width="99%" height="700px"></iframe>
"""


class Component:
    def __init__(self, **props):
        self.name = self.__class__.__name__
        self.props = props

        self.js = self._load_js()

    def _load_js(self):
        with open(JS_BUNDLE_PATH, "r") as file:
            return file.read()

    def to_html(self):
        html = COMPONENT_BOILERPLATE.format(
            name=self.name, props=json.dumps(self.props), js=self.js
        )
        return IFRAME_BOILERPLATE.format(html=html.replace('"', "&quot;"))

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
