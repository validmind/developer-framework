"""Script to run notebooks for integration testing the dev framework.

Usage:
    python scripts/run_e2e_notebooks.py

Note: This script is meant to be run from the root of the repo

Notebooks Tested:
 - notebooks/code_samples/quickstart_customer_churn_full_suite.ipynb
 - notebooks/code_samples/time_series/tutorial_time_series_forecasting.ipynb
 - notebooks/code_samples/regression/quickstart_regression_full_suite.ipynb
 - notebooks/code_samples/custom_tests/external_test_providers.ipynb

To add more notebooks to the list, simply add the path to the `NOTEBOOKS_TO_RUN` list.
This will use the default project id for the notebook. If you want to use a different
project/template, you can specify it as a dictionary with the keys `path` and `project`
where `path` is the path to the notebook and `project` is the project id.

Note: This script requires the following environment variables to be set:
    - NOTEBOOK_RUNNER_API_KEY (api key for the project)
    - NOTEBOOK_RUNNER_API_SECRET (api secret for the project)

This uses the dev environment for now... In the future, we may want to change this???
"""

import os

import click
import dotenv
import nbformat
import papermill as pm

dotenv.load_dotenv()

DEFAULT_PROJECT_ID = os.getenv(
    "NOTEBOOK_RUNNER_DEFAULT_PROJECT_ID", "clnt1f4qc00ap15lfts8ur7lw"
)

NOTEBOOKS_TO_RUN = [
    {
        "path": "notebooks/code_samples/quickstart_customer_churn_full_suite.ipynb",
        "project": DEFAULT_PROJECT_ID,
    },
    "notebooks/code_samples/time_series/tutorial_time_series_forecasting.ipynb",
    # "notebooks/code_samples/regression/quickstart_regression_full_suite.ipynb",
    # TODO: fix the above when we have a regression template installed
    "notebooks/how_to/run_unit_metrics.ipynb",
    "notebooks/code_samples/custom_tests/external_test_providers.ipynb",
    "notebooks/code_samples/custom_tests/implementing_custom_tests.ipynb",
]

INIT_CELL_CODE = """
import validmind as vm

vm.init(
  api_host = "{api_host}",
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
            click.echo(f"\n -------- Executing {notebook_path} ---------- \n")
            run_notebook(notebook_path, kernel)
            click.echo(f" -------- Finished executing {notebook_path} ---------- \n")
        except Exception as e:
            click.echo(f"Error running {notebook_path}: {e}")
            os.remove(notebook_path.replace(".ipynb", ".out.ipynb"))
            restore_notebook(notebook_path)
            raise e

        restore_notebook(notebook_path)


def run_notebook(notebook_path, kernel_name):
    output_path = notebook_path.replace(".ipynb", ".out.ipynb")

    is_gh_actions = os.getenv("GITHUB_ACTIONS") == "true"

    pm.execute_notebook(
        input_path=notebook_path,
        output_path=output_path,
        kernel_name=kernel_name,
        log_output=is_gh_actions,
        progress_bar=(not is_gh_actions),
        cwd=os.path.dirname(notebook_path),
    )

    # comment out the below line to see output notebook for debugging
    os.remove(output_path)


def update_vm_init_cell(notebook_path, project_id):
    api_host = os.getenv(
        "NOTEBOOK_RUNNER_API_HOST", "https://api.dev.vm.validmind.ai/api/v1/tracking"
    )
    api_key = os.getenv("NOTEBOOK_RUNNER_API_KEY")
    api_secret = os.getenv("NOTEBOOK_RUNNER_API_SECRET")

    init_code = INIT_CELL_CODE.format(
        api_host=api_host,
        api_key=api_key,
        api_secret=api_secret,
        project_id=project_id,
    )

    with open(notebook_path, "r") as f:
        nb = nbformat.read(f, as_version=4)

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            if (
                "import validmind as vm" in cell["source"]
                and "vm.init(" in cell["source"]
            ):
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
