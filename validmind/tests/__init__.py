"""All Tests for ValidMind"""

import importlib
from pathlib import Path
from typing import Dict

import pandas as pd

from ..errors import LoadTestError
from ..logging import get_logger
from ..utils import format_dataframe
from .__types__ import ExternalTestProvider
from .test_providers import GithubTestProvider, LocalTestProvider


logger = get_logger(__name__)


__all__ = [
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


# TODO: remove this when all templates are updated to new naming convention
def _get_legacy_test(content_id):
    global __legacy_mapping

    # create a mapping from test name (defined in the test class) to test ID
    if __legacy_mapping is None:
        __legacy_mapping = {}
        for test_id in list_tests(pretty=False):
            test = load_test(test_id, legacy=True)
            __legacy_mapping[test.name] = test_id

    return __legacy_mapping[content_id]


def _pretty_list_tests(tests):
    global __test_classes

    if __test_classes is None:
        __test_classes = {}
        for test_id in tests:
            __test_classes[test_id] = load_test(test_id)

    table = [
        {
            "Test Type": __test_classes[test_id].test_type,
            "Name": __test_classes[test_id].__name__,
            "Description": __test_classes[test_id].__doc__.strip(),
            "ID": test_id,
        }
        for test_id in tests
    ]

    return format_dataframe(pd.DataFrame(table))


def list_tests(filter=None, pretty=True):
    """List all tests in the tests directory.

    Args:
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
                if path.name.startswith("__"):
                    continue  # skip __init__.py and other special files

                test_id = (
                    f"validmind.{d}.{path.parent.stem}.{path.stem}"
                    if path.parent.parent.stem == d
                    else f"validmind.{d}.{path.stem}"
                )
                __tests.append(test_id)

    if filter is not None:
        tests = [test_id for test_id in __tests if filter.lower() in test_id.lower()]
    else:
        tests = __tests

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
        except ModuleNotFoundError:
            error = f"Unable to load test {test_id}. Module not found: {test_module}"
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


def describe_test(test_name: str = None, test_id: str = None):
    """Returns the test by test ID"""
    if test_name is not None:
        # TODO: we should rethink this a bit
        for test_id in list_tests(pretty=False):
            if test_id.endswith(test_name):
                break

    if __test_classes is None:
        test = load_test(test_id)
    else:
        test = __test_classes[test_id]

    return format_dataframe(
        pd.DataFrame(
            [
                {
                    "ID": test_id,
                    "Test Type": test.test_type,
                    "Name": test.__name__,
                    "Description": test.__doc__.strip(),
                }
            ]
        )
    )


def register_test_provider(namespace: str, test_provider: ExternalTestProvider) -> None:
    """Register an external test provider

    Args:
        namespace (str): The namespace of the test provider
        test_provider (ExternalTestProvider): The test provider
    """
    __test_providers[namespace] = test_provider
