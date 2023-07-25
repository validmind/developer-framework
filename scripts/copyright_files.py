# This software is proprietary and confidential. Unauthorized copying,
# modification, distribution or use of this software is strictly prohibited.
# Please refer to the LICENSE file in the root directory of this repository
# for more information.
#
# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
This script adds a standard ValidMind copyright
block to all Python files in the package directory.

How to use:
    poetry run python scripts/copyright_files.py
"""

import os

import nbformat

copyright_path = os.path.join(os.getcwd(), "scripts", "copyright.txt")
with open(copyright_path) as f:
    copyright = f.read()

# Scan the Python package directory
package_directory = os.path.join(os.getcwd(), "validmind")

# Scan the notebooks directory
notebooks_directory = os.path.join(os.getcwd(), "notebooks")

# List of file extensions to process
extensions = [".py", ".ipynb"]


def copyright_python_file(root, file):
    # Check if the file is __init__.py and if it's empty
    if file == "__init__.py":
        with open(os.path.join(root, file), "r") as f:
            contents = f.read()
        if not contents.strip():
            return

    # Read the contents of the file
    with open(os.path.join(root, file), "r") as f:
        contents = f.read()

    # Replace the existing copyright text with the new one
    if "This software is proprietary and confidential." in contents:
        start_index = contents.index("# This software is proprietary and confidential.")
        end_index = contents.index("All rights reserved.") + len("All rights reserved.")
        contents = contents[:start_index] + copyright.strip() + contents[end_index:]
    else:
        # Add the copyright block to a file that doesn't have it
        contents = f"{copyright}\n{contents}"

    # Write the modified contents back to the file
    with open(os.path.join(root, file), "w") as f:
        f.write(contents)


def copyright_notebook_file(root, file):
    # Read the contents of the file
    with open(os.path.join(root, file), "r") as f:
        nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)

    # Just override the copyright key on the metadata
    nb.metadata["copyright"] = copyright.strip()

    with open(os.path.join(root, file), "w") as f:
        nbformat.write(nb, f)


# Loop through all files in the directory and its subdirectories
for root, dirs, files in os.walk(package_directory):
    for file in files:
        # Check if the file has a valid extension
        if file.endswith(".py") and file != "__version__.py":
            copyright_python_file(root, file)

# Discuss notebook organization for including 3rd party notebooks
# before adding this change.
#
# for root, dirs, files in os.walk(notebooks_directory):
#     for file in files:
#         if file.endswith(".ipynb"):
#             copyright_notebook_file(root, file)
