"""
API Client
"""
import json
import os
from io import BytesIO

import requests

from .utils import NumpyEncoder

# from .vm_models import Model, ModelAttributes

# from .model_utils import (
#     # get_info_from_model_instance,
#     # get_params_from_model_instance,
#     # get_training_metrics,
# )
from .utils import get_full_typename, is_matplotlib_typename

API_HOST = os.environ.get("VM_API_HOST", "http://127.0.0.1:5000/api/v1/tracking")
VALID_DATASET_TYPES = ["training", "test", "validation"]

vm_api_key = None
vm_api_secret = None

api_session = requests.Session()


def __ping():
    r = api_session.get(f"{API_HOST}/ping")

    # TODO: handle 401
    if r.status_code != 200:
        print("Unsuccessful ping to ValidMind API")
        raise Exception(r.text)

    return True


def _get_or_create_run_cuid():
    """
    Get the run cuid from the api_session headers.
    Create it when not found.
    """
    if "X-RUN-CUID" in api_session.headers:
        return api_session.headers["X-RUN-CUID"]
    return start_run()


def init(project, api_key=None, api_secret=None, api_host=None):
    """
    Initializes the API client instances and /pings the API
    to ensure the provided credentials are valid.
    """
    global API_HOST

    ENV_API_KEY = os.environ.get("VM_API_KEY")
    ENV_API_SECRET = os.environ.get("VM_API_SECRET")

    vm_api_key = api_key or ENV_API_KEY
    vm_api_secret = api_secret or ENV_API_SECRET

    if api_host is not None:
        API_HOST = api_host

    if vm_api_key is None or vm_api_secret is None:
        raise ValueError(
            "API key and secret must be provided either as environment variables or as arguments to init."
        )

    api_session.headers.update(
        {
            "X-API-KEY": vm_api_key,
            "X-API-SECRET": vm_api_secret,
            "X-PROJECT-CUID": project,
        }
    )

    return __ping()


