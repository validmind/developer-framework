import pandas as pd
import json
import hashlib
import importlib

from ..utils import get_model_info


global_metric_values = {}

def _serialize_params(params):
    """
    Serialize the parameters to a unique hash.

    This function serializes the parameters dictionary to a JSON string,
    then creates a SHA-256 hash of the string to ensure a unique identifier
    for the parameters.

    Args:
        params (dict): The parameters to be serialized.

    Returns:
        str: A SHA-256 hash of the JSON string representation of the params.
    """
    # Convert the params to a JSON string, ensuring consistent ordering
    params_json = json.dumps(params, sort_keys=True)

    # Create a SHA-256 hash of the JSON string
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

    if model is None:
        # You can return a predefined hash, or handle it in another appropriate way
        model_info = "none_model_hash"
    else:
        model_info = get_model_info(model)

    model_json = json.dumps(model_info, sort_keys=True)

    # Create a SHA-256 hash of the JSON string
    hash_object = hashlib.sha256(model_json.encode())
    return hash_object.hexdigest()

def _serialize_dataset(dataset):
    """
    Serialize the description of the dataset input to a unique hash.

    This function generates descriptive statistics of the dataset, converts
    the description to a JSON string, and then creates a SHA-256 hash of the string
    to ensure a unique identifier for the dataset's description.

    Args:
        dataset (pd.DataFrame): The dataset whose description is to be serialized.

    Returns:
        str: A SHA-256 hash of the JSON string representation of the dataset's description.
    """
    if isinstance(dataset._df, pd.DataFrame):
        # Get the description of the DataFrame
        columns = [dataset.target_column] + dataset.feature_columns
        description = dataset._df[columns].describe()
        # Convert the description DataFrame to a JSON string
        description_json = json.dumps(
            description.to_dict(orient="records"), sort_keys=True
        )
        # Create a SHA-256 hash of the JSON string
        hash_object = hashlib.sha256(description_json.encode())
        return hash_object.hexdigest()
    else:
        # If it's not a DataFrame, we cannot get a description
        raise TypeError("The dataset provided is not a pandas DataFrame.")

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

def get_metric_value(metric_id, inputs=None):
    """
    Get the metric value, either by loading it from a global variable or by computing it,
    ensuring that the inputs are the same.

    Args:
        metric_id (str): The metric name (e.g., 'F1').
        inputs (dict, optional): Inputs necessary to compute the metric.

    Returns:
        The metric value.
    """
    # Serialize the inputs to ensure we can compare them
    serialized_dataset = _serialize_dataset(inputs.get("dataset"))

    # Use a tuple of the metric_id and the serialized inputs as the cache key
    cache_key = (metric_id, serialized_dataset)

    # Check if the metric value already exists in the global variable
    if cache_key in global_metric_values:
        print(f"Loading last computed value value from '{metric_id}'")
        return global_metric_values[cache_key]
    else:
        # Compute the metric value
        print(f"Computing metric value for '{metric_id}'")
        result = run_metric(metric_id, inputs=inputs)
        # Store the computed value in the global variable
        global_metric_values[cache_key] = result
        return result
    
def run_metric(metric_id, inputs=None, params=None):
    """Run a single metric

    This function provides a high level interface for running a single metric. A metric
    is a single test that calculates a value based on the input data.

    Args:
        metric_id (str): The metric name (e.g. 'F1')
        metric_value (dict): A dictionary of the metric value

    Returns:
        MetricResult: The metric result object
    """

    # Serialize the inputs to ensure we can compare them
    serialized_dataset = _serialize_dataset(inputs.get("dataset"))

    # Serialize the params to ensure we can compare them
    serialized_params = _serialize_params(params)

    serialized_model = _serialize_model(inputs.get("model"))

    # Use a tuple of the metric_id and the serialized inputs as the cache key
    cache_key = (metric_id, serialized_dataset, serialized_params, serialized_model)

    # Check if the metric value already exists in the global variable
    if cache_key in global_metric_values:
        print(f"Loading last computed value value from '{metric_id}'")
        return global_metric_values[cache_key]

    else:
        # Compute the metric value
        print(f"Computing metric value for '{metric_id}'")

        # Load the metric class by metric_id
        metric_class = _get_metric_class(metric_id)

        # Initialize the metric
        metric = metric_class(inputs=inputs, params=params)

        # Run the metric
        result = metric.run()

        # Serialize the inputs to ensure we can compare them
        serialized_dataset = _serialize_dataset(inputs.get("dataset"))

        # Serialize the params to ensure we can compare them
        serialized_params = _serialize_params(params)

        # Serialize the model to ensure we can compare them
        serialized_model = _serialize_model(inputs.get("model"))

        # Use a tuple of the metric_id and the serialized inputs as the cache key
        cache_key = (metric_id, serialized_dataset, serialized_params, serialized_model)

        global_metric_values[cache_key] = result

        return result