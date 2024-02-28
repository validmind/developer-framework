# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Class for storing ValidMind metric objects and associated
data for display and reporting purposes
"""
from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Optional, Union

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

    type: ClassVar[str] = ""  # type of metric: "training", "evaluation", etc.
    scope: ClassVar[str] = ""  # scope of metric: "training_dataset"
    value_formatter: ClassVar[Optional[str]] = None  # "records" or "key_values"

    # Instance Variables
    result: MetricResultWrapper = None  # populated by cache_results() method

    def run(self):
        """
        Run the metric
        """
        raise NotImplementedError("Metric must implement run()")

    @property
    def key(self):
        """
        Keep the key for compatibility reasons
        """
        return self._key if hasattr(self, "_key") else self.name

    @abstractmethod
    def summary(self, metric_value: Optional[Union[dict, list, pd.DataFrame]] = None):
        """
        Return the metric summary. Should be overridden by subclasses. Defaults to None.
        The metric summary allows renderers (e.g. Word and ValidMind UI) to display a
        short summary of the metric results.

        We return None here because the metric summary is optional.
        """
        return None

    
    def get_prediction_column_and_model_id(self, vm_dataset):
        """
        Directly extracts the model ID and prediction column from a dataset's _extra_columns attribute.
        
        Args:
        - vm_dataset: An instance of a dataset class with an _extra_columns attribute.
        
        Returns:
        - A tuple containing the model ID and the prediction column name.
        """
        # Directly access the model ID and prediction column name
        model_id = list(vm_dataset._extra_columns['prediction_columns'].keys())[0]
        prediction_column = vm_dataset._extra_columns['prediction_columns'][model_id]
        return model_id, prediction_column        
        
        
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

        # At a minimum, send the metric description
        result_metadata = [
            {
                "content_id": f"metric_description:{self.test_id}",
                "text": clean_docstring(self.description()),
            }
        ]

        result_summary = self.summary(metric_value)

        test_suite_result = MetricResultWrapper(
            result_id=self.test_id,
            result_metadata=result_metadata,
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
