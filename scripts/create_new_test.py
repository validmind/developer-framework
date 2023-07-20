# This software is proprietary and confidential. Unauthorized copying,
# modification, distribution or use of this software is strictly prohibited.
# Please refer to the LICENSE file in the root directory of this repository
# for more information.
#
# (c) 2023 ValidMind Inc. All rights reserved.

"""CLI Tool for generating new test modules

Usage:
    python scripts/create_new_test.py --help
    python scripts/create_new_test.py --test_type <test_type> --test_id <test_id>
    python scripts/create_new_test.py  # (prompts for test_type and test_id)

    e.g. python scripts/create_new_test.py --test_type metric --test_id validmind.data_validation.MyCoolMetric
"""

import os
import click
from pathlib import Path


def _camel_to_snake(name):
    """Convert a CamelCase name to snake_case"""
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


@click.command()
@click.option("--test_type", prompt="Test type", help="Type of the test.")
@click.option("--test_id", prompt="Test ID", help="ID of the test.")
def generate_test(test_type, test_id):
    """Generate a Python module based on a template file"""

    # Split test_id into organization, category, and test_name
    parts = test_id.split(".")
    organization, category_parts, test_name = parts[0], parts[1:-1], parts[-1]

    # Create the directory path based on test_id and test_type
    dir_path = os.path.join(organization, "tests", *category_parts)

    # Make directories if they don"t exist
    os.makedirs(dir_path, exist_ok=True)

    # Create the output file path
    file_path = os.path.join(dir_path, f"{test_name}.py")

    # Load the template
    self_path = Path(__file__).parent
    template_path = os.path.join(self_path, "test_templates", f"{test_type}.py")
    with open(template_path, "r") as f:
        template_content = f.read()

    # Render the template with the provided test_name
    generated_test = template_content.replace("__TEST_NAME__", test_name).replace(
        "__TEST_ID__", _camel_to_snake(test_name)
    )

    # Write the output file
    with open(file_path, "w") as f:
        f.write(generated_test)

    click.echo(f"Test module generated at: {file_path}")


if __name__ == "__main__":
    generate_test()
