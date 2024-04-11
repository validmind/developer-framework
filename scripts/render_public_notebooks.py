"""Script to render all notebooks intended for end user documentation.

Usage:
    python scripts/render_public_notebooks.py

Note: This script is meant to be run from the root of the repo

This script will run through every notebook in the following directories:
- notebooks/code_samples/
- notebooks/how_to/
- notebooks/tutorials/

We assume most notebooks are based on the sample Customer Churn model (binary classification),
so we have additional project IDs for models that use a different template.

Note: This script requires the following environment variables to be set:
    - NOTEBOOK_RUNNER_API_KEY (api key for the project)
    - NOTEBOOK_RUNNER_API_SECRET (api secret for the project)

This uses the dev environment for now
"""

import os

import click
import dotenv
import nbformat

dotenv.load_dotenv()

# Customer churn
DEFAULT_PROJECT_ID = os.getenv(
    "NOTEBOOK_RUNNER_DEFAULT_PROJECT_ID", "cltnl29bz00051omgwepjgu1r"
)
TIME_SERIES_PROJECT_ID = os.getenv(
    "NOTEBOOK_RUNNER_TIME_SERIES_PROJECT_ID", "cltnl8c7v001j1omgyzmjrzhj"
)
REGRESSION_PROJECT_ID = os.getenv(
    "NOTEBOOK_RUNNER_REGRESSION_PROJECT_ID", "cltnl7t6t000x1omg706sdv0j"
)
LLM_CLASSIFICATION_PROJECT_ID = os.getenv(
    "NOTEBOOK_RUNNER_LLM_CLASSIFICATION_PROJECT_ID", "cluue3sym011p1pl6mx3snow4"
)
LLM_SUMMARIZATION_PROJECT_ID = os.getenv(
    "NOTEBOOK_RUNNER_LLM_SUMMARIZATION_PROJECT_ID", "cluue49ou01241pl6v0en39ew"
)
NLP_CLASSIFICATION_PROJECT_ID = os.getenv(
    "NOTEBOOK_RUNNER_NLP_CLASSIFICATION_PROJECT_ID", "cluue525p012i1pl6z6pm0d0b"
)
NLP_SUMMARIZATION_PROJECT_ID = os.getenv(
    "NOTEBOOK_RUNNER_NLP_SUMMARIZATION_PROJECT_ID", "cluue5l38012x1pl6hszgl2oo"
)

# Register new notebooks here when they get added to the repo
NOTEBOOK_PROJECT_ID_MAP = {
    "tutorial_time_series_forecasting.ipynb": TIME_SERIES_PROJECT_ID,
    "quickstart_regression_full_suite.ipynb": REGRESSION_PROJECT_ID,
    "foundation_models_integration_demo.ipynb": LLM_CLASSIFICATION_PROJECT_ID,
    "prompt_validation_demo.ipynb": LLM_CLASSIFICATION_PROJECT_ID,
    "foundation_models_summarization_demo.ipynb": LLM_SUMMARIZATION_PROJECT_ID,
    "llm_summarization_demo.ipynb": LLM_SUMMARIZATION_PROJECT_ID,
    "hugging_face_integration_demo.ipynb": NLP_CLASSIFICATION_PROJECT_ID,
    "hugging_face_summarization_demo.ipynb": NLP_SUMMARIZATION_PROJECT_ID,
}

NOTEBOOK_DIRECTORIES = [
    "notebooks/code_samples/",
    "notebooks/how_to/",
    # "notebooks/tutorials/",
]

IGNORE_NOTEBOOKS = [
    "external_test_providers.ipynb",
]


QUARTO_OUTPUT_DIR = "docs/_notebooks"
QUARTO_CMD_FMT = (
    "VM_API_HOST={api_host} "
    "VM_API_KEY={api_key} "
    "VM_API_SECRET={api_secret} "
    "VM_API_PROJECT={api_project} "
    "poetry run quarto render {notebook_file} "
    "--execute --o {output_file} --to html"
)


