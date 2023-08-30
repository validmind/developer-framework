# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Models entrypoint
"""

from .dataset import VMDataset
from .figure import Figure
from .metric import Metric
from .metric_result import MetricResult
from .model import R_MODEL_TYPES, ModelAttributes, VMModel

# Import plot_utils so we can initialize the default matplotlib params
from .plot_utils import *  # noqa
from .result_summary import ResultSummary, ResultTable, ResultTableMetadata
from .test import Test
from .test_context import TestContext, TestContextUtils
from .test_plan import TestPlan
from .test_plan_result import (
    TestPlanDatasetResult,
    TestPlanMetricResult,
    TestPlanTestResult,
)
from .test_result import TestResult, TestResults
from .test_suite import TestSuite
from .threshold_test import ThresholdTest

__all__ = [
    "VMDataset",
    "Figure",
    "Metric",
    "MetricResult",
    "VMModel",
    "ModelAttributes",
    "R_MODEL_TYPES",
    "ResultSummary",
    "ResultTable",
    "ResultTableMetadata",
    "Test",
    "TestContext",
    "TestContextUtils",
    "TestPlan",
    "TestPlanDatasetResult",
    "TestPlanMetricResult",
    "TestPlanTestResult",
    "TestResult",
    "TestResults",
    "TestSuite",
    "ThresholdTest",
]
