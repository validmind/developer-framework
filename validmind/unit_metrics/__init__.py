# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import hashlib
import json
from importlib import import_module

from validmind.input_registry import input_registry
from validmind.tests.decorator import _build_result, _inspect_signature
from validmind.utils import get_model_info, test_id_to_name

unit_metric_results_cache = {}


def _serialize_params(params):
    """
    Serialize the parameters to a unique hash, handling None values.
    This function serializes the parameters dictionary to a JSON string,
    then creates a SHA-256 hash of the string to ensure a unique identifier
    for the parameters. If params is None, a default hash is returned.

    Args:
        params (dict or None): The parameters to be serialized.

    Returns:
        str: A SHA-256 hash of the JSON string representation of the params,
             or a default hash if params is None.
    """
    if params is None:
        # Handle None by returning a hash of an empty dictionary or a predefined value
        params_json = json.dumps({})
    else:
        params_json = json.dumps(params, sort_keys=True)

    hash_object = hashlib.sha256(params_json.encode())
    return hash_object.hexdigest()


def _serialize_model(model):
    """
    Generate a SHA-256 hash for a scikit-learn model based on its type and parameters.

    Args:
        model VMModel: The model to be serialized.

    Returns:
        str: A SHA-256 hash of the model's description.
    """

    model_info = get_model_info(model)

    model_json = json.dumps(model_info, sort_keys=True)

    # Create a SHA-256 hash of the JSON string
    hash_object = hashlib.sha256(model_json.encode())
    return hash_object.hexdigest()


def _serialize_dataset(dataset, model):
    """
    Serialize the description of the dataset input to a unique hash.

    This function generates a hash based on the dataset's structure, including
    the target and feature columns, the prediction column associated with a specific model ID,
    and directly incorporates the model ID and prediction column name to ensure uniqueness.

    Args:
        dataset: The dataset object, which should have properties like _df (pandas DataFrame),
                 target_column (string), feature_columns (list of strings), and extra_columns (dict).
        model (VMModel): The model whose predictions will be included in the serialized dataset

    Returns:
        str: MD5 hash of the dataset

    Note:
        Including the model ID and prediction column name in the hash calculation ensures uniqueness,
        especially in cases where the predictions are sparse or the dataset has not significantly changed.
        This approach guarantees that the hash will distinguish between model-generated predictions
        and pre-computed prediction columns, addressing potential hash collisions.
    """
    return _fast_hash(
        dataset.df[
            [
                *dataset.feature_columns,
                dataset.target_column,
                dataset.prediction_column(model),
            ]
        ]
    )


def _fast_hash(df, sample_size=1000):
    """
    Generates a fast hash by sampling, converting to string and md5 hashing.

    Args:
        df (pd.DataFrame): The DataFrame to hash.
        sample_size (int): The maximum number of rows to include in the sample.

    Returns:
        str: MD5 hash of the DataFrame.
    """
    df_sample = df.sample(n=min(sample_size, len(df)), random_state=42)

    return hashlib.md5(
        df_sample.to_string(header=True, index=True).encode()
    ).hexdigest()


def get_metric_cache_key(metric_id, params, inputs):
    cache_elements = [metric_id]

    # Serialize params if not None
    serialized_params = _serialize_params(params) if params else "None"
    cache_elements.append(serialized_params)

    # Check if 'inputs' is a dictionary
    if not isinstance(inputs, dict):
        raise TypeError("Expected 'inputs' to be a dictionary.")

    # Check for 'model' and 'dataset' keys in 'inputs'
    if "model" not in inputs or "dataset" not in inputs:
        raise ValueError("Missing 'model' or 'dataset' in 'inputs'.")

    dataset = inputs["dataset"]
    model = inputs["model"]

    cache_elements.append(_serialize_dataset(dataset, model))

    cache_elements.append(_serialize_model(model))

    # Combine elements to form the cache key
    combined_elements = "_".join(cache_elements)
    key = hashlib.sha256(combined_elements.encode()).hexdigest()
    return key


def load_metric(metric_id):
    """Load a metric class from a string

    Args:
        metric_id (str): The metric id (e.g. 'validmind.unit_metrics.classification.sklearn.F1')

    Returns:
        callable: The metric function
    """
    return getattr(import_module(metric_id), metric_id.split(".")[-1])


def run_metric(metric_id, inputs=None, params=None, show=True, value_only=False):
    """Run a single metric and cache the results

    Args:
        metric_id (str): The metric id (e.g. 'validmind.unit_metrics.classification.sklearn.F1')
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

    cache_key = get_metric_cache_key(metric_id, params, inputs)

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
        )

    value = unit_metric_results_cache[cache_key][0]

    if value_only:
        return value

    output_template = f"""
    <table>
        <thead>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>{test_id_to_name(metric_id)}</strong></td>
                <td>{value:.4f}</td>
            </tr>
        </tbody>
    </table>
    <style>
        th, td {{
            padding: 5px;
            text-align: left;
        }}
    </style>
    """
    result = _build_result(
        results=value,
        test_id=metric_id,
        description="",
        output_template=output_template,
        inputs=unit_metric_results_cache[cache_key][1],
    )

    # in case the user tries to log the result object
    def log():
        raise Exception(
            "Cannot log unit metrics directly..."
            "You can run this unit metric as part of a composite metric and log that"
        )

    result.log = log

    if show:
        result.show()

    return result
