# ValidMind

![](images/ValidMind-logo-color.svg)

ValidMind helps model developers and model validators streamline communication and automate the model documentation process. 

## Contributing to the ValidMind Developer Framework

We believe in the power of collaboration and welcome contributions to the ValidMind Python Client. If you've noticed a bug, have a feature request, or want to contribute a test, please submit an issue or create a pull request and refer to the [contributing guide](README.md#how-to-contribute) below.

- Interested in connecting with fellow Model Risk Management (MRM) practioners? Join our [Community Slack](site/guide/join-community.qmd)

- For more information about ValidMind's open source tests and Jupyter notebooks, read the [Developer Framework docs](https://docs.validmind.ai/guide/developer-framework.html).

## Getting started

### Install from PyPI

```bash
pip install validmind
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

- After cloning this repo run:

```bash
poetry shell
poetry install
```

### Installing PyTorch dependencies

You can install the `pytorch` extra to install the necessary PyTorch dependencies by running:

```bash
poetry install --extras pytorch
```

### Creating a new Test

All ValidMind Tests are in the `validmind/tests/` directory. Each file should be named using Camel Case and should have a single Test class that matches the file name. For example, `MyNewTest.py` should have the Test `class MyNewTest`. This class should inherit from `validmind.vm_models.Metric` or `validmind.vm_models.ThresholdTest` depending on the type of test you are creating. 

The tests are separated into subdirectories based on the category and type of test. For example, `validmind/tests/model_validation/sklearn` contains all of the model validation tests for sklearn-compatible models. There are two subdirectories in this folder: `metrics/` and `threshold_tests/` that contain the different types of tests. Any sub category can be used here and the `__init__.py` file will automatically pick up the tests.

Please see the notebook `listing-and-loading-tests.ipynb` for more information and examples and to learn about how the directory relates to the test's ID which is used across the ValidMind platform.

To create a new test, you can use the create_new_test.py script to generate a metric or threshold test. This script will create a new test file in the appropriate directory and will also create a new test class in that file. It is registered as a custom Poetry script in the `pyproject.toml` and it can be used as follows:

```bash
generate-test --help  # see the usage instructions
generate-test  # interactively create a new test (will prompt for the test type and ID)
generate-test --test_type metric --test_id validmind.model_validation.sklearn.MyNewMetric  # create a new metric test for sklearn models
generate-test --test_type threshold_test --test_id validmind.data_validation.MyNewDataTest  # create a new threshold test for data validation
```

### Installing R dependencies

If you want to use the R support that is provided by the ValidMind Developer Framework, you must have R installed on your machine. You can download R from <https://cran.r-project.org/>. If you are on a Mac, you can install R using Homebrew:

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

The value of `tag` corresponds to one of the options provided by Poetry: <https://python-poetry.org/docs/cli/#version>

## Generating Docs

API documentation can be generated as HTML format with `pdoc` with the following
command:

```bash
# Generate HTML
make docs
```

The resulting docs will be written to `docs/pdoc/_build`.

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
