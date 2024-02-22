# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""All Tests for ValidMind"""

import importlib
import sys
from pathlib import Path
from pprint import pformat
from typing import Dict

import pandas as pd
from IPython.display import display
from ipywidgets import HTML
from markdown import markdown

from ..errors import LoadTestError
from ..html_templates.content_blocks import test_content_block_html
from ..logging import get_logger
from ..utils import clean_docstring, format_dataframe, fuzzy_match, test_id_to_name
from ..vm_models import TestContext, TestInput
from .__types__ import ExternalTestProvider
from .test_providers import GithubTestProvider, LocalTestProvider

logger = get_logger(__name__)


__all__ = [
    "data_validation",
    "model_validation",
    "prompt_validation",
    "list_tests",
    "load_test",
    "describe_test",
    "register_test_provider",
    "GithubTestProvider",
    "LoadTestError",
    "LocalTestProvider",
]

__tests = None
__test_classes = None

__test_providers: Dict[str, ExternalTestProvider] = {}


def _test_description(test_class, truncate=True):
    if truncate and len(test_class.__doc__.split("\n")) > 5:
        return test_class.__doc__.strip().split("\n")[0] + "..."

    return test_class.__doc__


def _load_tests(test_ids):
    global __test_classes

    if __test_classes is None:
        __test_classes = {}
        for test_id in test_ids:
            __test_classes[test_id] = load_test(test_id)


def _pretty_list_tests(tests, truncate=True):
    _load_tests(tests)

    table = [
        {
            "Test Type": __test_classes[test_id].test_type,
            "Name": test_id_to_name(test_id),
            "Description": _test_description(__test_classes[test_id], truncate),
            "ID": test_id,
        }
        for test_id in tests
    ]

    return format_dataframe(pd.DataFrame(table))


def _initialize_test_classes():
    """
    Initialize and populate the __test_classes global variable.
    """
    global __test_classes

    if __test_classes is None:
        __test_classes = {}
        for path in Path(__file__).parent.glob("**/*.py"):
            if path.name.startswith("__") or not path.name[0].isupper():
                continue  # skip special files and non-class files
            test_id = path.stem  # or any other way to define test_id
            __test_classes[test_id] = load_test(
                test_id
            )  # Assuming a function load_test exists


def list_tags():
    """
    List unique tags from all test classes.
    """
    _initialize_test_classes()

    unique_tags = set()

    for test_class in __test_classes.values():
        if hasattr(test_class, "metadata") and "tags" in test_class.metadata:
            for tag in test_class.metadata["tags"]:
                unique_tags.add(tag)

    return list(unique_tags)


def list_tasks_and_tags():
    """
    List all task types and their associated tags, with one row per task type and
    all tags for a task type in one row.

    Returns:
        pandas.DataFrame: A DataFrame with 'Task Type' and concatenated 'Tags'.
    """
    _initialize_test_classes()
    task_tags_dict = {}

    for test_class in __test_classes.values():
        if hasattr(test_class, "metadata"):
            task_types = test_class.metadata.get("task_types", [])
            tags = test_class.metadata.get("tags", [])

            for task_type in task_types:
                if task_type not in task_tags_dict:
                    task_tags_dict[task_type] = set()
                task_tags_dict[task_type].update(tags)

    # Convert the dictionary into a DataFrame
    task_tags_data = [
        {"Task Type": task_type, "Tags": ", ".join(tags)}
        for task_type, tags in task_tags_dict.items()
    ]
    return format_dataframe(pd.DataFrame(task_tags_data))


def list_task_types():
    """
    List unique task types from all test classes.
    """
    _initialize_test_classes()

    unique_task_types = set()

    for test_class in __test_classes.values():
        if hasattr(test_class, "metadata") and "task_types" in test_class.metadata:
            for task_type in test_class.metadata["task_types"]:
                unique_task_types.add(task_type)

    return list(unique_task_types)


def list_tests(filter=None, task=None, tags=None, pretty=True, truncate=True):
    """List all tests in the tests directory.

    Args:
        filter (str, optional): Find tests where the ID, task_type or tags match the
            filter string. Defaults to None.
        task (str, optional): Find tests that match the task type. Can be used to
            narrow down matches from the filter string. Defaults to None.
        tags (list, optional): Find tests that match list of tags. Can be used to
            narrow down matches from the filter string. Defaults to None.
        pretty (bool, optional): If True, returns a pandas DataFrame with a
            formatted table. Defaults to True.
        truncate (bool, optional): If True, truncates the test description to the first
            line. Defaults to True. (only used if pretty=True)

    Returns:
        list or pandas.DataFrame: A list of all tests or a formatted table.
    """
    global __tests

    if __tests is None:
        __tests = []

        directories = [p.name for p in Path(__file__).parent.iterdir() if p.is_dir()]

        for d in directories:
            for path in Path(__file__).parent.joinpath(d).glob("**/**/*.py"):
                if path.name.startswith("__") or not path.name[0].isupper():
                    continue  # skip __init__.py and other special files as well as non Test files

                test_id = (
                    f"validmind.{d}.{path.parent.stem}.{path.stem}"
                    if path.parent.parent.stem == d
                    else f"validmind.{d}.{path.stem}"
                )
                __tests.append(test_id)

    tests = __tests

    # first filter by the filter string since it's the most general search
    if filter is not None:
        _load_tests(tests)

        matched_by_id = [
            test_id for test_id in tests if filter.lower() in test_id.lower()
        ]
        matched_by_task = [
            test_id
            for test_id in tests
            if hasattr(__test_classes[test_id], "metadata")
            and any(
                filter.lower() in task.lower()
                for task in __test_classes[test_id].metadata["task_types"]
            )
        ]
        matched_by_tags = [
            test_id
            for test_id in tests
            if hasattr(__test_classes[test_id], "metadata")
            and any(
                fuzzy_match(tag, filter.lower())
                for tag in __test_classes[test_id].metadata["tags"]
            )
        ]

        tests = list(set(matched_by_id + matched_by_task + matched_by_tags))

    # then filter by task type and tags since they are more specific
    if task is not None:
        _load_tests(tests)

        tests = [
            test_id
            for test_id in tests
            if hasattr(__test_classes[test_id], "metadata")
            and task in __test_classes[test_id].metadata["task_types"]
        ]

    if tags is not None:
        _load_tests(tests)

        tests = [
            test_id
            for test_id in tests
            if hasattr(__test_classes[test_id], "metadata")
            and all(tag in __test_classes[test_id].metadata["tags"] for tag in tags)
        ]

    if pretty:
        return _pretty_list_tests(tests, truncate=truncate)

    return tests


