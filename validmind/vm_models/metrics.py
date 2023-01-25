"""
Class for storing ValidMind metric objects and associated
data for display and reporting purposes
"""
from dataclasses import dataclass
from typing import List, Optional, Union

from pandas import DataFrame

from ..utils import format_records, format_key_values


@dataclass()
class Metric:
    """
    Metric objects track the schema supported by the ValidMind API
    """

    type: str
    scope: str
    key: str
    value: Union[dict, list, DataFrame] = None
    value_formatter: Optional[str] = None

    def serialize(self):
        """
        Serializes the Metric to a dictionary so it can be sent to the API
        """
        if self.value_formatter == "records":
            value = format_records(self.value)
        elif self.value_formatter == "key_values":
            value = format_key_values(self.value)
        elif self.value_formatter is not None:
            raise ValueError(
                f"Invalid value_formatter: {self.value_formatter}. "
                "Must be one of 'records' or 'key_values'"
            )
        else:
            value = self.value

        if isinstance(value, DataFrame):
            raise ValueError(
                "A DataFrame value was provided but no value_formatter was specified."
            )

        return {
            "type": self.type,
            "scope": self.scope,
            "key": self.key,
            "value": value,
        }


@dataclass()
class Figure:
    """
    Figure objects track the schema supported by the ValidMind API
    """

    key: str
    metadata: dict
    figure: object

    def serialize(self):
        """
        Serializes the Figure to a dictionary so it can be sent to the API
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
    that extracts metrics from a dataset or model, and returns 1) Metric and Figure
    objects that can be sent to the API and 2) and plots and metadata for display purposes
    """

    api_metric: Metric
    api_figures: Optional[List[Figure]] = None
    plots: Optional[List[object]] = None
    metadata: Optional[dict] = None
