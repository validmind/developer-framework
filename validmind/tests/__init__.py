"""All Tests for ValidMind"""

import importlib
from pathlib import Path


def list_tests():
    """List all tests in the tests directory."""
    directories = [p.name for p in Path(__file__).parent.iterdir() if p.is_dir()]

    tests = []

    for d in directories:
        for path in Path(__file__).parent.joinpath(d).glob("**/**/*.py"):
            if path.name.startswith("__"):  # skip __init__.py and other special files
                continue

            if path.parent.parent.stem == d:
                tests.append(f"validmind.{d}.{path.stem}")
            else:
                tests.append(f"validmind.{d}.{path.parent.parent.stem}.{path.stem}")

    return tests


def load_test(test_id):
    parts = test_id.split(".")
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
