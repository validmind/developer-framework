"""
TestPlanResult
"""

from dataclasses import dataclass
from typing import List, Optional

import ipywidgets as widgets
from IPython.display import display


# old way with one class
@dataclass
class TestPlanResult:
    """
    Result wrapper tests that run as part of a test plan
    """

    dataset: Optional[object] = None
    metric: Optional[object] = None
    model: Optional[object] = None
    test_results: Optional[object] = None
    figures: Optional[object] = None
    plots: Optional[List[object]] = None

@dataclass
class TestPlanDatasetResult:
    """
    Result wrapper for datasets that run as part of a test plan
    """

    dataset: Optional[object] = None


@dataclass
class TestPlanMetricResult:
    """
    Result wrapper for metrics that run as part of a test plan
    """

    figures
    metric: Optional[object] = None