def log_dataset(vm_dataset):
    """
    Logs metadata and statistics about a dataset to ValidMind API.

    :param dataset: A VM dataset object
    :param dataset_type: The type of dataset. Can be one of "training", "test", or "validation".
    :param dataset_options: Additional dataset options for analysis
    :param dataset_targets: A list of targets for the dataset.
    :param features: Optional. A list of features metadata.
    :type dataset_targets: validmind.DatasetTargets, optional
    """
    payload = json.dumps(vm_dataset.serialize(), cls=NumpyEncoder)
    r = api_session.post(
        f"{API_HOST}/log_dataset",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    if r.status_code != 200:
        print("Could not log dataset to ValidMind API")
        raise Exception(r.text)

    print("Successfully logged dataset metadata and statistics.")

    return vm_dataset


def log_metadata(content_id, text=None, extra_json=None):
    """
    Logs free-form metadata to ValidMind API.

    :param content_id: Unique content identifier for the metadata
    :param text: Free-form text to assign to the metadata
    :param extra_json: Free-form key-value pairs to assign to the metadata
    """
    metadata_dict = {
        "content_id": content_id,
    }

    if text is not None:
        metadata_dict["text"] = text
    if extra_json is not None:
        metadata_dict["json"] = extra_json

    r = api_session.post(
        f"{API_HOST}/log_metadata",
        data=json.dumps(metadata_dict, cls=NumpyEncoder),
        headers={"Content-Type": "application/json"},
    )

    if r.status_code != 200:
        print("Could not log metadata to ValidMind API")
        raise Exception(r.text)

    print("Successfully logged metadata")

    return True


# def log_model(model_instance, vm_model=None):
#     """
#     Logs model metadata and hyperparameters to ValidMind API.

#     :param model_instance: A model instance. Only supports XGBoost at the moment.
#     :param vm_model: A ValidMind Model wrapper instance.
#     :type vm_model: validmind.Model, optional
#     """
#     if vm_model is None:
#         vm_model = Model(
#             attributes=ModelAttributes(),
#         )

#     model_info = get_info_from_model_instance(model_instance)

#     if vm_model.task is None:
#         vm_model.task = model_info["task"]
#     if vm_model.subtask is None:
#         vm_model.subtask = model_info["subtask"]
#     if vm_model.attributes.framework is None:
#         vm_model.attributes.framework = model_info["framework"]
#     if vm_model.attributes.framework_version is None:
#         vm_model.attributes.framework_version = model_info["framework_version"]
#     if vm_model.attributes.architecture is None:
#         vm_model.attributes.architecture = model_info["architecture"]

#     vm_model.params = get_params_from_model_instance(model_instance)

#     r = api_session.post(
#         f"{API_HOST}/log_model",
#         data=json.dumps(vm_model.serialize(), cls=NumpyEncoder),
#         headers={"Content-Type": "application/json"},
#     )

#     if r.status_code != 200:
#         print("Could not log model to ValidMind API")
#         raise Exception(r.text)

#     return True


# def log_training_metrics(model, x_train, y_train, x_val, y_val, run_cuid=None):
#     """
#     Logs training metrics to ValidMind API.

#     :param model: A model instance. Only supports XGBoost at the moment.
#     :param x_train: The training dataset.
#     :param y_train: The training dataset targets.
#     :param x_val: The validation dataset.
#     :param y_val: The validation dataset targets.
#     :param run_cuid: The run CUID. If not provided, a new run will be created.
#     """
#     if run_cuid is None:
#         run_cuid = start_run()

#     training_metrics = get_training_metrics(model, x_train, y_train, x_val, y_val)

#     return log_metrics(training_metrics, run_cuid)


def log_metrics(metrics, run_cuid=None):
    """
    Logs metrics to ValidMind API.

    :param metrics: A list of Metric objects.
    :param run_cuid: The run CUID. If not provided, a new run will be created.
    """
    if run_cuid is None:
        run_cuid = start_run()

    serialized_metrics = [m.serialize() for m in metrics]

    r = api_session.post(
        f"{API_HOST}/log_metrics?run_cuid={run_cuid}",
        data=json.dumps(serialized_metrics, cls=NumpyEncoder),
        headers={"Content-Type": "application/json"},
    )

    if r.status_code != 200:
        print("Could not log metrics to ValidMind API")
        raise Exception(r.text)

    print("Successfully logged metrics")

    return True


def log_test_result(result, run_cuid=None, dataset_type="training"):
    """
    Logs test results information. This method will be called automatically be any function
    running tests but can also be called directly if the user wants to run tests on their own.

    :param result: A TestResults object
    :param run_cuid: The run CUID. If not provided, a new run will be created.
    """
    if run_cuid is None:
        run_cuid = start_run()

    r = api_session.post(
        f"{API_HOST}/log_test_results?run_cuid={run_cuid}&dataset_type={dataset_type}",
        data=json.dumps(result.dict(), cls=NumpyEncoder),
        headers={"Content-Type": "application/json"},
    )

    # Exit on the first error
    if r.status_code != 200:
        print("Could not log test results to ValidMind API")
        raise Exception(r.text)

    print(f"Successfully logged test results for test: {result.test_name}")

    return True


def log_test_results(results, run_cuid=None, dataset_type="training"):
    """
    Logs test results information. This method will be called automatically be any function
    running tests but can also be called directly if the user wants to run tests on their own.

    :param results: A list of TestResults objects
    :param run_cuid: The run CUID. If not provided, a new run will be created.
    """
    if run_cuid is None:
        run_cuid = start_run()

    # TBD - parallelize API requests
    for result in results:
        log_test_result(result, run_cuid, dataset_type)

    return True


def start_run():
    """
    Starts a new test run. This method will return a test run CUID that needs to be
    passed to any functions logging test results to the ValidMind API.

    If "X-RUN-CUID" was already set as an HTTP header to the session, we reuse it
    """
    if api_session.headers.get("X-RUN-CUID") is not None:
        return api_session.headers.get("X-RUN-CUID")

    r = api_session.post(f"{API_HOST}/start_run")

    if r.status_code != 200:
        print("Could not start data logging run with ValidMind API")
        raise Exception(r.text)

    test_run = r.json()
    test_run_cuid = test_run["cuid"]
    api_session.headers.update({"X-RUN-CUID": test_run_cuid})
    return test_run_cuid


def log_figure(data_or_path, key, metadata, run_cuid=None):
    """
    Logs a figure

    :param data_or_path: the path of the image or the data of the plot
    :param key: identifier of the figure
    :param metadata: python data structure
    :param run_cuid: run cuid from start_run
    """
    if not run_cuid:
        run_cuid = _get_or_create_run_cuid()

    url = f"{API_HOST}/log_figure?run_cuid={run_cuid}"

    if isinstance(data_or_path, str):
        type_ = "file_path"
        _, extension = os.path.splitext(data_or_path)
        files = {"image": (f"{key}{extension}", open(data_or_path, "rb"))}
    elif is_matplotlib_typename(get_full_typename(data_or_path)):
        type_ = "plot"
        buffer = BytesIO()
        data_or_path.savefig(buffer, bbox_inches="tight")
        buffer.seek(0)
        files = {"image": (f"{key}.png", buffer, "image/png")}
    else:
        raise ValueError(
            f"data_or_path type not supported: {get_full_typename(data_or_path)}. "
            f"Available supported types: string path or matplotlib"
        )

    try:
        metadata_json = json.dumps(metadata)
    except TypeError:
        raise

    res = api_session.post(
        url, files=files, data={"key": key, "type": type_, "metadata": metadata_json}
    )
    return res.json()
