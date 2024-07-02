# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
ThresholdTestResult models
"""
from dataclasses import dataclass
from typing import List, Optional

from .result_summary import ResultSummary


@dataclass
class ThresholdTestResult:
    """
    ThresholdTestResult model
    """

    values: dict
    test_name: Optional[str] = None  # Optionally allow a name for an individual test
    column: Optional[
        str
    ] = None  # Optionally track the results for an individual column
    passed: Optional[bool] = None  # Optionally per-result pass/fail

    def serialize(self):
        """
        Serializes the ThresholdTestResult to a dictionary so it can be sent to the API
        """
        test_result = {
            "values": self.values,
        }

        if self.test_name is not None:
            test_result["test_name"] = self.test_name

        if self.column is not None:
            test_result["column"] = self.column

        if self.passed is not None:
            test_result["passed"] = self.passed

        return test_result


@dataclass
class ThresholdTestResults:
    """
    ThresholdTestResults model
    """

    test_name: str
    ref_id: str
    params: dict
    passed: bool
    results: List[ThresholdTestResult]
    summary: Optional[ResultSummary]

    def serialize(self):
        """
        Serializes the ThresholdTestResults to a dictionary so it can be sent to the API
        """
        test_results = {
            "test_name": self.test_name,
            "ref_id": self.ref_id,
            "params": self.params,
            "passed": self.passed,
            "results": [result.serialize() for result in self.results],
        }

        if self.summary is not None:
            test_results["summary"] = self.summary.serialize()

        return test_results