# This needs to be inserted at the beginning of the <header> for each rendered notebook
# to allow the HTML to render with default Quarto styles
QUARTO_HTML_HEADER_PATCH = """
<script src="libs/clipboard/clipboard.min.js"></script>
<script src="libs/quarto-html/quarto.js"></script>
<script src="libs/quarto-html/popper.min.js"></script>
<script src="libs/quarto-html/tippy.umd.min.js"></script>
<script src="libs/quarto-html/anchor.min.js"></script>
<link
  href="libs/quarto-html/tippy.css"
  rel="stylesheet"
/>
<link
  href="libs/quarto-html/quarto-syntax-highlighting.css"
  rel="stylesheet"
  id="quarto-text-highlighting-styles"
/>
<script src="libs/bootstrap/bootstrap.min.js"></script>
<link
  href="libs/bootstrap/bootstrap-icons.css"
  rel="stylesheet"
/>
<link
  href="libs/bootstrap/bootstrap.min.css"
  rel="stylesheet"
  id="quarto-bootstrap"
  data-mode="light"
/>
"""


@click.command()
def main():
    """
    Run notebooks from the public notebook directories
    """
    for notebook_directory in NOTEBOOK_DIRECTORIES:
        for root, _, files in os.walk(notebook_directory):
            for file in files:
                if (
                    file.endswith(".ipynb")
                    and "checkpoint" not in file
                    and file not in IGNORE_NOTEBOOKS
                ):
                    render_notebook(root, file)


def render_notebook(notebook_directory, file):
    # Remove the "notebooks/" prefix from the directory
    output_notebook_directory = notebook_directory.replace("notebooks/", "")
    notebook_path = os.path.join(os.getcwd(), notebook_directory, file)

    # if file == "external_test_providers.ipynb":
    #     print(file)
    #     print(notebook_path)
    #     print(notebook_directory)
    # else:
    #     return

    # Patch the notebook kernelspec to use the python3 kernel using nbformat
    # this is necessary because quarto doesn't support specifying the kernel
    # when rendering the notebook
    with open(notebook_path, "r") as f:
        notebook = nbformat.read(f, as_version=4)

        notebook["metadata"]["kernelspec"] = {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        }

    with open(notebook_path, "w") as f:
        nbformat.write(notebook, f)

    api_host = os.getenv(
        "NOTEBOOK_RUNNER_API_HOST", "https://api.dev.vm.validmind.ai/api/v1/tracking"
    )
    api_key = os.getenv("NOTEBOOK_RUNNER_API_KEY")
    api_secret = os.getenv("NOTEBOOK_RUNNER_API_SECRET")
    api_project = NOTEBOOK_PROJECT_ID_MAP.get(file, DEFAULT_PROJECT_ID)

    mkdir_cmd = f"mkdir -p {os.path.join(os.getcwd(), QUARTO_OUTPUT_DIR, output_notebook_directory)}"
    os.system(mkdir_cmd)

    output_file = os.path.join(
        os.getcwd(),
        QUARTO_OUTPUT_DIR,
        output_notebook_directory,
        file.replace(".ipynb", ".html"),
    )

    quarto_cmd = QUARTO_CMD_FMT.format(
        api_host=api_host,
        api_key=api_key,
        api_secret=api_secret,
        api_project=api_project,
        notebook_file=notebook_path,
        output_file=output_file,
    )

    print(quarto_cmd)

    depth = output_notebook_directory.count("/")
    prefix = "../" * depth

    try:
        click.echo(f"\n -------- Rendering {notebook_path} ---------- \n")
        os.system(quarto_cmd)
        click.echo(f" -------- Finished rendering {notebook_path} ---------- \n")
    except Exception as e:
        click.echo(f"Error rendering {notebook_path}: {e}")
        raise e

    print(f"Patching {output_file}")
    with open(output_file, "r") as f:
        content = f.read()
        content = content.replace("<head>", f"<head>{QUARTO_HTML_HEADER_PATCH}")
        content = content.replace('src="libs/', f'src="{prefix}libs/')
        content = content.replace('href="libs/', f'href="{prefix}libs/')

    with open(output_file, "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()
