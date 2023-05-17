"""
API Client
"""
import json
import os
from io import BytesIO

import requests

from .utils import NumpyEncoder
from .utils import get_full_typename, is_matplotlib_typename

API_HOST = os.environ.get("VM_API_HOST", "http://127.0.0.1:5000/api/v1/tracking")
API_PROJECT = os.environ.get("VM_API_PROJECT")
VALID_DATASET_TYPES = ["training", "test", "validation"]

vm_api_key = None
vm_api_secret = None

api_session = requests.Session()


def get_api_host():
    return API_HOST


def get_api_project():
    return API_PROJECT


def __ping():
    r = api_session.get(f"{API_HOST}/ping")

    # TODO: handle 401
    if r.status_code != 200:
        print("Unsuccessful ping to ValidMind API")
        raise Exception(r.text)

    project_info = r.json()

    if "name" in project_info:
        print(
            f"Connected to ValidMind. Project: {project_info['name']} ({project_info['cuid']})"
        )
    else:
        print("Connected to ValidMind")


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
    Initializes the API client instances and calls the /ping endpoint to ensure
    the provided credentials are valid and we can connect to the ValidMind API.

    If the API key and secret are not provided, the client will attempt to
    retrieve them from the environment variables `VM_API_KEY` and `VM_API_SECRET`.

    Args:
        project (str): The project CUID
        api_key (str, optional): The API key. Defaults to None.
        api_secret (str, optional): The API secret. Defaults to None.
        api_host (str, optional): The API host. Defaults to None.

    Raises:
        ValueError: If the API key and secret are not provided

    Returns:
        bool: True if the ping was successful
    """
    global API_HOST
    global API_PROJECT

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

    API_PROJECT = project

    return __ping()


def log_dataset(vm_dataset):
    """
    Logs metadata and statistics about a dataset to ValidMind API.

    Args:
        vm_dataset (validmind.VMDataset): A VM dataset object
        dataset_type (str, optional): The type of dataset. Can be one of "training", "test", or "validation". Defaults to "training".
        dataset_options (dict, optional): Additional dataset options for analysis. Defaults to None.
        dataset_targets (validmind.DatasetTargets, optional): A list of targets for the dataset. Defaults to None.
        features (list, optional): Optional. A list of features metadata. Defaults to None.

    Raises:
        Exception: If the API call fails

    Returns:
        validmind.VMDataset: The VMDataset object
    """
    payload = json.dumps(vm_dataset.serialize(), cls=NumpyEncoder, allow_nan=False)
    r = api_session.post(
        f"{API_HOST}/log_dataset",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    if r.status_code != 200:
        print("Could not log dataset to ValidMind API")
        raise Exception(r.text)

    return vm_dataset


def log_metadata(content_id, text=None, extra_json=None):
    """
    Logs free-form metadata to ValidMind API. This function is not exported on purpose.
    To use it you must import it from the validmind.api_client module like this:
        `from validmind.api_client import log_metadata`

    Args:
        content_id (str): Unique content identifier for the metadata
        text (str, optional): Free-form text to assign to the metadata. Defaults to None.
        extra_json (dict, optional): Free-form key-value pairs to assign to the metadata. Defaults to None.

    Raises:
        Exception: If the API call fails

    Returns:
        bool: True if the API call was successful
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
        data=json.dumps(metadata_dict, cls=NumpyEncoder, allow_nan=False),
        headers={"Content-Type": "application/json"},
    )

    if r.status_code != 200:
        print("Could not log metadata to ValidMind API")
        raise Exception(r.text)

    return True


def get_metadata(content_id):
    """
    Gets a metadata object from ValidMind API.

    Args:
        content_id (str): Unique content identifier for the metadata

    Raises:
        Exception: If the API call fails

    Returns:
        bool: Metadata object
    """
    r = api_session.get(f"{API_HOST}/get_metadata/{content_id}")

    if r.status_code == 404:
        return None
    if r.status_code != 200:
        print("Could not retrieve metadata from ValidMind API")
        raise Exception(r.text)

    return r.json()


