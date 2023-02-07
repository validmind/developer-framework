"""
MetricResult wrapper
"""


from dataclasses import dataclass
from typing import List, Optional

from .figure import Figure
from .metric import Metric


@dataclass
class MetricResult:
    """
    MetricResult class definition. A MetricResult is returned by any internal method
    that extracts metrics from a dataset or model, and returns 1) Metric and Figure
    objects that can be sent to the API and 2) and plots and metadata for display purposes
    """

    api_metric: Metric
    api_figures: Optional[List[Figure]] = None
    plots: Optional[List[object]] = None
    metadata: Optional[dict] = None
