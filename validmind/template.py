from ipywidgets import Accordion, HTML, VBox
from IPython.display import display

from .logging import get_logger
from .test_plans import list_tests
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
        widget.children = (
            *widget.children,
            _create_sub_section_widget(section["sections"], i + 1),
        )
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


def _get_validmind_tests(pretty=False):
    """
    Get a dictionary of ValidMind tests with the test name as key.

    Args:
        pretty: A flag indicating the output format of the list.

    Returns:
        A dictionary of ValidMind tests.
    """
    return {test.name: test for test in list_tests(pretty)}


def _get_section_tests(section, validmind_tests):
    """
    Get all the tests in a section and its subsections.

    Args:
        section: A dictionary representing a section.
        validmind_tests: A dictionary of ValidMind tests.

    Returns:
        A list of tests in the section.
    """
    tests = []
    for content in section.get("contents", []):
        test = validmind_tests.get(content["content_id"], None)
        if not test:
            continue
        tests.append(test)
    for sub_section in section["sections"]:
        tests.extend(_get_section_tests(sub_section, validmind_tests))
    return tests


def _create_test_plan(section, validmind_tests):
    """
    Create a test plan from a section.

    Args:
        section: A dictionary representing a section.
        validmind_tests: A dictionary of ValidMind tests.

    Returns:
        An instance of a TestPlan.
    """
    section_tests = [
        test
        for sub_section in section["sections"]
        for test in _get_section_tests(sub_section, validmind_tests)
    ]
    if not section_tests:
        return None

    return type(
        f"{section['title'].title().replace(' ', '')}TestPlan",
        (TestPlan,),
        {
            "name": section["id"],
            "required_context": [],  # TODO: infer the required context
            "tests": section_tests,
            "__doc__": section["title"],
        },
    )


def _create_test_suite(template, validmind_tests, vm_dataset, vm_model, suite_config):
    """
    Create and run a test suite from a template.

    Args:
        template: A dictionary representing a template.
        validmind_tests: A dictionary of ValidMind tests.
        vm_dataset: The dataset to use for the test suite.
        vm_model: The model to use for the test suite.
        suite_config: The configuration for the test suite.

    Returns:
        The result of running the test suite.
    """
    tree = _convert_sections_to_section_tree(template["sections"])
    test_plans = [
        plan
        for section in tree
        if (plan := _create_test_plan(section, validmind_tests)) is not None
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
    test_suite_instance = test_suite(
        dataset=vm_dataset, model=vm_model, config=suite_config
    )

    return test_suite_instance.run()


def run_template(template, *args, **kwargs):
    """Run all tests in a template

    This function will collect all tests used in a template into a TestPlan and then
    run the TestPlan as usual.

    Args:
        template: A dictionary representing a template.

    Returns:
        The result of running the test suite.
    """
    validmind_tests = _get_validmind_tests(pretty=False)
    return _create_test_suite(template, validmind_tests, *args, **kwargs)
