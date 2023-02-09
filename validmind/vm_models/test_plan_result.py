"""
TestPlanResult
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TestPlanResult:
    """
    Result wrapper tests that run as part of a test plan
    """

    metric: Optional[object] = None
    test_results: Optional[object] = None
    figures: Optional[object] = None
    plots: Optional[List[object]] = None
