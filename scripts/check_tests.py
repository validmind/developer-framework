"""
This software is proprietary and confidential. Unauthorized copying,
modification, distribution or use of this software is strictly prohibited.
Please refer to the LICENSE file in the root directory of this repository
for more information.

(c) 2023 ValidMind Inc. All rights reserved.
"""

"""CLI Tool for checking if all tests in a file exist in the tests folder

Usage:
    python scripts/check_tests.py --input_file <input_file>
Example:
    python scripts/check_tests.py --input_file validmind/data_validation/metrics.py
"""

import importlib

import click

from validmind.tests import list_tests


@click.command()
@click.option(
    "--input_file", prompt="File to check", help="File to check against tests directory"
)
def check_tests(input_file):
    """Check if all tests in a file exist in the tests folder"""

    # load the input file and extract all classes
    input_module = importlib.import_module(
        input_file.replace("/", ".").replace(".py", "")
    )
    all_classes = [
        getattr(input_module, name) for name in dir(input_module) if name[0].isupper()
    ]
    test_classes = [
        cls
        for cls in all_classes
        if cls.__module__.startswith(input_file.replace("/", ".").replace(".py", ""))
    ]
    test_names = [cls.__name__ for cls in test_classes]

    click.echo(f"Found {len(test_classes)} classes in {input_file}")

    tests = [test.split(".")[-1] for test in list_tests(pretty=False)]

    missing_tests = []
    for test_name in test_names:
        if test_name not in tests:
            missing_tests.append(test_name)

    if len(missing_tests) > 0:
        click.echo(f"Missing {len(missing_tests)} tests:")
        for test in missing_tests:
            click.echo(f"  {test}")
    else:
        click.echo("All tests found!")


if __name__ == "__main__":
    check_tests()
