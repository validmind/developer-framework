"""
This script adds a standard ValidMind copyright
block to all Python files in the package directory.

How to use:
    poetry run python scripts/copyright_files.py
"""

import os

copyright = """
This software is proprietary and confidential. Unauthorized copying,
modification, distribution or use of this software is strictly prohibited.
Please refer to the LICENSE file in the root directory of this repository
for more information.

(c) 2023 ValidMind Inc. All rights reserved.
"""

# Scan the Python package directory
directory = os.path.join(os.getcwd(), "..", "validmind")

# List of file extensions to process
extensions = [".py"]

# Loop through all files in the directory and its subdirectories
for root, dirs, files in os.walk(directory):
    for file in files:
        # Check if the file has a valid extension
        if file.endswith(tuple(extensions)):
            # Read the contents of the file
            with open(os.path.join(root, file), "r") as f:
                contents = f.read()
            # Add the copyright block to the contents
            contents = f"{copyright}\n{contents}"
            # Write the modified contents back to the file
            with open(os.path.join(root, file), "w") as f:
                f.write(contents)
