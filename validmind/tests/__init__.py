"""All Tests for ValidMind"""

import importlib
from pathlib import Path

import pandas as pd


__legacy_mapping = None
__tests = None
__test_classes = None


# TODO: remove this when all templates are updated to new naming convention
def _get_legacy_test(content_id):
    global __legacy_mapping

    # create a mapping from test name (defined in the test class) to test ID
    if __legacy_mapping is None:
        __legacy_mapping = {}
        for test_id in list_tests():
            test = load_test(test_id)
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
            "Test Type": test.test_type,
            "Name": test.__name__,
            "Description": test.__doc__.strip(),
            "ID": test_id,
        }
        for test_id, test in __test_classes.items()
    ]

    return pd.DataFrame(table).style.hide(axis="index")


def list_tests(pretty=False):
    """List all tests in the tests directory.

    Args:
        pretty (bool, optional): If True, returns a pandas DataFrame with a
            formatted table. Defaults to False.

    Returns:
        list or pandas.DataFrame: A list of all tests or a formatted table.
    """
    global __tests
    if __tests is not None:
        return __tests

    __tests = []

    directories = [p.name for p in Path(__file__).parent.iterdir() if p.is_dir()]

    for d in directories:
        for path in Path(__file__).parent.joinpath(d).glob("**/**/*.py"):
            if path.name.startswith("__"):  # skip __init__.py and other special files
                continue

            test_id = (
                f"validmind.{d}.{path.stem}"
                if path.parent.parent.stem == d
                else f"validmind.{d}.{path.parent.parent.stem}.{path.stem}"
            )
            __tests.append(test_id)

    if pretty:
        return _pretty_list_tests(__tests)

    return __tests


def load_test(test_id):
    parts = test_id.split(".")

    # for now this code will handle the legacy test IDs
    # (e.g. "ModelMetadata" instead of "validmind.model_validation.ModelMetadata")
    if len(parts) == 1:
        return load_test(_get_legacy_test(test_id))

    test_org = parts[0]

    if test_org == "validmind":
        test_module = ".".join(parts[1:-1])
        test_class = parts[-1]

        return getattr(
            importlib.import_module(f"validmind.tests.{test_module}"),
            test_class,
        )

    else:
        raise ValueError(f"Custom tests are not supported yet")


def describe_test(test_id: str):
    """Returns the test by test ID"""
    if __test_classes is None:
        test = load_test(test_id)
    else:
        test = __test_classes[test_id]

    return pd.DataFrame([
        {
            "Test Type": test.test_type,
            "Name": test.__name__,
            "Description": test.__doc__.strip(),
            "ID": test_id,
        }
    ]).style.hide(axis="index")
