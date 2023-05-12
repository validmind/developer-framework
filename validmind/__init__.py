"""
Main entrypoint to the ValidMind Python Library
"""
import warnings

# Ignore Numba warnings. We are not requiring this package directly
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning

warnings.simplefilter("ignore", category=NumbaDeprecationWarning)
warnings.simplefilter("ignore", category=NumbaPendingDeprecationWarning)

from .vm_models import (  # noqa: E402
    Dataset,
    DatasetTargets,
    Figure,
    Metric,
    Model,
    ModelAttributes,
    TestResult,
    TestResults,
    ThresholdTest,
)

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
from .data_validation import *  # noqa
from .test_plans import *  # noqa

__all__ = [  # noqa
    # Framework High Level API
    "data_validation",
    "init",
    "init_dataset",
    "init_model",
    "init_r_model",
    "test_plans",
    "run_test_plan",
    "run_test_suite",
    # Framework Logging API
    "log_dataset",
    "log_figure",
    "log_metrics",
    "log_model",
    "log_test_results",
    # Models
    "Dataset",
    "DatasetTargets",
    "Figure",
    "Metric",
    "Model",
    "ModelAttributes",
    "TestResult",
    "TestResults",
    "ThresholdTest",
]
