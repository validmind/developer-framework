# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import hashlib
import importlib
import json

import numpy as np

from validmind.vm_models import TestInput

from ..utils import get_model_info

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


def _serialize_dataset(dataset, model_id):
    """
    Serialize the description of the dataset input to a unique hash.

    This function generates a hash based on the dataset's structure, including
    the target and feature columns, the prediction column associated with a specific model ID,
    and directly incorporates the model ID and prediction column name to ensure uniqueness.

    Args:
        dataset: The dataset object, which should have properties like _df (pandas DataFrame),
                 target_column (string), feature_columns (list of strings), and _extra_columns (dict).
        model_id (str): The ID of the model associated with the prediction column.

    Returns:
        str: A SHA-256 hash representing the dataset.

    Note:
        Including the model ID and prediction column name in the hash calculation ensures uniqueness,
        especially in cases where the predictions are sparse or the dataset has not significantly changed.
        This approach guarantees that the hash will distinguish between model-generated predictions
        and pre-computed prediction columns, addressing potential hash collisions.
    """

    # Access the prediction column for the given model ID from the dataset's extra columns
    prediction_column_name = dataset._extra_columns["prediction_columns"][model_id]

    # Include model ID and prediction column name directly in the hash calculation
    model_and_prediction_info = f"{model_id}_{prediction_column_name}".encode()

    # Start with target and feature columns, and include the prediction column
    columns = (
        [dataset._target_column] + dataset._feature_columns + [prediction_column_name]
    )

    # Use _fast_hash function and include model_and_prediction_info in the hash calculation
    hash_digest = _fast_hash(
        dataset._df[columns], model_and_prediction_info=model_and_prediction_info
    )

    return hash_digest


def _fast_hash(df, sample_size=1000, model_and_prediction_info=None):
    """
    Generates a hash for a DataFrame by sampling and combining its size, content,
    and optionally model and prediction information.

    Args:
        df (pd.DataFrame): The DataFrame to hash.
        sample_size (int): The maximum number of rows to include in the sample.
        model_and_prediction_info (bytes, optional): Additional information to include in the hash.

    Returns:
        str: A SHA-256 hash of the DataFrame's sample and additional information.
    """
    # Convert the number of rows to bytes and include it in the hash calculation
    rows_bytes = str(len(df)).encode()

    # Sample rows if DataFrame is larger than sample_size, ensuring reproducibility
    if len(df) > sample_size:
        df_sample = df.sample(n=sample_size, random_state=42)
    else:
        df_sample = df

    # Convert the sampled DataFrame to a byte array. np.asarray ensures compatibility with various DataFrame contents.
    byte_array = np.asarray(df_sample).data.tobytes()

    # Initialize the hash object and update it with the row count, data bytes, and additional info
    hash_obj = hashlib.sha256(
        rows_bytes + byte_array + (model_and_prediction_info or b"")
    )

    return hash_obj.hexdigest()


def _get_metric_class(metric_id):
    """Get the metric class by metric_id

    This function will load the metric class by metric_id.

    Args:
        metric_id (str): The full metric id (e.g. 'validmind.vm_models.test.v2.model_validation.sklearn.F1')

    Returns:
        Metric: The metric class
    """

    metric_module = importlib.import_module(f"{metric_id}")

    class_name = metric_id.split(".")[-1]

    # Access the class within the F1 module
    metric_class = getattr(metric_module, class_name)

    return metric_class


def get_input_type(input_obj):
    """
    Determines whether the input object is a 'dataset' or 'model' based on its class module path.

    Args:
        input_obj: The object to type check.

    Returns:
        str: 'dataset' or 'model' depending on the object's module, or raises ValueError.
    """
    # Obtain the class object of input_obj (for clarity and debugging)
    class_obj = input_obj.__class__

    # Obtain the module name as a string from the class object
    class_module = class_obj.__module__

    if "validmind.vm_models.dataset" in class_module:
        return "dataset"
    elif "validmind.models" in class_module:
        return "model"
    else:
        raise ValueError("Input must be of type validmind Dataset or Model")


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
    model_id = model.input_id

    cache_elements.append(_serialize_dataset(dataset, model_id))

    cache_elements.append(_serialize_model(model))

    # Combine elements to form the cache key
    combined_elements = "_".join(cache_elements)
    key = hashlib.sha256(combined_elements.encode()).hexdigest()
    return key


def run_metric(metric_id=None, inputs=None, params=None):
    """Run a single metric

    This function provides a high level interface for running a single metric. A metric
    is a single test that calculates a value based on the input data.

    Args:
        metric_id (str): The metric name (e.g. 'F1')
        params (dict): A dictionary of the metric parameters

    Returns:
        MetricResult: The metric result object
    """
    cache_key = get_metric_cache_key(metric_id, params, inputs)

    # Check if the metric value already exists in the global variable
    if cache_key in unit_metric_results_cache:
        return unit_metric_results_cache[cache_key]

    # Load the metric class by metric_id
    metric_class = _get_metric_class(metric_id)

    # Initialize the metric
    metric = metric_class(test_id=metric_id, inputs=TestInput(inputs), params=params)

    # Run the metric
    result = metric.run()

    cache_key = get_metric_cache_key(metric_id, params, inputs)

    unit_metric_results_cache[cache_key] = result

    return result
