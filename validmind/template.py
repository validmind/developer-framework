from ipywidgets import Accordion, HTML, VBox
from IPython.display import display

from .logging import get_logger
from .utils import is_notebook
from .vm_models.test_plan import TestPlan
from .vm_models.test_suite import TestSuite

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
        widget.set_title(i, f"{i + 1}. {section['title']}")

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
        # {
        #     "ref_id": f"{section['id']}:{content['content_id']}",
        #     "test_id": content["content_id"],
        # }  # we will need this mechanism for tagging with section id
        content["content_id"]
        for content in section.get("contents", [])
        if content["content_type"] in ["metric", "test"]
    ]

    for sub_section in section["sections"]:
        tests.extend(_get_section_tests(sub_section))

    return tests


def _create_section_test_plan(section):
    """Create a test plan for a section in a template

    Args:
        section: a section of a template (in tree form)

    Returns:
        A dynamically-created TestPlan Class
    """
    section_tests = _get_section_tests(section)

    if section_tests:
        return type(
            f"{section['title'].title().replace(' ', '')}TestPlan",
            (TestPlan,),
            {
                "name": section["id"],
                "required_context": [],
                "tests": section_tests,
                "__doc__": section["title"],
            },
        )


def _create_template_test_suite(template):
    """
    Create and run a test suite from a template.

    Args:
        template: A valid flat template

    Returns:
        A dynamically-create TestSuite Class
    """
    tree = _convert_sections_to_section_tree(template["sections"])
    test_plans = [
        plan
        for section in tree
        if (plan := _create_section_test_plan(section)) is not None
    ]
    test_suite = type(
        f"{template['template_name'].title().replace(' ', '')}TestSuite",
        (TestSuite,),
        {
            "name": template["template_id"],
            "required_context": [],
            "test_plans": test_plans,
            "__doc__": template["description"],
        },
    )

    return test_suite


def run_template(template, *args, **kwargs):
    """Run all tests in a template

    This function will collect all tests used in a template into a TestPlan and then
    run the TestPlan as usual.

    Args:
        template: A valid flat template
        *args: Arguments to pass to the TestSuite
        **kwargs: Keyword arguments to pass to the TestSuite

    Returns:
        The result of running the test suite.
    """
    test_suite = _create_template_test_suite(template)
    test_suite_instance = test_suite(*args, **kwargs)

    return test_suite_instance.run()
