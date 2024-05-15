# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

# gui/app.py

import os

from IPython.display import HTML, display

from .result import Result

result = Result()

bundle_wrapper_html = """
<script type="text/javascript">
{bundle_js}
</script>
"""


class App:
    def __init__(self, *children):
        self.children = children
        self.result = result

    def load_web_components(self):
        with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "bundle.js"), "r"
        ) as file:
            bundle_js = file.read()

        return HTML(bundle_wrapper_html.format(bundle_js=bundle_js))

    def render_children(self):
        rendered = ""
        for child in self.children:
            rendered += f"""
            <div>
                <{child.__class__.__name__.lower()}-component {self.render_props(child)}></{child.__class__.__name__.lower()}-component>
            </div>
            """
        return rendered

    def render_props(self, child):
        return " ".join(f'{key}="{value}"' for key, value in child.props.items())

    def display(self):
        self.load_web_components()
        html_content = f"""
        <div id="app">
            {self.render_children()}
        </div>
        """
        display(HTML(html_content))
