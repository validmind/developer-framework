"""
Main entrypoint to the ValidMind Python Library
"""
import warnings

# Ignore Numba warnings. We are not requiring this package directly
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning

warnings.simplefilter("ignore", category=NumbaDeprecationWarning)
warnings.simplefilter("ignore", category=NumbaPendingDeprecationWarning)

import validmind.vm_models as vm_models

from .api_client import (  # noqa: E402
    init,
    log_dataset,
    log_metrics,
    log_model,
    log_test_results,
    log_figure,
)

from .client import (  # noqa: E402
    init_dataset,
    init_model,
    init_r_model,
    run_test_plan,
    run_test_suite,
)

# TODO: need to fix this import * situation
from .datasets import *  # noqa
from .data_validation import *  # noqa
from .model_validation import *  # noqa
from .test_plans import *  # noqa
from .test_suites import *  # noqa

__all__ = [  # noqa
    # Framework High Level API
    "datasets",
    "data_validation",
    "init",
    "init_dataset",
    "init_model",
    "init_r_model",
    "model_validation",
    "run_test_plan",
    "run_test_suite",
    "test_plans",
    "test_suites",
    "vm_models",
    # Framework Logging API
    "log_dataset",
    "log_figure",
    "log_metrics",
    "log_model",
    "log_test_results",
]