def load_test(test_id, reload=False):  # noqa: C901
    # Extract the test ID extension from the actual test ID when loading
    # the test class. This enables us to generate multiple results for
    # the same tests within the document. For instance, consider the
    # test ID "validmind.data_validation.ClassImbalance:data_id_1,"
    # where the test ID extension is "data_id_1".
    parts = test_id.split(":")[0].split(".")

    error = None
    namespace = parts[0]

    if namespace != "validmind" and namespace not in __test_providers:
        error = (
            f"Unable to load test {test_id}. "
            f"No Test Provider found for the namespace: {namespace}."
        )

    if namespace == "validmind":
        test_module = ".".join(parts[1:-1])
        test_class = parts[-1]

        try:
            full_path = f"validmind.tests.{test_module}.{test_class}"

            if reload and full_path in sys.modules:
                module = importlib.reload(sys.modules[full_path])
            else:
                module = importlib.import_module(full_path)

            test = getattr(module, test_class)
        except ModuleNotFoundError as e:
            error = f"Unable to load test {test_id}. {e}"
        except AttributeError:
            error = f"Unable to load test {test_id}. Class not in module: {test_class}"

    elif namespace in __test_providers:
        try:
            test = __test_providers[namespace].load_test(test_id.split(".", 1)[1])
        except Exception as e:
            error = (
                f"Unable to load test {test_id} from test  provider: "
                f"{__test_providers[namespace]}\n Got Exception: {e}"
            )

    if error:
        logger.error(error)
        raise LoadTestError(error)

    test.test_id = test_id

    return test


def describe_test(test_id: str = None, raw: bool = False):
    """Get or show details about the test

    This function can be used to see test details including the test name, description,
    required inputs and default params. It can also be used to get a dictionary of the
    above information for programmatic use.

    Args:
        test_id (str, optional): The test ID. Defaults to None.
        raw (bool, optional): If True, returns a dictionary with the test details.
            Defaults to False.
    """
    test = load_test(test_id)

    details = {
        "ID": test_id,
        "Name": test_id_to_name(test_id),
        "Test Type": test.test_type,
        "Required Inputs": test.required_inputs,
        "Params": test.default_params or {},
        "Description": clean_docstring(test.__doc__),
    }

    if raw:
        return details

    display(
        HTML(
            test_content_block_html.format(
                title=f'{details["Name"]}',
                description=markdown(details["Description"]),
                required_inputs=", ".join(details["Required Inputs"] or ["None"]),
                params_table="\n".join(
                    [
                        f"<tr><td>{param}</td><td>{pformat(value, indent=4)}</td></tr>"
                        for param, value in details["Params"].items()
                    ]
                ),
                table_display="table" if details["Params"] else "none",
            )
        )
    )


def run_test(test_id, params: dict = None, inputs=None, output_template=None, **kwargs):
    """Run a test by test ID

    Args:
        test_id (str): The test ID
        params (dict, optional): A dictionary of params to override the default params
        inputs: A dictionary of test inputs to pass to the Test
        output_template (str, optional): A template to use for customizing the output
        **kwargs: Any extra arguments will be passed in via the TestInput object. i.e.:
            - dataset: A validmind Dataset object or a Pandas DataFrame
            - model: A model to use for the test
            - models: A list of models to use for the test
            other inputs can be accessed inside the test via `self.inputs["input_name"]`
    """
    TestClass = load_test(test_id, reload=True)
    test = TestClass(
        test_id=test_id,
        context=TestContext(),
        inputs=TestInput({**kwargs, **(inputs or {})}),
        output_template=output_template,
        params=params,
    )

    test.run()
    test.result.show()

    return test.result


def register_test_provider(namespace: str, test_provider: ExternalTestProvider) -> None:
    """Register an external test provider

    Args:
        namespace (str): The namespace of the test provider
        test_provider (ExternalTestProvider): The test provider
    """
    __test_providers[namespace] = test_provider
