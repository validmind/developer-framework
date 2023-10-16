import os

import click
import dotenv
import nbformat
import papermill as pm

dotenv.load_dotenv()

NOTEBOOKS_TO_RUN = [
    {
        "path": "notebooks/code_samples/quickstart_customer_churn_full_suite.ipynb",
        "project": "clnt1f4qc00ap15lfts8ur7lw",
    },
    "notebooks/code_samples/time_series/tutorial_time_series_forecasting.ipynb",
    "notebooks/code_samples/regression/quickstart_regression_full_suite.ipynb",
    {
        "path": "notebooks/code_samples/custom_tests/external_test_providers_demo.ipynb",
        "project": "clnt1pypw00o415lfjj78fkgl",
    },
]

DEFAULT_PROJECT_ID = "clnt1f4qc00ap15lfts8ur7lw"

INIT_CELL_CODE = """
import validmind as vm

vm.init(
  api_host = "https://api.dev.vm.validmind.ai/api/v1/tracking",
  api_key = "{api_key}",
  api_secret = "{api_secret}",
  project = "{project_id}"
)
"""


@click.command()
@click.option(
    "--kernel", default="python3", help="Kernel to use when executing notebooks."
)
def main(kernel):
    """Run notebooks from the specified directory for end-to-end testing."""
    for notebook_file in NOTEBOOKS_TO_RUN:
        if isinstance(notebook_file, dict):
            notebook_path = os.path.join(os.getcwd(), notebook_file["path"])
            project_id = notebook_file["project"]
        else:
            notebook_path = os.path.join(os.getcwd(), notebook_file)
            project_id = DEFAULT_PROJECT_ID

        backup_notebook(notebook_path)

        try:
            update_vm_init_cell(notebook_path, project_id)
            click.echo(f"Executing {notebook_path} ...")
            run_notebook(notebook_path, kernel)
            click.echo(f"Finished executing {notebook_path}.")
        except Exception as e:
            click.echo(f"Error running {notebook_path}: {e}")

        restore_notebook(notebook_path)


def run_notebook(notebook_path, kernel_name):
    output_path = notebook_path.replace(".ipynb", ".out.ipynb")
    pm.execute_notebook(notebook_path, output_path, kernel_name=kernel_name)


def update_vm_init_cell(notebook_path, project_id):
    api_key = os.getenv("NOTEBOOK_RUNNER_API_KEY")
    api_secret = os.getenv("NOTEBOOK_RUNNER_API_SECRET")

    init_code = INIT_CELL_CODE.format(
        api_key=api_key,
        api_secret=api_secret,
        project_id=project_id,
    )

    with open(notebook_path, "r") as f:
        nb = nbformat.read(f, as_version=4)

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            if "import validmind as vm" in cell["source"]:
                cell["source"] = init_code

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
