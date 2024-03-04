# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Class for storing ValidMind metric objects and associated
data for display and reporting purposes
"""
from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Optional, Union, Dict

import pandas as pd

from validmind.vm_models import MetricResult

from ...utils import clean_docstring
from .result_wrapper import MetricResultWrapper
from .test import Test


@dataclass
class UnitMetric(Test):
    """
    Metric objects track the schema supported by the ValidMind API
    """

    # Class Variables
    test_type: ClassVar[str] = "UnitMetric"
    name: ClassVar[str] = ""  # name of the metric

    type: ClassVar[str] = ""  # type of metric: "training", "evaluation", etc.
    scope: ClassVar[str] = ""  # scope of metric: "training_dataset"

    # Instance Variables
    result: MetricResult = None  # populated by cache_results() method

    def run(self):
        """
        Run the metric
        """
        raise NotImplementedError("Metric must implement run()")

    def _metric_name(self) -> str:
        # get metric name from metric_id, for example if metric_id i:
        # 'validmind.unit_metrics.sklearn.classification.F1' then the metric name is 'f1'
        print(f"metric_id: {self.metric_id}")
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

        return {self._metric_name(): metric_value}

    def get_prediction_column(self, vm_dataset, model_id):
        """
        Extracts the prediction column from a dataset's _extra_columns attribute, if available, based on the provided model_id.

        Args:
        - vm_dataset: An instance of a dataset class with an _extra_columns attribute.
        - model_id: The ID of the model for which predictions are being sought.

        Returns:
        - The prediction column name. If no prediction columns are found for the given model ID or if the prediction columns dictionary is empty,
        returns None.
        """
        # Initialize prediction_column to None
        prediction_column = None

        # Check if prediction_columns dictionary is not empty and contains the model_id
        if (
            vm_dataset._extra_columns["prediction_columns"]
            and model_id in vm_dataset._extra_columns["prediction_columns"]
        ):
            prediction_column = vm_dataset._extra_columns["prediction_columns"][
                model_id
            ]

        return prediction_column

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

        test_suite_result = MetricResultWrapper(
            result_id=self.test_id,
            inputs=self.get_accessed_inputs(),
        )

        test_suite_result.metric = MetricResult(
            key=self.test_id,
            ref_id=self._ref_id,
            value=metric_value,
            summary=result_summary,
            metric_inputs=self.metric_inputs,
            required_inputs=self.required_inputs,
        )

        self.result = test_suite_result

        return self.result
