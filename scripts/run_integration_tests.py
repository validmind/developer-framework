"""
This script will run notebooks from the `notebooks` directory that will do end-to-end testing of the ValidMind Developer Framework

Usage:
    python run_integration_tests.py
"""

import os

import nbformat
import papermill as pm


def run_notebook(notebook_path):
    pm.execute_notebook(notebook_path, notebook_path)


def update_vm_init_cell(notebook_path):
    with open(notebook_path, "r") as f:
        nb = nbformat.read(f, as_version=4)

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            if "import validmind as vm" in cell["source"]:
                cell["source"] = cell["source"].replace(
                    "import validmind as vm",
                    "import validmind as vm\n\nvm.init(api_host='http://localhost:5000/api/v1/tracking/tracking', api_key='test', api_secret='test', project='test')",
                )

    with open(notebook_path, "w") as f:
        nbformat.write(nb, f)
