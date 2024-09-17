# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from itertools import product
from typing import Any, Dict, List, Union
from uuid import uuid4

import pandas as pd

from validmind.ai.test_descriptions import get_description_metadata
from validmind.errors import LoadTestError
from validmind.logging import get_logger
from validmind.unit_metrics import run_metric
from validmind.unit_metrics.composite import load_composite_metric
from validmind.vm_models import (
    MetricResult,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestContext,
    TestInput,
    ThresholdTestResults,
)
from validmind.vm_models.figure import is_matplotlib_figure, is_plotly_figure
from validmind.vm_models.test.result_wrapper import (
    MetricResultWrapper,
    ThresholdTestResultWrapper,
)

from .__types__ import TestID
from .load import load_test

logger = get_logger(__name__)


def _cartesian_product(input_grid: Dict[str, List[Any]]):
    """Get all possible combinations for a set of inputs"""
    return [dict(zip(input_grid, values)) for values in product(*input_grid.values())]


def _combine_summaries(summaries: List[Dict[str, Any]]):
    """Combine the summaries from multiple results

    Args:
        summaries (List[Dict[str, Any]]): A list of dictionaries where each dictionary
            has two keys: "inputs" and "summary". The "inputs" key should contain the
            inputs used for the test and the "summary" key should contain the actual
            summary object.

    Constraint: The summaries must all have the same structure meaning that each has
    the same number of tables in the same order with the same columns etc. This
    should always be the case for comparison tests since its the same test run
    multiple times with different inputs.
    """
    if not summaries[0]["summary"]:
        return None

    def combine_tables(table_index):
        combined_df = pd.DataFrame()

        for summary_obj in summaries:
            serialized = summary_obj["summary"].results[table_index].serialize()
            summary_df = pd.DataFrame(serialized["data"])
            summary_df = pd.concat(
                [
                    pd.DataFrame(summary_obj["inputs"], index=summary_df.index),
                    summary_df,
                ],
                axis=1,
            )
            combined_df = pd.concat([combined_df, summary_df], ignore_index=True)

        return ResultTable(
            data=combined_df.to_dict(orient="records"),
            metadata=summaries[0]["summary"].results[table_index].metadata,
        )

    return ResultSummary(
        results=[
            combine_tables(table_index)
            for table_index in range(len(summaries[0]["summary"].results))
        ]
    )


def _get_input_id(v):
    if isinstance(v, str):
        return v  # If v is a string, return it as is.
    elif isinstance(v, list) and all(hasattr(item, "input_id") for item in v):
        # If v is a list and all items have an input_id attribute, join their input_id values.
        return ", ".join(item.input_id for item in v)
    elif hasattr(v, "input_id"):
        return v.input_id  # If v has an input_id attribute, return it.
    return str(v)  # Otherwise, return the string representation of v.


def _update_plotly_titles(figures, input_group, title_template):
    for figure in figures:

        current_title = figure.figure.layout.title.text

        input_description = " and ".join(
            f"{key}: {_get_input_id(value)}" for key, value in input_group.items()
        )

        figure.figure.layout.title.text = title_template.format(
            current_title=f"{current_title} " if current_title else "",
            input_description=input_description,
        )


def _update_matplotlib_titles(figures, input_group, title_template):
    for figure in figures:

        current_title = (
            figure.figure._suptitle.get_text() if figure.figure._suptitle else ""
        )

        input_description = " and ".join(
            f"{key}: {_get_input_id(value)}" for key, value in input_group.items()
        )

        figure.figure.suptitle(
            title_template.format(
                current_title=f"{current_title} " if current_title else "",
                input_description=input_description,
            )
        )


def _combine_figures(figure_lists: List[List[Any]], input_groups: List[Dict[str, Any]]):
    """Combine the figures from multiple results"""
    if not figure_lists[0]:
        return None

    title_template = "{current_title}({input_description})"

    for idx, figures in enumerate(figure_lists):
        input_group = input_groups[idx]
        if is_plotly_figure(figures[0].figure):
            _update_plotly_titles(figures, input_group, title_template)
        elif is_matplotlib_figure(figures[0].figure):
            _update_matplotlib_titles(figures, input_group, title_template)
        else:
            logger.warning("Cannot properly annotate png figures")

    return [figure for figures in figure_lists for figure in figures]


