# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from itertools import product
from typing import Any, Dict, List, Union

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
    output_template: str = None,
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
    params: Dict[str, Any] = None,
    inputs: Dict[str, Any] = None,
    input_grid: Union[Dict[str, List[Any]], List[Dict[str, Any]]] = None,
    name: str = None,
    unit_metrics: List[TestID] = None,
    output_template: str = None,
    show: bool = True,
    **kwargs,
):
    """Run a test by test ID

    Args:
        test_id (TestID, optional): The test ID to run. Not required if `unit_metrics` is provided.
        params (dict, optional): A dictionary of parameters to pass into the test. Params
            are used to customize the test behavior and are specific to each test. See the
            test details for more information on the available parameters. Defaults to None.
        inputs (Dict[str, Any], optional): A dictionary of test inputs to pass into the
            test. Inputs are either models or datasets that have been initialized using
            vm.init_model() or vm.init_dataset(). Defaults to None.
        input_grid (Union[Dict[str, List[Any]], List[Dict[str, Any]]], optional): To run
            a comparison test, provide either a dictionary of inputs where the keys are
            the input names and the values are lists of different inputs, or a list of
            dictionaries where each dictionary is a set of inputs to run the test with.
            This will run the test multiple times with different sets of inputs and then
            combine the results into a single output. When passing a dictionary, the grid
            will be created by taking the Cartesian product of the input lists. Its simply
            a more convenient way of forming the input grid as opposed to passing a list of
            all possible combinations. Defaults to None.
        name (str, optional): The name of the test (used to create a composite metric
            out of multiple unit metrics) - required when running multiple unit metrics
        unit_metrics (list, optional): A list of unit metric IDs to run as a composite
            metric - required when running multiple unit metrics
        output_template (str, optional): A jinja2 html template to customize the output
            of the test. Defaults to None.
        show (bool, optional): Whether to display the results. Defaults to True.
        **kwargs: Keyword inputs to pass into the test (same as `inputs` but as keyword
            args instead of a dictionary):
            - dataset: A validmind Dataset object or a Pandas DataFrame
            - model: A model to use for the test
            - models: A list of models to use for the test
            - dataset: A validmind Dataset object or a Pandas DataFrame
    """
    if not test_id and not name and not unit_metrics:
        raise ValueError(
            "`test_id` or `name` and `unit_metrics` must be provided to run a test"
        )

    if (unit_metrics and not name) or (name and not unit_metrics):
        raise ValueError("`name` and `unit_metrics` must be provided together")

    if (input_grid and kwargs) or (input_grid and inputs):
        raise ValueError(
            "When providing an `input_grid`, you cannot also provide `inputs` or `kwargs`"
        )

    if input_grid:
        return run_comparison_test(
            test_id, input_grid, output_template=output_template, show=show
        )

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
