"""
MetricResult wrapper
"""


from dataclasses import dataclass
from typing import Optional, Union

import pandas as pd

from .result_summary import ResultSummary
from ..utils import format_records, format_key_values


@dataclass
class MetricResult:
    """
    MetricResult class definition. A MetricResult is returned by any internal method
    that extracts metrics from a dataset or model, and returns 1) Metric and Figure
    objects that can be sent to the API and 2) and plots and metadata for display purposes
    """

    type: str
    scope: str
    key: dict
    value: Union[dict, list, pd.DataFrame]
    summary: Optional[ResultSummary] = None
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
            # TODO: we need to handle formatting arbitrary shapes of data
            value = self.value

        if isinstance(value, pd.DataFrame):
            raise ValueError(
                "A DataFrame value was provided but no value_formatter was specified."
            )

        return {
            "type": self.type,
            "scope": self.scope,
            "key": self.key,
            "value": value,
            "summary": self.summary.serialize() if self.summary else None,
        }
