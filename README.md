# ValidMind Python Client

## Contributing to ValidMind Developer Framework

### Install dependencies

- Ensure you have `poetry` installed: https://python-poetry.org/

- After cloning this repo run:

```bash
poetry shell
poetry install
```

### Versioning

Make sure you bump the package version before merging a PR with the following command:

```bash
make version tag=prerelease
```

The value of `tag` corresponds to one of the options provided by Poetry: https://python-poetry.org/docs/cli/#version

## Integrating the ValidMind Developer Framework to your development environment

If you want to integate the `validmind` package to your development environment, you must build the package
wheel first, since we have not pushed the package to a public PyPI repository yet. Steps:

- Run `make build` to build a new Python package for the developer framework
- This will create a new wheel file in the `dist` folder
- Run `pip install <path-to-wheel>` to install the newly built package in your environment

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

# Generate Markdown docs
make markdown

# Generate HTML docs
make html
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