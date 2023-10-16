import os

import click
import nbformat
import papermill as pm

NOTEBOOKS_TO_RUN = [
    "notebooks/code_samples/quickstart_customer_churn_full_suite.ipynb",
    "notebooks/code_samples/time_series/tutorial_time_series_forecasting.ipynb",
    "notebooks/code_samples/regression/quickstart_regression_full_suite.ipynb",
    "notebooks/code_samples/custom_tests/external_test_providers_demo.ipynb",
]

INIT_CELL_CODE = """
import validmind as vm

vm.init(
  api_host = "http://localhost:3000/api/v1/tracking",
  api_key = "9ebdb4ae381178f15fe09aa6ca6749d2",
  api_secret = "4e9471d9a54d9db736caa053b6f705d40885cd3822accbb55ca371acbd3d0b3a",
  project = "cln9pes5900010wryh94c4q5j"
)
"""


@click.command()
@click.option(
    "--kernel", default="python3", help="Kernel to use when executing notebooks."
)
def main(kernel):
    """Run notebooks from the specified directory for end-to-end testing."""
    for notebook_file in NOTEBOOKS_TO_RUN:
        notebook_path = os.path.join(os.getcwd(), notebook_file)

        backup_notebook(notebook_path)

        try:
            update_vm_init_cell(notebook_path)
            click.echo(f"Executing {notebook_file} ...")
            run_notebook(notebook_path, kernel)
            click.echo(f"Finished executing {notebook_file}.")
        except Exception as e:
            click.echo(f"Error running {notebook_file}: {e}")

        restore_notebook(notebook_path)


def run_notebook(notebook_path, kernel_name):
    output_path = notebook_path.replace(".ipynb", ".out.ipynb")
    pm.execute_notebook(notebook_path, output_path, kernel_name=kernel_name)


def update_vm_init_cell(notebook_path):
    with open(notebook_path, "r") as f:
        nb = nbformat.read(f, as_version=4)
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            if "import validmind as vm" in cell["source"]:
                cell["source"] = INIT_CELL_CODE
    with open(notebook_path, "w") as f:
        nbformat.write(nb, f)


def backup_notebook(notebook_path):
    backup_path = f"{notebook_path}.backup"
    if os.path.exists(backup_path):
        os.remove(backup_path)
    os.system(f"cp {notebook_path} {backup_path}")


def restore_notebook(notebook_path):
    backup_path = f"{notebook_path}.backup"
    os.rename(backup_path, notebook_path)


if __name__ == "__main__":
    main()
