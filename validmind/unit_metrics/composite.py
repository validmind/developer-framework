# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from typing import Protocol
from uuid import uuid4

from ..utils import run_async
from ..vm_models.test.metric import Metric
from ..vm_models.test.metric_result import MetricResult
from ..vm_models.test.result_summary import ResultSummary, ResultTable
from ..vm_models.test.result_wrapper import MetricResultWrapper
from . import run_metric


class MetricProtocol(Protocol):
    unit_metrics: list[str]

    def output(self, results):
        pass


@dataclass
class CompositeMetric(Metric):

    unit_metrics: list[str] = None

    def __post_init__(self):
        if self._unit_metrics:
            self.unit_metrics = self._unit_metrics
        elif self.unit_metrics is None:
            raise ValueError("unit_metrics must be provided")

        if hasattr(self, "_output_template"):
            self.output_template = self._output_template

    def run(self):
        self.result = run_metrics(
            key=self.test_id,
            metric_ids=self.unit_metrics,
            inputs=self._get_input_dict(),
            params=self.params,
            output_template=self.output_template,
            show=False,
        )

        return self.result

    def summary(self, result: dict):
        return ResultSummary(results=[ResultTable(data=[result])])


def load_composite_metric(
    metric_key: str = None, metric_name: str = None, unit_metrics: list[str] = None
) -> CompositeMetric:
    # this function can either create a composite metric from a list of unit metrics or
    # load a stored composite metric based on the test id

    # TODO: figure out this circular import thing:
    from ..api_client import get_metadata

    if metric_key:
        # get the unit metric ids from the metadata
        unit_metrics = run_async(
            get_metadata, f"composite_metric_def:{metric_key}:unit_metrics"
        )

        output_template = run_async(
            get_metadata, f"composite_metric_def:{metric_key}:output_template"
        )

        class_def = type(
            metric_key.split(".")[-1],
            (CompositeMetric,),
            {
                "__doc__": "Composite Metric built from multiple unit metrics",
                "_unit_metrics": unit_metrics["json"],
                "_output_template": output_template["json"]["output_template"],
            },
        )

    else:
        class_def = type(
            metric_name,
            (CompositeMetric,),
            {
                "__doc__": "Composite Metric built from multiple unit metrics",
                "_unit_metrics": unit_metrics,
            },
        )

    return class_def


def run_metrics(
    name: str = None,
    metric_ids: list[str] = None,
    output_template=None,
    inputs=None,
    params=None,
    key: str = None,
    show=True,
) -> MetricResultWrapper:
    if not metric_ids:
        raise ValueError("metric_ids must be provided")

    if not name and not key:
        raise ValueError("name or key must be provided")

    results = {}

    for metric_id in metric_ids:
        result = run_metric(
            metric_id=metric_id,
            inputs=inputs,
            params=params,
        )
        results[list(result.summary.keys())[0]] = result.value

    metric_key = f"validmind.composite_metric.{name}" if not key else key

    result_wrapper = MetricResultWrapper(
        result_id=metric_key,
        result_metadata=[
            {
                "content_id": f"composite_metric_def:{metric_key}:unit_metrics",
                "json": metric_ids,
            },
            {
                "content_id": f"composite_metric_def:{metric_key}:output_template",
                "json": {"output_template": output_template},
            },
        ],
        inputs=list(inputs.keys()),
        output_template=output_template,
        metric=MetricResult(
            key=metric_key,
            ref_id=str(uuid4()),
            value=results,
            summary=ResultSummary(results=[ResultTable(data=[results])]),
        ),
    )

    if show:
        result_wrapper.show()

    return result_wrapper


def metric(cls: MetricProtocol):
    """decorator to compose metrics from classes"""

    def run(self, inputs=None, params=None):
        return run_metrics(self.unit_metrics, inputs=inputs, params=params)

    cls.run = run

    return cls
