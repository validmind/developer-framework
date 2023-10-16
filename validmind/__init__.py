# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
ValidMind’s Python Developer Framework is a library of developer tools and methods designed to automate
the documentation and validation of your models.

The Developer Framework is designed to be model agnostic. If your model is built in Python, ValidMind's
Python library will provide all the standard functionality without requiring your developers to rewrite any functions.

The Developer Framework provides a rich suite of documentation tools and test suites, from documenting
descriptions of your dataset to testing your models for weak spots and overfit areas. The Developer Framework
helps you automate the generation of model documentation by feeding the ValidMind platform with documentation
artifacts and test results to the ValidMind platform.

To install the client library:

```bash
pip install validmind
```

To initialize the client library, paste the code snippet with the client integration details directly into your
development source code, replacing this example with your own:

```python
import validmind as vm

vm.init(
  api_host = "https://api.dev.vm.validmind.ai/api/v1/tracking/tracking",
  api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  api_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  project = "<project-identifier>"
)
```

After you have pasted the code snippet into your development source code and executed the code, the Python client
library will register with ValidMind. You can now use the Developer Framework to document and test your models,
and to upload to the ValidMind Platform.
"""
import warnings

# Ignore Numba warnings. We are not requiring this package directly
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning

warnings.simplefilter("ignore", category=NumbaDeprecationWarning)
warnings.simplefilter("ignore", category=NumbaPendingDeprecationWarning)

from .__version__ import __version__  # noqa: E402
from .api_client import init
from .api_client import log_dataset as _log_dataset_async  # noqa: E402
from .api_client import log_figure as _log_figure_async
from .api_client import log_metrics as _log_metrics_async
from .api_client import log_test_results
from .client import run_test_plan  # DEPRECATED
from .client import (  # noqa: E402
    get_test_suite,
    init_dataset,
    init_model,
    init_r_model,
    preview_template,
    run_documentation_tests,
    run_template,
    run_test_suite,
)
from .utils import run_async  # noqa: E402


def log_dataset(dataset):
    """Logs metadata and statistics about a dataset to ValidMind API.

    Args:
        vm_dataset (validmind.VMDataset): A VM dataset object

    Returns:
        validmind.VMDataset: The VMDataset object
    """
    run_async(_log_dataset_async, dataset)


def log_metrics(metrics):
    """Logs metrics to ValidMind API.

    Args:
        metrics (list): A list of Metric objects

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    run_async(_log_metrics_async, metrics)


def log_figure(figure):
    """Logs a figure

    Args:
        figure (Figure): The Figure object wrapper

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    run_async(_log_figure_async, figure)


__all__ = [  # noqa
    "__version__",
    # Framework High Level API
    "datasets",
    "errors",
    "get_test_suite",
    "init",
    "init_dataset",
    "init_model",
    "init_r_model",
    "preview_template",
    "run_documentation_tests",
    "run_template",
    "run_test_plan",  # DEPRECATED
    "run_test_suite",
    "tests",
    "test_suites",
    "vm_models",
    # Framework Logging API
    "log_dataset",
    "log_figure",
    "log_metrics",
    "log_test_results",
]
