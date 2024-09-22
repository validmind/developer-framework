# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import glob
import hashlib
import json
import os
from importlib import import_module
from textwrap import dedent

from IPython.display import Markdown, display

from validmind.input_registry import input_registry
from validmind.tests.decorator import _build_result, _inspect_signature
from validmind.utils import test_id_to_name

unit_metric_results_cache = {}


def _serialize_dataset(dataset, model=None, sample_size=1000):
    columns = [*dataset.feature_columns, dataset.target_column]
    if model:
        columns.append(dataset.prediction_column(model))

    df = dataset._df[columns]

    return hashlib.md5(
        df.sample(n=min(sample_size, df.shape[0]), random_state=42)
        .to_string(header=True, index=True)
        .encode()
    ).hexdigest()


def _get_metric_cache_key(metric_id, inputs, params):
    cache_elements = [
        metric_id,
        hashlib.md5(json.dumps(params, sort_keys=True).encode()).hexdigest(),
    ]

    if "model" in inputs:
        cache_elements.append(inputs["model"].input_id)

    if "dataset" in inputs:
        cache_elements.append(inputs["dataset"].input_id)
        cache_elements.append(
            _serialize_dataset(inputs["dataset"], inputs.get("model"))
        )

    return hashlib.md5("_".join(cache_elements).encode()).hexdigest()


def describe_metric(metric_id, raw=False):
    """Describe a metric

    Args:
        metric_id (str): The metric id (e.g. 'validmind.unit_metrics.classification.F1')
        raw (bool): Whether to return the description as a dictionary

    Returns:
        dict: A dictionary containing the metric description
    """
    metric = load_metric(metric_id)
    inputs, params = _inspect_signature(metric)

    if raw:
        return {
            "id": metric_id,
            "description": metric.__doc__,
            "inputs": inputs,
            "params": params,
        }

    inputs = ", ".join(inputs.keys())
    params = ", ".join(params.keys())
    description_md = f"""
    ### {test_id_to_name(metric_id)} (*'{metric_id}'*)

    {metric.__doc__ or ""}

    **Inputs**: {inputs}

    **Parameters**: {params}
    """
    display(Markdown(dedent(description_md)))


def list_metrics():
    """List all available metrics

    Returns:
        list: A list of metric ids
    """
    # current directory of this file is the __init__.py file in the validmind/unit_metrics directory
    # glob for all metrics in the unit_metrics directory (indicated by capitalized python files)
    # recursive since we want to include subdirectories
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    return [
        f"{__name__}.{os.path.relpath(metric, curr_dir).replace('/', '.')[:-3]}"
        for metric in glob.glob(f"{curr_dir}/**/*.py", recursive=True)
        if os.path.isfile(metric) and os.path.basename(metric)[0].isupper()
    ]


def load_metric(metric_id):
    """Load a metric class from a string

    Args:
        metric_id (str): The metric id (e.g. 'validmind.unit_metrics.classification.F1')

    Returns:
        callable: The metric function
    """
    return getattr(import_module(metric_id), metric_id.split(".")[-1])


def run_metric(metric_id, inputs=None, params=None, show=True, value_only=False):
    """Run a single metric and cache the results

    Args:
        metric_id (str): The metric id (e.g. 'validmind.unit_metrics.classification.F1')
        inputs (dict): A dictionary of the metric inputs
        params (dict): A dictionary of the metric parameters
        show (bool): Whether to display the results
        value_only (bool): Whether to return only the value
    """
    inputs = {
        k: input_registry.get(v) if isinstance(v, str) else v
        for k, v in (inputs or {}).items()
    }
    params = params or {}

    cache_key = _get_metric_cache_key(metric_id, inputs, params)

    if cache_key not in unit_metric_results_cache:
        metric = load_metric(metric_id)
        _inputs, _params = _inspect_signature(metric)

        result = metric(
            **{k: v for k, v in inputs.items() if k in _inputs.keys()},
            **{
                k: v
                for k, v in params.items()
                if k in _params.keys() or "kwargs" in _params.keys()
            },
        )
        unit_metric_results_cache[cache_key] = (
            result,
            # store the input ids that were used to calculate the result
            [v.input_id for v in inputs.values()],
            # store the params that were used to calculate the result
            params,
        )

    cached_result = unit_metric_results_cache[cache_key]

    if value_only:
        return cached_result[0]

    result_wrapper = _build_result(
        results=cached_result[0],
        test_id=metric_id,
        inputs=cached_result[1],
        params=cached_result[2],
        generate_description=False,
    )

    if show:
        result_wrapper.show()

    return result_wrapper
