"""
Checks if any notebook in the notebooks directory contains printed outputs.

This script is run as part of the CI pipeline to ensure that no notebooks
contain printed outputs. If any printed outputs are detected, the script
exits with a non-zero exit code, which causes the CI pipeline to fail.
"""

import os

import nbformat

# Scan the notebooks directory
notebooks_directory = os.path.join(os.getcwd(), "notebooks")

# These notebooks should be allowed to have printed outputs since they do
# not attempt to make a network connection to ValidMind
ALLOWED_PRINTED_OUTPUTS = [
    "explore_test_suites.ipynb",
    "explore_tests.ipynb",
]
SKIP_DIRS = ["scratch"]


def check_notebook(root, file, should_have_printed_outputs=False):
    notebook_error = False

    # Read the contents of the file
    with open(os.path.join(root, file), "r") as f:
        nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)

    has_printed_outputs = False

    # Loop through the cells in the notebook
    for i, cell in enumerate(nb.cells):
        cell_content = cell.source

        # Check if attribute outputs exists:
        if (
            hasattr(cell, "outputs")
            and should_have_printed_outputs is False
            and len(cell.outputs) > 0
        ):
            print(
                f"Printed output detected in:\n\t[{file}][Cell #{i+1}] {cell_content}\n"
            )
            notebook_error = True

        # Check if it should have printed outputs and has at least one.
        if (
            hasattr(cell, "outputs")
            and should_have_printed_outputs is True
            and len(cell.outputs) > 0
        ):
            has_printed_outputs = True

    if should_have_printed_outputs and has_printed_outputs is False:
        print(f"Found a notebook that should have printed outputs:\n\t[{file}]\n")
        notebook_error = True

    return notebook_error


any_error = False

for root, dirs, files in os.walk(notebooks_directory):
    for file in files:
        if any([d in root for d in SKIP_DIRS]):
            continue

        if file.endswith(".ipynb") and ".ipynb_checkpoints" not in root:
            notebook_error = check_notebook(
                root,
                file,
                should_have_printed_outputs=(file in ALLOWED_PRINTED_OUTPUTS),
            )
            any_error = any_error or notebook_error

if any_error:
    raise Exception(
        """
        Detected output issues in at least one notebook.
        To fix these issues:

        - Remove all printed outputs from problematic notebooks
        - Ensure notebooks that should have an output are executed and saved
        """
    )

print("No printed outputs detected in notebooks.")
