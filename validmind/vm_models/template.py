from ipywidgets import Accordion, HTML, VBox
from IPython.display import display

from ..logging import get_logger

logger = get_logger(__name__)

content_html = """
<div class="lm-Widget p-Widget jupyter-widget-Collapse jupyter-widget-Accordion-child">
    <div class="lm-Widget p-Widget jupyter-widget-Collapse-header">
        <span>Content Block: '{content_id}' <i>({content_type})</i></span>
    </div>
</div>
"""


def _convert_sections_to_section_tree(sections, parent_id="_root_"):
    section_tree = []

    for section in sections:
        section_parent_id = section.get("parent_section", "_root_")
        if section_parent_id == parent_id:
            child_sections = _convert_sections_to_section_tree(sections, section["id"])
            section_tree.append({**section, "sections": child_sections})

    return sorted(section_tree, key=lambda x: x.get("order", 0))


def _create_content_widget(content):
    return HTML(
        content_html.format(
            content_id=content["content_id"],
            content_type=content["content_type"],
        )
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
        widget.children = (
            *widget.children,
            _create_sub_section_widget(section["sections"], i + 1),
        )
        widget.set_title(i, f"{i + 1}. {section['title']}")
    return widget


def preview_template(template):
    display(
        _create_section_widget(_convert_sections_to_section_tree(template["sections"]))
    )
