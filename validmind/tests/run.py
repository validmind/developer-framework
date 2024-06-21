# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from itertools import product
from typing import Any, Dict, List

from validmind.errors import LoadTestError
from validmind.unit_metrics import run_metric
from validmind.unit_metrics.composite import load_composite_metric
from validmind.vm_models import TestContext, TestInput
from validmind.vm_models.test.result_wrapper import MetricResultWrapper

from .__types__ import TestID
from .load import load_test


# TODO:
# 1. How to combine `value`?
# 2. Support for threshold tests
# 3. When combining figures it's important that the test produces figures annotates
#       them correctly with the input names so they can be distinguished
def run_comparison_test(  # noqa: C901
    test_id: TestID,
    input_grid: Dict[str, List[Any]],
    show=True,
):
    keys, values = zip(*input_grid.items())
    input_groups = [dict(zip(keys, v)) for v in product(*values)]

    merged_metric_result = None
    merged_results = MetricResultWrapper(metric=merged_metric_result)

    for input_group_index, inputs in enumerate(input_groups):
        result = run_test(test_id, inputs=inputs, show=False)

        if merged_metric_result is None:
            merged_metric_result = result
            merged_results.name = merged_results.name
            # Use the key and ref_id from the first result
            merged_metric_result.key = result.metric.key
            merged_metric_result.ref_id = result.metric.ref_id
            merged_results.result_id = result.result_id
        else:
            merged_results.name = merged_results.name + "." + result.name

        # TODO: how to combine inputs?
        merged_results.inputs = result.inputs

        # Combine the figures when available
        if merged_results.figures is None:
            merged_results.figures = result.figures
        else:
            merged_results.figures.extend(result.figures)

        # Some metrics have no summary (e.g. when they only produce figures)
        if result.metric.summary is None:
            continue

        # Add a new column to the results dataset that describes the inputs
        input_description = []
        for _, input in inputs.items():
            if isinstance(input, str):
                input_description.append(input)
            else:
                input_description.append(input.input_id)
        input_description = ", ".join(input_description)

        # Each element inside the table is a dict. We need to add the inputs key
        # to the beginning of each dict.
        for i, table in enumerate(result.metric.summary.results):
            for j, row in enumerate(table.data):
                new_dict = {"Inputs": input_description}
                new_dict.update(row)
                table.data[j] = new_dict

        # Only merge results for the second and subsequent results
        if input_group_index == 0:
            continue

        for i, table in enumerate(result.metric.summary.results):
            merged_metric_result.metric.summary.results[i].data.extend(table.data)

    if show:
        merged_metric_result.show()

    return merged_metric_result


def run_test(
    test_id: TestID = None,
    name: str = None,
    unit_metrics: list = None,
    params: dict = None,
    inputs=None,
    output_template=None,
    show=True,
    **kwargs,
):
    """Run a test by test ID

    Args:
        test_id (str, option): The test ID to run - required when running a single test
            i.e. when not running multiple unit metrics
        name (str, optional): The name of the test (used to create a composite metric
            out of multiple unit metrics) - required when running multiple unit metrics
        unit_metrics (list, optional): A list of unit metric IDs to run as a composite
            metric - required when running multiple unit metrics
        params (dict, optional): A dictionary of params to override the default params
        inputs: A dictionary of test inputs to pass to the Test
        output_template (str, optional): A template to use for customizing the output
        show (bool, optional): Whether to display the results. Defaults to True.
        **kwargs: Any extra arguments will be passed in via the TestInput object. i.e.:
            - dataset: A validmind Dataset object or a Pandas DataFrame
            - model: A model to use for the test
            - models: A list of models to use for the test
            other inputs can be accessed inside the test via `self.inputs["input_name"]`
    """
    if not test_id and not name and not unit_metrics:
        raise ValueError(
            "`test_id` or `name` and `unit_metrics` must be provided to run a test"
        )

    if (unit_metrics and not name) or (name and not unit_metrics):
        raise ValueError("`name` and `unit_metrics` must be provided together")

    if test_id and test_id.startswith("validmind.unit_metrics"):
        # TODO: as we move towards a more unified approach to metrics
        # we will want to make everything functional and remove the
        # separation between unit metrics and "normal" metrics
        return run_metric(test_id, inputs=inputs, params=params, show=show)

    if unit_metrics:
        metric_id_name = "".join(word[0].upper() + word[1:] for word in name.split())
        test_id = f"validmind.composite_test.{metric_id_name}"

        error, TestClass = load_composite_metric(
            unit_metrics=unit_metrics, metric_name=metric_id_name
        )

        if error:
            raise LoadTestError(error)

    else:
        TestClass = load_test(test_id, reload=True)

    test = TestClass(
        test_id=test_id,
        context=TestContext(),
        inputs=TestInput({**kwargs, **(inputs or {})}),
        output_template=output_template,
        params=params,
    )

    test.run()

    if show:
        test.result.show()

    return test.result
