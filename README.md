# ValidMind Developer Framework

![](images/ValidMind-logo-color.svg)

ValidMind's Developer Framework is a library of developer tools and methods designed to run validation tests and automate the documentation of your models. The Developer Framework provides a rich suite of documentation tools and test plans, from documenting descriptions of your dataset to testing your models for weak spots and overfit areas.

The Developer Framework includes the Python client library, which is designed to be model agnostic. If your model is built in Python, ValidMind's Python library will provide all the standard functionality without requiring your developers to rewrite any functions.

## Contributing to the ValidMind Developer Framework

We believe in the power of collaboration and welcome contributions to the ValidMind Developer Framework. If you've noticed a bug, have a feature request, or want to contribute a test, please create a pull request or submit an issue and refer to the [contributing guide](README.md#how-to-contribute) below.

- Interested in connecting with fellow AI model risk practitioners? Join our [Community Slack](site/guide/join-community.qmd)!

- For more information about ValidMind's open source tests and Jupyter notebooks, read the [Developer Framework docs](https://docs.validmind.ai/guide/developer-framework.html).

## Getting started

### Install from PyPI

```bash
pip install validmind
```

#### Install with Hugging Face `transformers` support

```bash
pip install validmind[transformers]
```

#### Install with PyTorch support

```bash
pip install validmind[pytorch]
```

#### Install with R support (requires R to be installed)

```bash
pip install validmind[r-support]
```

## How to contribute

### Install dependencies

- Ensure you have `poetry` installed: <https://python-poetry.org/>

- After cloning this repo, run:

    ```bash
    poetry shell
    poetry install
    ```

- To run Jupyter notebooks using the source code from the repo, you can use `poetry` to register
a new kernel with Jupyter:

```bash
poetry run python -m ipykernel install --user --name dev-framework --display-name "Developer Framework"
```

### Installing LLM validation dependencies

You can install the `transformers` and `torch` dependencies using the `llm` extra. This will install the Hugging Face transformers and PyTorch libraries by running:

```bash
poetry install --extras llm
```
### Installing R dependencies

If you want to use the R support that is provided by the ValidMind Developer Framework, you must have R installed on your machine. You can download R from <https://cran.r-project.org/>. On a Mac, you can install R using Homebrew:

```bash
brew install r
```

Once you have R installed, install the `r-support` extra to install the necessary dependencies for R by running:

```bash
poetry install --extras r-support
```

### Versioning

Make sure you bump the package version before merging a PR with the following command:

```bash
make version tag=patch
```

The value of `tag` corresponds to one of the options provided by Poetry: <https://python-poetry.org/docs/cli/#version>

## Generating API Reference Docs

The [API reference documentation](https://docs.validmind.ai/validmind/validmind.html) you see in our docs site is generated in HTML format with `pdoc` with the following
command:

```bash
# Generate HTML
make docs
```

The resulting docs are written to `docs/pdoc/_build`.

## Adding a Copyright Header

When adding new files to the project, you can add the ValidMind copyright header to any files that
are missing it by running:

```bash
make copyright
```

## Known Issues

### ValidMind wheel errors

If you run into an error related to the ValidMind wheel, try:

```bash
poetry add wheel
poetry update wheel
poetry install
```

If there are lightgbm errors partway through, run `remove lightgbm`, followed by `poetry update wheel` and `poetry install`.
