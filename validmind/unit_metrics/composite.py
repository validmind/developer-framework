# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from typing import Protocol

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


def run_metrics(
    metric_ids: list[str], inputs=None, params=None, output_template=None
) -> MetricResultWrapper:
    results = {}

    for metric_id in metric_ids:
        result = run_metric(
            metric_id=metric_id,
            inputs=inputs,
            params=params,
        )
        results[list(result.summary.keys())[0]] = result.value

    result_wrapper = MetricResultWrapper(
        result_id="composite_metric",
        result_metadata=[
            {
                "content_id": "unit_metrics:composite_metric",
                "json": metric_ids,
            },
            {
                "content_id": "output_template:composite_metric",
                "json": {"output_template": output_template},
            },
        ],
        inputs=list(inputs.keys()),
        output_template=output_template,
        metric=MetricResult(
            key="composite_metric",
            ref_id="composite_metric",
            value=results,
            summary=ResultSummary(results=[ResultTable(data=[results])]),
        ),
    )

    result_wrapper.show()

    return result_wrapper


def metric(cls: MetricProtocol):
    """decorator to compose metrics from classes"""

    def run(self, inputs=None, params=None):
        return run_metrics(self.unit_metrics, inputs=inputs, params=params)

    cls.run = run

    return cls


@dataclass
class CompositeMetric(Metric):

    unit_metrics: list[str] = None

    def __post_init__(self):
        if self.unit_metrics is None:
            raise ValueError("unit_metrics must be provided")

    def run(self):
        return self.cache_results(
            run_metrics(
                self.unit_metrics,
                inputs=self.inputs,
                params=self.params,
            )
        )

    def summary(self, result: dict):
        return ResultSummary(results=[ResultTable(data=[result])])
