# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
MetricResult wrapper
"""


from dataclasses import dataclass
from typing import Optional, Union

import pandas as pd

from ...errors import InvalidValueFormatterError
from ...utils import format_key_values, format_records
from .result_summary import ResultSummary


@dataclass
class MetricResult:
    """
    MetricResult class definition. A MetricResult is returned by any internal method
    that extracts metrics from a dataset or model, and returns 1) Metric and Figure
    objects that can be sent to the API and 2) and plots and metadata for display purposes
    """

    key: dict
    ref_id: str
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
            raise InvalidValueFormatterError(
                f"Invalid value_formatter: {self.value_formatter}. "
                "Must be one of 'records' or 'key_values'"
            )
        else:
            # TODO: we need to handle formatting arbitrary shapes of data
            value = self.value

        if isinstance(value, pd.DataFrame):
            raise InvalidValueFormatterError(
                "A DataFrame value was provided but no value_formatter was specified."
            )

        return {
            "key": self.key,
            "ref_id": self.ref_id,
            "value": value,
            "summary": self.summary.serialize() if self.summary else None,
        }