def log_model(vm_model):
    """
    Logs model metadata and hyperparameters to ValidMind API.

    Args:
        vm_model (validmind.VMModel): A VM model object

    Raises:
        Exception: If the API call fails

    Returns:
        bool: True if the API call was successful
    """
    r = api_session.post(
        f"{API_HOST}/log_model",
        data=json.dumps(vm_model.serialize(), cls=NumpyEncoder, allow_nan=False),
        headers={"Content-Type": "application/json"},
    )

    if r.status_code != 200:
        print("Could not log model to ValidMind API")
        raise Exception(r.text)

    return True


def log_metrics(metrics, run_cuid=None):
    """
    Logs metrics to ValidMind API.

    Args:
        metrics (list): A list of Metric objects
        run_cuid (str, optional): The run CUID. If not provided, a new run will be created. Defaults to None.

    Raises:
        Exception: If the API call fails

    Returns:
        bool: True if the API call was successful
    """
    if run_cuid is None:
        run_cuid = start_run()

    serialized_metrics = [m.serialize() for m in metrics]

    r = api_session.post(
        f"{API_HOST}/log_metrics?run_cuid={run_cuid}",
        data=json.dumps(serialized_metrics, cls=NumpyEncoder, allow_nan=False),
        headers={"Content-Type": "application/json"},
    )

    if r.status_code != 200:
        print("Could not log metrics to ValidMind API")
        raise Exception(r.text)

    return True


def log_test_result(result, run_cuid=None, dataset_type="training"):
    """
    Logs test results information. This method will be called automatically be any function
    running tests but can also be called directly if the user wants to run tests on their own.

    Args:
        result (validmind.TestResults): A TestResults object
        run_cuid (str, optional): The run CUID. If not provided, a new run will be created. Defaults to None.
        dataset_type (str, optional): The type of dataset. Can be one of "training", "test", or "validation". Defaults to "training".

    Raises:
        Exception: If the API call fails

    Returns:
        bool: True if the API call was successful
    """
    if run_cuid is None:
        run_cuid = start_run()

    r = api_session.post(
        f"{API_HOST}/log_test_results?run_cuid={run_cuid}&dataset_type={dataset_type}",
        data=json.dumps(result.serialize(), cls=NumpyEncoder, allow_nan=False),
        headers={"Content-Type": "application/json"},
    )

    # Exit on the first error
    if r.status_code != 200:
        print("Could not log test results to ValidMind API")
        raise Exception(r.text)

    return True


def log_test_results(results, run_cuid=None, dataset_type="training"):
    """
    Logs test results information. This method will be called automatically be any function
    running tests but can also be called directly if the user wants to run tests on their own.

    Args:
        results (list): A list of TestResults objects
        run_cuid (str, optional): The run CUID. If not provided, a new run will be created. Defaults to None.
        dataset_type (str, optional): The type of dataset. Can be one of "training", "test", or "validation". Defaults to "training".

    Raises:
        Exception: If the API call fails

    Returns:
        bool: True if the API call was successful
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

    Args:
        data_or_path (str or matplotlib.figure.Figure): The path of the image or the data of the plot
        key (str): Identifier of the figure
        metadata (dict): Python data structure
        run_cuid (str, optional): The run CUID. If not provided, a new run will be created. Defaults to None.

    Raises:
        Exception: If the API call fails

    Returns:
        bool: True if the API call was successful
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
        metadata_json = json.dumps(metadata, allow_nan=False)
    except TypeError:
        raise

    res = api_session.post(
        url, files=files, data={"key": key, "type": type_, "metadata": metadata_json}
    )

    if res.status_code != 200:
        print("Could not log figure to ValidMind API")
        raise Exception(res.text)

    return res.json()
