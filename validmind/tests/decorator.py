# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""Decorators for creating and registering metrics with the ValidMind framework."""

import inspect
from uuid import uuid4

import pandas as pd

from validmind.logging import get_logger
from validmind.utils import clean_docstring
from validmind.vm_models import (
    Metric,
    MetricResult,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)
from validmind.vm_models.figure import (
    Figure,
    is_matplotlib_figure,
    is_plotly_figure,
    is_png_image,
)
from validmind.vm_models.test.result_wrapper import MetricResultWrapper

from . import _register_custom_test

logger = get_logger(__name__)


def _inspect_signature(test_func: callable):
    input_keys = ["dataset", "datasets", "model", "models"]

    inputs = {}
    params = {}

    for name, arg in inspect.signature(test_func).parameters.items():
        if name in input_keys:
            target_dict = inputs
        else:
            target_dict = params

        target_dict[name] = {
            "type": arg.annotation,
            "default": (
                arg.default if arg.default is not inspect.Parameter.empty else None
            ),
        }

    return inputs, params


def _build_result(results, test_id, description, output_template):
    ref_id = str(uuid4())
    figure_metadata = {
        "_type": "metric",
        "_name": test_id,
        "_ref_id": ref_id,
    }

    tables = []
    figures = []

    def process_item(item):
        if is_matplotlib_figure(item) or is_plotly_figure(item) or is_png_image(item):
            figures.append(
                Figure(
                    key=f"{test_id}:{len(figures) + 1}",
                    figure=item,
                    metadata=figure_metadata,
                )
            )
        elif isinstance(item, list):
            tables.append(ResultTable(data=item))
        elif isinstance(item, pd.DataFrame):
            tables.append(ResultTable(data=item))
        elif isinstance(item, dict):
            for table_name, table in item.items():
                tables.append(
                    ResultTable(
                        data=table,
                        metadata=ResultTableMetadata(title=table_name),
                    )
                )
        else:
            raise ValueError(f"Invalid return type: {type(item)}")

    # if the results are a tuple, process each item as a separate result
    if isinstance(results, tuple):
        for item in results:
            process_item(item)
    else:
        process_item(results)

    return MetricResultWrapper(
        result_id=test_id,
        metric=MetricResult(
            key=test_id,
            ref_id=ref_id,
            value="Empty",
            summary=ResultSummary(results=tables),
        ),
        figures=figures,
        result_metadata=[
            {
                "content_id": f"metric_description:{test_id}",
                "text": clean_docstring(description),
            }
        ],
        inputs=[],
        output_template=output_template,
    )


def get_run_method(func, inputs, params):
    def run(self: Metric):
        input_kwargs = {k: getattr(self.inputs, k) for k in inputs.keys()}
        param_kwargs = {k: getattr(self.params, k) for k in params.keys()}

        raw_results = func(**input_kwargs, **param_kwargs)

        self.result = _build_result(
            results=raw_results,
            test_id=self.test_id,
            description=self.__doc__,
            output_template=self.output_template,
        )

        return self.result

    return run


def metric(func_or_id):
    """Decorator for creating and registering metrics with the ValidMind framework.

    Creates a metric object and registers it with ValidMind under the provided ID. If
    no ID is provided, the function name will be used as to build one. So if the
    function name is `my_metric`, the metric will be registered under the ID
    `validmind.custom_metrics.my_metric`.

    This decorator works by creating a new `Metric` class will be created whose `run`
    method calls the decorated function. This function should take as arguments the
    inputs it requires (`dataset`, `datasets`, `model`, `models`) followed by any
    parameters. It can return any number of the following types:

    - Table: Either a list of dictionaries or a pandas DataFrame
    - Plot: Either a matplotlib figure or a plotly figure

    The function may also include a docstring. This docstring will be used and logged
    as the metric's description.

    Args:
        func: The function to decorate
        test_id: The identifier for the metric. If not provided, the function name is used.

    Returns:
        The decorated function.
    """

    def decorator(func):
        test_id = func_or_id or f"validmind.custom_metrics.{func.__name__}"

        inputs, params = _inspect_signature(func)
        description = inspect.getdoc(func)

        metric_class = type(
            func.__name__,
            (Metric,),
            {
                "run": get_run_method(func, inputs, params),
                "required_inputs": list(inputs.keys()),
                "default_parameters": params,
                "__doc__": description,
            },
        )
        _register_custom_test(test_id, metric_class)

        return func

    if callable(func_or_id):
        return decorator(func_or_id)

    return decorator
