# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from pprint import pformat

import mistune
from IPython.display import display
from ipywidgets import HTML, Accordion, VBox

from .html_templates.content_blocks import (
    failed_content_block_html,
    non_test_content_block_html,
    test_content_block_html,
)
from .logging import get_logger
from .tests import LoadTestError, describe_test
from .utils import is_notebook
from .vm_models import TestSuite

logger = get_logger(__name__)

CONTENT_TYPE_MAP = {
    "test": "Threshold Test",
    "metric": "Metric",
    "metadata_text": "Metadata Text",
    "dynamic": "Dynamic Content",
    "text": "Text",
}


def _convert_sections_to_section_tree(
    sections, parent_id="_root_", start_section_id=None
):
    section_tree = []

    for section in sections:
        section_parent_id = section.get("parent_section", "_root_")

        if start_section_id:
            if section["id"] == start_section_id:
                child_sections = _convert_sections_to_section_tree(
                    sections, section["id"]
                )
                section_tree.append({**section, "sections": child_sections})

        elif section_parent_id == parent_id:
            child_sections = _convert_sections_to_section_tree(sections, section["id"])
            section_tree.append({**section, "sections": child_sections})

    if start_section_id and not section_tree:
        raise ValueError(f"Section {start_section_id} not found in template")

    return sorted(section_tree, key=lambda x: x.get("order", 0))


def _create_content_widget(content):
    content_type = CONTENT_TYPE_MAP[content["content_type"]]

    if content["content_type"] not in ["metric", "test"]:
        return HTML(
            non_test_content_block_html.format(
                content_id=content["content_id"],
                content_type=content_type,
            )
        )

    try:
        test_deets = describe_test(test_id=content["content_id"], raw=True)
    except LoadTestError:
        return HTML(failed_content_block_html.format(test_id=content["content_id"]))

    return Accordion(
        children=[
            HTML(
                test_content_block_html.format(
                    title=test_deets["Name"],
                    description=mistune.html(test_deets["Description"]),
                    required_inputs=", ".join(
                        test_deets["Required Inputs"] or ["None"]
                    ),
                    params_table="\n".join(
                        [
                            f"<tr><td>{param}</td><td>{pformat(value, indent=4)}</td></tr>"
                            for param, value in test_deets["Params"].items()
                        ]
                    ),
                    table_display="table" if test_deets["Params"] else "none",
                )
            )
        ],
        titles=[f"{content_type} Block: '{content['content_id']}'"],
    )


def _create_sub_section_widget(sub_sections, section_number):
    if not sub_sections:
        return HTML("<p>Empty Section</p>")

    accordion = Accordion()

    for i, section in enumerate(sub_sections):
        if section["sections"]:
            accordion.children = (
                *accordion.children,
                _create_sub_section_widget(
                    section["sections"], section_number=f"{section_number}.{i + 1}"
                ),
            )
        elif contents := section.get("contents", []):
            contents_widget = VBox(
                [_create_content_widget(content) for content in contents]
            )

            accordion.children = (
                *accordion.children,
                contents_widget,
            )
        else:
            accordion.children = (*accordion.children, HTML("<p>Empty Section</p>"))

        accordion.set_title(
            i, f"{section_number}.{i + 1}. {section['title']} ('{section['id']}')"
        )

    return accordion


def _create_section_widget(tree):
    widget = Accordion()
    for i, section in enumerate(tree):
        sub_widget = None
        if section.get("sections"):
            sub_widget = _create_sub_section_widget(section["sections"], i + 1)

        if section.get("contents"):
            contents_widget = VBox(
                [_create_content_widget(content) for content in section["contents"]]
            )
            if sub_widget:
                sub_widget.children = (
                    *sub_widget.children,
                    contents_widget,
                )
            else:
                sub_widget = contents_widget

        if not sub_widget:
            sub_widget = HTML("<p>Empty Section</p>")

        widget.children = (*widget.children, sub_widget)
        widget.set_title(i, f"{i + 1}. {section['title']} ('{section['id']}')")

    return widget


def preview_template(template):
    """Preview a template in Jupyter Notebook

    Args:
        template (dict): The template to preview
    """
    if not is_notebook():
        logger.warning("preview_template() only works in Jupyter Notebook")
        return

    display(
        _create_section_widget(_convert_sections_to_section_tree(template["sections"]))
    )


def _get_section_tests(section):
    """
    Get all the tests in a section and its subsections.

    Args:
        section: A dictionary representing a section.

    Returns:
        A list of tests in the section.
    """
    tests = [
        {
            "id": content["content_id"],
            "output_template": content.get("output_template"),
        }
        for content in section.get("contents", [])
        if content["content_type"] in ["metric", "test"]
    ]

    for sub_section in section["sections"]:
        tests.extend(_get_section_tests(sub_section))

    return tests


def _create_test_suite_section(section):
    """Create a section object for a test suite that contains the tests in a section
    in the template

    Args:
        section: a section of a template (in tree form)

    Returns:
        A TestSuite section dict
    """
    if section_tests := _get_section_tests(section):
        return {
            "section_id": section["id"],
            "section_description": section["title"],
            "section_tests": section_tests,
        }


def _create_template_test_suite(template, section=None):
    """
    Create and run a test suite from a template.

    Args:
        template: A valid flat template
        section: The section of the template to run (if not provided, run all sections)

    Returns:
        A dynamically-create TestSuite Class
    """
    section_tree = _convert_sections_to_section_tree(
        sections=template["sections"],
        start_section_id=section,
    )

    # dynamically create a TestSuite class using `type` and populate it with the tests
    return type(
        f"{template['template_name'].title().replace(' ', '')}TestSuite",
        (TestSuite,),
        {
            "suite_id": template["template_id"],
            "tests": [
                section_dict
                for section in section_tree
                if (section_dict := _create_test_suite_section(section)) is not None
            ],
            "__doc__": template["description"],
        },
    )


def get_template_test_suite(template, section=None):
    """Get a TestSuite instance containing all tests in a template

    This function will collect all tests used in a template into a dynamically-created
    TestSuite object

    Args:
        template: A valid flat template
        section: The section of the template to run (if not provided, run all sections)

    Returns:
        The TestSuite instance
    """
    return _create_template_test_suite(template, section)()
