# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Class for storing ValidMind metric objects and associated
data for display and reporting purposes
"""
from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, Union

import pandas as pd

from validmind.vm_models import MetricResult

from .test import Test


@dataclass
class UnitMetric(Test):
    """
    Metric objects track the schema supported by the ValidMind API
    """

    # Instance Variables
    result: MetricResult = None  # populated by cache_results() method

    def run(self):
        """
        Run the metric
        """
        raise NotImplementedError("Metric must implement run()")

    @property
    def metric_id(self) -> str:
        """
        Return the metric id by using the automatically generated test_id
        """
        return self.test_id

    @property
    def name(self) -> str:
        # get metric name from metric_id, for example if metric_id i:
        # 'validmind.unit_metrics.sklearn.classification.F1' then the metric name is 'f1'
        return self.metric_id.split(".")[-1].lower()

    @abstractmethod
    def summary(
        self, metric_value: Optional[Union[str, float]] = None
    ) -> Dict[str, float]:
        """
        Raise an error if metric_value is None.
        Else, return an object like this: {<metric-name>: <value>}
        Metric name can be calculated from a property, similar to how you defined test_id above.
        The metric name should ideally be a single lowercase word such as accuracy.
        """
        if metric_value is None:
            raise ValueError("metric_value cannot be None")

        return {self.name: metric_value}

    def cache_results(
        self,
        metric_value: Optional[Union[dict, list, pd.DataFrame]] = None,
    ):
        """
        Cache the results of the metric calculation and do any post-processing if needed

        Args:
            metric_value (Union[dict, list, pd.DataFrame]): The value of the metric

        Returns:
            TestSuiteResult: The test suite result object
        """

        result_summary = self.summary(metric_value)

        metric_result = MetricResult(
            key=self.test_id,
            ref_id=self._ref_id,
            value=metric_value,
            summary=result_summary,
        )

        self.result = metric_result

        return self.result