def _combine_unit_metrics(results: List[MetricResultWrapper]):
    if not results[0].scalar:
        return

    for result in results:
        table = ResultTable(
            data=[{"value": result.scalar}],
            metadata=ResultTableMetadata(title="Unit Metrics"),
        )
        if not result.metric:
            result.metric = MetricResult(
                ref_id="will_be_overwritten",
                key=result.result_id,
                value=result.scalar,
                summary=ResultSummary(results=[table]),
            )
        else:
            result.metric.summary.results.append(table)


def metric_comparison(
    results: List[MetricResultWrapper],
    test_id: TestID,
    input_groups: Union[Dict[str, List[Any]], List[Dict[str, Any]]],
    output_template: str = None,
    generate_description: bool = True,
):
    """Build a comparison result for multiple metric results"""
    ref_id = str(uuid4())

    input_group_strings = []

    for group in input_groups:
        new_group = {}
        for k, v in group.items():
            if isinstance(v, str):
                new_group[k] = v
            elif hasattr(v, "input_id"):
                new_group[k] = v.input_id
            elif isinstance(v, list) and all(hasattr(item, "input_id") for item in v):
                new_group[k] = ", ".join([item.input_id for item in v])
            else:
                raise ValueError(f"Unsupported type for value: {v}")
        input_group_strings.append(new_group)

    # handle unit metrics (scalar values) by adding it to the summary
    _combine_unit_metrics(results)

    # Check if the results list contains a result object with a metric
    if any(
        hasattr(result, "metric")
        and hasattr(result.metric, "summary")
        and result.metric.summary
        for result in results
    ):
        # Compute merged summaries only if there is a result with a metric
        merged_summary = _combine_summaries(
            [
                {"inputs": input_group_strings[i], "summary": result.metric.summary}
                for i, result in enumerate(results)
            ]
        )
    else:
        merged_summary = None

    # Check if the results list contains a result object with figures
    if any(hasattr(result, "figures") and result.figures for result in results):
        # Compute merged figures only if there is at least one result with figures
        merged_figures = _combine_figures(
            [result.figures for result in results],
            input_groups,
        )
        # Patch figure metadata so they are connected to the comparison result
        if merged_figures and len(merged_figures):
            for i, figure in enumerate(merged_figures):
                figure.key = f"{figure.key}-{i}"
                figure.metadata["_name"] = test_id
                figure.metadata["_ref_id"] = ref_id
    else:
        merged_figures = None

    return MetricResultWrapper(
        result_id=test_id,
        result_metadata=[
            get_description_metadata(
                test_id=test_id,
                default_description=f"Comparison test result for {test_id}",
                summary=merged_summary.serialize() if merged_summary else None,
                figures=merged_figures if merged_figures else None,
                should_generate=generate_description,
            ),
        ],
        inputs=[
            item.input_id if hasattr(item, "input_id") else item
            for group in input_groups
            for input in group.values()
            for item in (input if isinstance(input, list) else [input])
            if hasattr(item, "input_id") or isinstance(item, str)
        ],
        output_template=output_template,
        metric=MetricResult(
            key=test_id,
            ref_id=ref_id,
            value=[],
            summary=merged_summary,
        ),
        figures=merged_figures,
    )


