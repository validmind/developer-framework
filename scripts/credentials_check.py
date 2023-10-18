"""
Checks if any notebook in the notebooks directory contains credentials.
"""

import os
import re

import nbformat

# Scan the notebooks directory
notebooks_directory = os.path.join(os.getcwd(), "notebooks")


def contains_actual_credentials(code):
    patterns = [
        r"api_key\s*=\s*[\"\']\w+[\"\']",
        r"api_secret\s*=\s*[\"\']\w+[\"\']",
    ]

    return any(re.search(pattern, code) for pattern in patterns)


def check_notebook(root, file):
    notebook_error = False

    # Read the contents of the file
    with open(os.path.join(root, file), "r") as f:
        nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)

    # Loop through the cells in the notebook
    for i, cell in enumerate(nb.cells):
        cell_content = cell.source

        # Check for vm.init call
        if "vm.init(" in cell_content and contains_actual_credentials(cell_content):
            notebook_error = True
            print(
                f"Potential clear text credentials detected in Cell {i+1} for notebook {root}/{file}"
            )

    return notebook_error


any_error = False

for root, dirs, files in os.walk(notebooks_directory):
    for file in files:
        if file.endswith(".ipynb") and ".ipynb_checkpoints" not in root:
            notebook_error = check_notebook(root, file)
            any_error = any_error or notebook_error

if any_error:
    print("Potential clear text credentials detected in at least one notebook.")
    os._exit(1)

print("No clear text credentials detected in notebooks.")
