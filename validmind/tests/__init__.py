# Copyright © 2023 ValidMind Inc. All rights reserved.

"""All Tests for ValidMind"""

import importlib
from pathlib import Path
from typing import Dict

import pandas as pd

from ..errors import LoadTestError
from ..logging import get_logger
from ..utils import clean_docstring, format_dataframe
from .__types__ import ExternalTestProvider
from .test_providers import GithubTestProvider, LocalTestProvider

logger = get_logger(__name__)


__all__ = [
    "data_validation",
    "model_validation",
    "list_tests",
    "load_test",
    "describe_test",
    "register_test_provider",
    "GithubTestProvider",
    "LoadTestError",
    "LocalTestProvider",
]

__legacy_mapping = None
__tests = None
__test_classes = None

__test_providers: Dict[str, ExternalTestProvider] = {}


def _test_title(name):
    title = f"{name[0].upper()}"

    for i in range(1, len(name)):
        if name[i].isupper() and (
            name[i - 1].islower() or (i + 1 < len(name) and name[i + 1].islower())
        ):
            title += " "
        title += name[i]

    return title


# TODO: remove this when all templates are updated to new naming convention
def _get_legacy_test(content_id):
    global __legacy_mapping

    # create a mapping from test name (defined in the test class) to test ID
    if __legacy_mapping is None:
        __legacy_mapping = {}
        for test_id in list_tests(pretty=False):
            try:
                test = load_test(test_id, legacy=True)
            except LoadTestError:
                continue

            __legacy_mapping[test.name] = test_id

    try:
        return __legacy_mapping[content_id]
    except KeyError:
        raise LoadTestError(
            f"Unable to load test {content_id}. "
            f"Test not found or there was an error loading the test."
        )


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
            "Name": _test_title(__test_classes[test_id].__name__),
            "Description": clean_docstring(
                __test_classes[test_id].description(__test_classes[test_id])
            )
            if hasattr(__test_classes[test_id], "description")
            else "",
            "ID": test_id,
        }
        for test_id in tests
    ]

    return format_dataframe(pd.DataFrame(table))


def list_tests(filter=None, task=None, pretty=True):
    """List all tests in the tests directory.

    Args:
        filter (str, optional): Find tests where any part of the ID matches the filter
          string. Defaults to None.
        task (str, optional): Find tests that match the task type. Defaults to None.
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

    if task is not None:
        _load_tests(tests)
        tests = [
            test_id
            for test_id in tests
            if hasattr(__test_classes[test_id], "metadata")
            and task in __test_classes[test_id].metadata["task_type"]
        ]

    if filter is not None:
        tests = [test_id for test_id in __tests if filter.lower() in test_id.lower()]

    if pretty:
        return _pretty_list_tests(tests)

    return tests


def load_test(test_id, legacy=False):  # noqa: C901
    parts = test_id.split(".")

    # for now this code will handle the legacy test IDs
    # (e.g. "ModelMetadata" instead of "validmind.model_validation.ModelMetadata")
    if len(parts) == 1:
        return load_test(_get_legacy_test(test_id), legacy=True)

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
            module = importlib.import_module(
                f"validmind.tests.{test_module}.{test_class}"
            )
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

    # TODO: restore non-legacy flag for test IDs once we have a migration plan for existing templates
    # if not legacy:
    #     test._key = test_id

    return test


def describe_test(test_name: str = None, test_id: str = None, raw: bool = False):
    """Returns the test by test ID"""
    matches = []

    if test_name is not None:
        # test_name can be passed as PascalCase or snake_case and test_ids are all
        # PascalCase so we convert test_id and test_name to all lowercase without
        # underscores to check the match.
        test_name = test_name.lower().replace("_", "")
        for test_id in list_tests(pretty=False):
            test_id_lower = test_id.lower().replace("_", "")
            if test_name == test_id_lower or test_id_lower.endswith(test_name):
                matches.append(test_id)
    else:
        matches.append(test_id)

    if len(matches) == 0:
        print(f"No test found with name: {test_name}")
        return
    elif len(matches) > 1:
        print(
            f"Found multiple matches for test name: {', '.join(matches)}. Please specify a unique test name."
        )
        return

    test_id = matches[0]

    if __test_classes is None:
        test = load_test(test_id)
    else:
        test = __test_classes[test_id]

    test_details = {
        "ID": test_id,
        "Name": _test_title(test.__name__),
        "Description": clean_docstring(test.description(test))
        if hasattr(test, "description")
        else "",
        "Test Type": test.test_type,
        "Required Inputs": test.required_inputs,
        "Params": test.default_params or {},
    }

    if raw:
        return test_details

    return format_dataframe(
        pd.DataFrame(
            {
                "": [f"{key}:" for key in test_details.keys()],
                " ": test_details.values(),
            }
        )
    )


def register_test_provider(namespace: str, test_provider: ExternalTestProvider) -> None:
    """Register an external test provider

    Args:
        namespace (str): The namespace of the test provider
        test_provider (ExternalTestProvider): The test provider
    """
    __test_providers[namespace] = test_provider
