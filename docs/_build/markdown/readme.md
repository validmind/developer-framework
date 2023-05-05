# ValidMind Python Client

## Installation

### Install from PyPI

```bash
pip install validmind
```

#### Install with R support (requires R to be installed)

```bash
pip install validmind[r-support]
```

## Contributing to ValidMind Developer Framework

### Install dependencies


* Ensure you have `poetry` installed: https://python-poetry.org/


* After cloning this repo run:

```bash
poetry shell
poetry install
```

### Installing R dependencies

If you want to use the R support that is provided by the ValidMind Developer Framework, you must have R installed on your machine. You can download R from https://cran.r-project.org/. If you are on a Mac, you can install R using Homebrew:

```bash
brew install r
```

Once you have R installed, you can install the `r-support` extra to install the necessary dependencies for R by running:

```bash
poetry install --extras r-support
```

### Versioning

Make sure you bump the package version before merging a PR with the following command:

```bash
make version tag=patch
```

The value of `tag` corresponds to one of the options provided by Poetry: https://python-poetry.org/docs/cli/#version

## Integrating the ValidMind Developer Framework to your development environment

If you want to integate the `validmind` package to your development environment, you must build the package
wheel first, since we have not pushed the package to a public PyPI repository yet. Steps:


* Run `make build` to build a new Python package for the developer framework


* This will create a new wheel file in the `dist` folder


* Run `pip install <path-to-wheel>` to install the newly built package in your environment

## Generating Docs

API documentation can be generated in Markdown or HTML format. Our documentation pipeline
uses Markdown documentation before generating the final HTML assets for the documentation site.

For local testing, HTML docs can be generated with Sphinx. Note that the output template
is different since the documentation pipeline uses the source Markdown files for the final
HTML output.

Markdown and HTML docs can be generated with the following commands:

```bash
# Navigate to the docs folder
cd docs/

# Generate HTML and Markdown docs
make docs

# Generate Markdown docs only
make docs-markdown

# Generate HTML docs only
make docs-html
```

The resulting `markdown` and `html` under `docs/_build` folders will contain the generated documentation.

## Known Issues

### ValidMind wheel errors

If you run into an error related to the ValidMind wheel, try:

```bash
poetry add wheel
poetry update wheel
poetry install
```

If there are lightgbm errors partway through, run `remove lightgbm`, followed by `poetry update wheel` and `poetry install`.
