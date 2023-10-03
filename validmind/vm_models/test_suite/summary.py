# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List, Optional

import ipywidgets as widgets
from IPython.display import display

from ...logging import get_logger
from ...utils import clean_docstring
from .result import TestSuiteFailedResult
from .test_suite import TestSuiteSection, TestSuiteTest

logger = get_logger(__name__)


def id_to_name(id: str) -> str:
    # replace underscores, hyphens etc with spaces
    name = id.replace("_", " ").replace("-", " ").replace(".", " ")
    # capitalize each word
    name = " ".join([word.capitalize() for word in name.split(" ")])

    return name


@dataclass
class TestSuiteSectionSummary:

    tests: List[TestSuiteTest]
    description: Optional[str] = None

    _widgets: List[widgets.Widget] = None

    def __post_init__(self):
        self._build_summary()

    def _add_description(self):
        description = f'<div class="result">{clean_docstring(self.description)}</div>'
        self._widgets.append(widgets.HTML(value=description))

    def _add_tests_summary(self):
        children = []
        titles = []

        for test in self.tests:
            children.append(test.result._to_widget())
            titles.append(
                f"❌ {test.result.name}: {test.title} ({test.test_id})"
                if isinstance(test.result, TestSuiteFailedResult)
                else f"{test.result.name}: {test.title} ({test.test_id})"
            )

        self._widgets.append(widgets.Accordion(children=children, titles=titles))

    def _build_summary(self):
        self._widgets = []

        if self.description:
            self._add_description()

        self._add_tests_summary()

        self.summary = widgets.VBox(self._widgets)

    def display(self):
        display(self.summary)


@dataclass
class TestSuiteSummary:

    title: str
    description: str
    sections: List[TestSuiteSection]

    _widgets: List[widgets.Widget] = None

    def __post_init__(self):
        self._build_summary()

    def _add_title(self):
        title = f"""
        <h2>Test Suite Results: <i style="color: #DE257E">{self.title}</i></h2><hr>
        """.strip()

        self._widgets.append(widgets.HTML(value=title))

    def _add_results_link(self):
        # avoid circular import
        from ...api_client import get_api_host, get_api_project

        ui_host = get_api_host().replace("/api/v1/tracking", "").replace("api", "app")
        link = f"{ui_host}/projects/{get_api_project()}/project-overview"
        results_link = f"""
        <h3>
            Check out the updated documentation in your
            <a href="{link}" target="_blank">ValidMind project</a>.
        </h3>
        """.strip()

        self._widgets.append(widgets.HTML(value=results_link))

    def _add_description(self):
        description = f'<div class="result">{clean_docstring(self.description)}</div>'
        self._widgets.append(widgets.HTML(value=description))

    def _add_sections_summary(self):
        children = []
        titles = []

        for section in self.sections:
            if not section.tests:
                continue

            children.append(
                TestSuiteSectionSummary(
                    description=section.description,
                    tests=section.tests,
                ).summary
            )
            titles.append(id_to_name(section.section_id))

        self._widgets.append(widgets.Accordion(children=children, titles=titles))

    def _add_top_level_section_summary(self):
        self._widgets.append(
            TestSuiteSectionSummary(tests=self.sections[0].tests).summary
        )

    def _add_footer(self):
        footer = """
        <style>
            .result {
                margin: 10px 0;
                padding: 10px;
                background-color: #f1f1f1;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        </style>
        """.strip()

        self._widgets.append(widgets.HTML(value=footer))

    def _build_summary(self):
        self._widgets = []

        self._add_title()
        self._add_results_link()
        self._add_description()
        if len(self.sections) == 1:
            self._add_top_level_section_summary()
        else:
            self._add_sections_summary()

        self.summary = widgets.VBox(self._widgets)

    def display(self):
        display(self.summary)
