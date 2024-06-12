# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

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
from .api_client import log_figure as _log_figure_async
from .api_client import log_metrics as _log_metrics_async
from .api_client import log_test_results, reload
from .client import (  # noqa: E402
    get_test_suite,
    init_dataset,
    init_model,
    init_r_model,
    preview_template,
    run_documentation_tests,
    run_test_suite,
)
from .tests.decorator import metric, tags, tasks, test
from .utils import run_async  # noqa: E402


def log_metrics(metrics, inputs=None):
    """Logs metrics to ValidMind API.

    Args:
        metrics (list): A list of Metric objects
        inputs (list): A list of input names to associate with the metrics

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    run_async(_log_metrics_async, metrics, inputs)


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
    "metric",
    "preview_template",
    "reload",
    "run_documentation_tests",
    "run_test_suite",
    "tags",
    "tasks",
    "test",
    "tests",
    "test_suites",
    "vm_models",
    "unit_metrics",
    # Framework Logging API
    "log_figure",
    "log_metrics",
    "log_test_results",
]
