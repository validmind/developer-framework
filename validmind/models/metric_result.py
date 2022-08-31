"""
Class for storing ValidMind metric objects and associated
data for display and reporting purposes
"""
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass()
class APIMetric:
    """
    APIMetric objects track the schema supported by the ValidMind API
    """

    type: str
    scope: str
    key: str
    value: Union[dict, list] = None

    def serialize(self):
        """
        Serializes the APIMetric to a dictionary so it can be sent to the API
        """
        return {
            "type": self.type,
            "scope": self.scope,
            "key": self.key,
            "value": self.value,
        }


@dataclass()
class APIFigure:
    """
    APIFigure objects track the schema supported by the ValidMind API
    """

    key: str
    metadata: dict
    figure: object

    def serialize(self):
        """
        Serializes the APIFigure to a dictionary so it can be sent to the API
        """
        return {
            "key": self.key,
            "metadata": self.metadata,
            "figure": self.figure,
        }


@dataclass()
class MetricResult:
    """
    MetricResult class definition. A MetricResult is returned by any internal method
    that extracts metrics from a dataset or model, and returns 1) APIMetric and APIFigure
    objects that can be sent to the API and 2) and plots and metadata for display purposes
    """

    api_metric: APIMetric
    api_figures: Optional[List[APIFigure]] = None
    plots: Optional[List[object]] = None
    metadata: Optional[dict] = None
