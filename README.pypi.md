# ValidMind Developer Framework

ValidMind’s Python Developer Framework is a library of developer tools and methods designed to automate
the documentation and validation of your models.

The Developer Framework is designed to be model agnostic. If your model is built in Python, ValidMind's
Python library will provide all the standard functionality without requiring your developers to rewrite any functions.

The Developer Framework provides a rich suite of documentation tools and test suites, from documenting
descriptions of your dataset to testing your models for weak spots and overfit areas. The Developer
Framework helps you automate the generation of model documentation by feeding the ValidMind platform with
documentation artifacts and test results to the ValidMind platform.

## Installation

To install the ValidMind Developer Framework and all optional dependencies, run:

```bash
pip install validmind[all]
```

To install the Developer Framework without optional dependencies (core functionality only), run:

```bash
pip install validmind
```

### Extra dependencies

The Developer Framework has optional dependencies that can be installed separately to support additional model types and tests.

- **LLM Support**: To be able to run tests for Large Language Models (LLMs), install the `llm` extra:

    ```bash
    pip install validmind[llm]
    ```

- **PyTorch Models**: To use pytorch models with the Developer Framework, install the `torch` extra:

    ```bash
    pip install validmind[torch]
    ```

- **Hugging Face Transformers**: To use Hugging Face Transformers models with the Developer Framework, install the `transformers` extra:

    ```bash
    pip install validmind[transformers]
    ```

- **R Models**: To use R models with the Developer Framework, install the `r` extra:

    ```bash
    pip install validmind[r-support]
    ```
