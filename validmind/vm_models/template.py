import markdown

from ipywidgets import Accordion, HTML, VBox
from IPython.display import display

from ..logging import get_logger

logger = get_logger(__name__)

section_html = """
<div class="lm-Widget p-Widget jupyter-widget-Collapse jupyter-widget-Accordion-child">
    <div class="lm-Widget p-Widget jupyter-widget-Collapse-header">
        <span>{title}</span>
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
    return sorted(section_tree, key=lambda x: x["order"])


class Template:
    def __init__(self, sections):
        self.sections = sections

    def _create_content_widget(self, content):
        if content["content_type"] == "metadata_text":
            return HTML(markdown.markdown(content["options"]["default_text"]))
        elif content["content_type"] == "dynamic":
            return HTML(f"<em>Dynamic content: {content['content_id']}</em>")
        elif content["content_type"] == "test":
            return HTML(f"<strong>Test: {content['content_id']}</strong>")
        elif content["content_type"] == "metric":
            return HTML(f"<strong>Metric: {content['content_id']}</strong>")
        else:
            logger.warning(f"Unknown content type: {content['content_type']}")

    def _create_sub_section_widget(self, sections):
        widgets = []

        for section in sections:
            section_widgets = [HTML(section_html.format(title=section["title"]))]

            if section["sections"]:
                section_widgets.append(self._create_section_widget(section["sections"]))

            for content in section.get("contents", []):
                section_widgets.append(self._create_content_widget(content))

            widgets.append(VBox(section_widgets))

        return VBox(widgets)

    def _create_section_widget(self, tree):
        widget = Accordion()

        for i, section in enumerate(tree):
            widget.children = (
                *widget.children,
                self._create_sub_section_widget(section["sections"]),
            )
            widget.set_title(i, section["title"])

        return widget

    def preview(self):
        display(
            self._create_section_widget(
                _convert_sections_to_section_tree(self.sections)
            )
        )
