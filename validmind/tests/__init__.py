# Copyright © 2023 ValidMind Inc. All rights reserved.

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
from ..vm_models import TestContext
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


def _test_description(test_class):
    if len(test_class.__doc__.split("\n")) > 5:
        return test_class.__doc__.strip().split("\n")[0] + "..."

    return test_class.__doc__


def _load_tests(test_ids):
    global __test_classes

    if __test_classes is None:
        __test_classes = {}
        for test_id in test_ids:
            __test_classes[test_id] = load_test(test_id)


def _pretty_list_tests(tests):
    _load_tests(tests)

    table = [
        {
            "Test Type": __test_classes[test_id].test_type,
            "Name": test_id_to_name(test_id),
            "Description": _test_description(__test_classes[test_id]),
            "ID": test_id,
        }
        for test_id in tests
    ]

    return format_dataframe(pd.DataFrame(table))


def list_tests(filter=None, task=None, tags=None, pretty=True):
    """List all tests in the tests directory.

    Args:
        filter (str, optional): Find tests where the ID, task_type or tags match the
            filter string. Defaults to None.
        task (str, optional): Find tests that match the task type. Can be used to
            narrow down matches from the filter string. Defaults to None.
        tags (list, optional): Find tests that match list of tags. Can be used to
            narrow down matches from the filter string. Defaults to None.
        pretty (bool, optional): If True, returns a pandas DataFrame with a
            formatted table. Defaults to False.

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
        return _pretty_list_tests(tests)

    return tests


def load_test(test_id, reload=False):  # noqa: C901
    parts = test_id.split(".")

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


def run_test(test_id, *args, **kwargs):
    """
    Run a test by test ID. Any extra arguments will be passed to the test's run method.
    The only special argument is `params` which can be used to override the test's default params.
    """
    TestClass = load_test(test_id, reload=True)

    test_params = kwargs.pop("params", None)
    test_context = TestContext(*args, **kwargs)

    test = TestClass(test_context=test_context, params=test_params)
    test.run()
    test.result.show()

    return test


def register_test_provider(namespace: str, test_provider: ExternalTestProvider) -> None:
    """Register an external test provider

    Args:
        namespace (str): The namespace of the test provider
        test_provider (ExternalTestProvider): The test provider
    """
    __test_providers[namespace] = test_provider