def threshold_test_comparison(
    results: List[ThresholdTestResultWrapper],
    test_id: TestID,
    input_groups: Union[Dict[str, List[Any]], List[Dict[str, Any]]],
    output_template: str = None,
    generate_description: bool = True,
):
    """Build a comparison result for multiple threshold test results"""
    ref_id = str(uuid4())

    input_group_strings = []

    for group in input_groups:
        new_group = {}
        for k, v in group.items():
            if isinstance(v, str):
                new_group[k] = v
            elif hasattr(v, "input_id"):
                new_group[k] = v.input_id
            elif isinstance(v, list) and all(hasattr(item, "input_id") for item in v):
                new_group[k] = ", ".join([item.input_id for item in v])
            else:
                raise ValueError(f"Unsupported type for value: {v}")
        input_group_strings.append(new_group)

    merged_summary = _combine_summaries(
        [
            {"inputs": input_group_strings[i], "summary": result.test_results.summary}
            for i, result in enumerate(results)
        ]
    )
    merged_figures = _combine_figures(
        [result.figures for result in results], input_groups
    )

    # Patch figure metadata so they are connected to the comparison result
    if merged_figures and len(merged_figures):
        for i, figure in enumerate(merged_figures):
            figure.key = f"{figure.key}-{i}"
            figure.metadata["_name"] = test_id
            figure.metadata["_ref_id"] = ref_id

    return ThresholdTestResultWrapper(
        result_id=test_id,
        result_metadata=[
            get_description_metadata(
                test_id=test_id,
                default_description=f"Comparison test result for {test_id}",
                summary=merged_summary.serialize() if merged_summary else None,
                figures=merged_figures,
                prefix="test_description",
                should_generate=generate_description,
            )
        ],
        inputs=[
            input if isinstance(input, str) else input.input_id
            for group in input_groups
            for input in group.values()
        ],
        output_template=output_template,
        test_results=ThresholdTestResults(
            test_name=test_id,
            ref_id=ref_id,
            # TODO: when we have param_grid support, this will need to be updated
            params=results[0].test_results.params,
            passed=all(result.test_results.passed for result in results),
            results=[],
            summary=merged_summary,
        ),
        figures=merged_figures,
    )


def run_comparison_test(
    test_id: TestID,
    input_grid: Union[Dict[str, List[Any]], List[Dict[str, Any]]],
    name: str = None,
    unit_metrics: List[TestID] = None,
    params: Dict[str, Any] = None,
    show: bool = True,
    output_template: str = None,
    generate_description: bool = True,
):
    """Run a comparison test"""
    if isinstance(input_grid, dict):
        input_groups = _cartesian_product(input_grid)
    else:
        input_groups = input_grid

    results = [
        run_test(
            test_id,
            name=name,
            unit_metrics=unit_metrics,
            inputs=inputs,
            show=False,
            params=params,
            __generate_description=False,
        )
        for inputs in input_groups
    ]

    if isinstance(results[0], MetricResultWrapper):
        func = metric_comparison
    else:
        func = threshold_test_comparison

    result = func(results, test_id, input_groups, output_template, generate_description)

    if show:
        result.show()

    return result


def run_test(
    test_id: TestID = None,
    params: Dict[str, Any] = None,
    inputs: Dict[str, Any] = None,
    input_grid: Union[Dict[str, List[Any]], List[Dict[str, Any]]] = None,
    name: str = None,
    unit_metrics: List[TestID] = None,
    output_template: str = None,
    show: bool = True,
    __generate_description: bool = True,
    **kwargs,
) -> Union[MetricResultWrapper, ThresholdTestResultWrapper]:
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

    if unit_metrics:
        metric_id_name = "".join(word[0].upper() + word[1:] for word in name.split())
        test_id = f"validmind.composite_metric.{metric_id_name}" or test_id

    if input_grid:
        return run_comparison_test(
            test_id,
            input_grid,
            name=name,
            unit_metrics=unit_metrics,
            params=params,
            output_template=output_template,
            show=show,
            generate_description=__generate_description,
        )

    if test_id.startswith("validmind.unit_metrics"):
        # TODO: as we move towards a more unified approach to metrics
        # we will want to make everything functional and remove the
        # separation between unit metrics and "normal" metrics
        return run_metric(test_id, inputs=inputs, params=params, show=show)

    if unit_metrics:
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
        generate_description=__generate_description,
    )

    test.run()

    if show:
        test.result.show()

    return test.result
