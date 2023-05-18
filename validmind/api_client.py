"""ValidMind API client

Note that this takes advantage of the fact that python modules are singletons to store and share
the configuration and session across the entire project regardless of where the client is imported.
"""
import asyncio
import json
import os
import urllib.parse
from io import BytesIO

import aiohttp
import requests
from aiohttp import FormData

from .utils import get_full_typename, is_matplotlib_typename, NumpyEncoder, run_async


_api_key = os.environ.get("VM_API_KEY")
_api_secret = os.environ.get("VM_API_SECRET")
_api_host = os.environ.get("VM_API_HOST")

_project = os.environ.get("VM_PROJECT")
_run_cuid = os.environ.get("VM_RUN_CUID")

__api_session: aiohttp.ClientSession = None


def get_api_config():
    return {
        "VM_API_KEY": _api_key,
        "VM_API_SECRET": _api_secret,
        "VM_API_HOST": _api_host,
        "VM_PROJECT": _project,
        "VM_RUN_CUID": _run_cuid,
    }


def get_api_host():
    return _api_host


def get_api_project():
    return _project


def init(project=None, api_key=None, api_secret=None, api_host=None):
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
    global _api_key, _api_secret, _api_host, _run_cuid, _project, api_session

    _api_key = api_key or os.environ.get("VM_API_KEY")
    _api_secret = api_secret or os.environ.get("VM_API_SECRET")

    if _api_key is None or _api_secret is None:
        raise ValueError(
            "API key and secret must be provided either as environment variables or as arguments to init."
        )

    _api_host = api_host or os.environ.get(
        "VM_API_HOST", "http://127.0.0.1:5000/api/v1/tracking"
    )
    _project = project or os.environ.get("VM_API_PROJECT")
    _run_cuid = os.environ.get("VM_RUN_CUID", None)  # this is for sub-processes

    return __ping()


async def _get_session():
    """Initializes the async client session"""
    global __api_session

    if __api_session is None:
        __api_session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
        __api_session.headers.update(
            {
                "X-API-KEY": _api_key,
                "X-API-SECRET": _api_secret,
                "X-PROJECT-CUID": _project,
            }
        )

    return __api_session


def __ping():
    """Validates that we can connect to the ValidMind API (does not use the async session)"""
    r = requests.get(
        f"{_api_host}/ping",
        headers={
            "X-API-KEY": _api_key,
            "X-API-SECRET": _api_secret,
            "X-PROJECT-CUID": _project,
        },
    )

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


async def __get_url(endpoint, params=None):
    if not _run_cuid:
        start_run()

    params = params or {}

    params["run_cuid"] = _run_cuid
    # api_session.headers["X-RUN-CUID"] = _run_cuid

    return f"{_api_host}/{endpoint}?{urllib.parse.urlencode(params)}"


async def _get(endpoint, params=None):
    url = await __get_url(endpoint, params)
    session = await _get_session()
    session.headers.update({"X-RUN-CUID": _run_cuid})

    async with session.get(url) as r:
        if r.status != 200:
            raise Exception(await r.text())

        return await r.json()


async def _post(endpoint, params=None, data=None, files=None):
    url = await __get_url(endpoint, params)
    session = await _get_session()
    session.headers.update({"X-RUN-CUID": _run_cuid})

    if not isinstance(data, dict) and files is not None:
        raise ValueError("Cannot pass both non-json data and file objects to _post")

    if files:
        _data = FormData()

        for key, value in (data or {}).items():
            _data.add_field(key, value)

        for key, file_info in (files or {}).items():
            _data.add_field(
                key,
                file_info[1],
                filename=file_info[0],
                content_type=file_info[2] if len(file_info) > 2 else None,
            )
    else:
        _data = data

    async with session.post(url, data=_data) as r:
        if r.status != 200:
            raise Exception(await r.text())

        return await r.json()


async def get_metadata(content_id):
    """Gets a metadata object from ValidMind API.

    Args:
        content_id (str): Unique content identifier for the metadata

    Raises:
        Exception: If the API call fails

    Returns:
        bool: Metadata object
    """
    return await _get(f"get_metadata/{content_id}")


async def log_dataset(vm_dataset):
    """Logs metadata and statistics about a dataset to ValidMind API.

    Args:
        vm_dataset (validmind.VMDataset): A VM dataset object

    Returns:
        validmind.VMDataset: The VMDataset object
    """
    try:
        await _post(
            "log_dataset",
            data=json.dumps(vm_dataset.serialize(), cls=NumpyEncoder, allow_nan=False),
        )
    except Exception as e:
        print("Error logging dataset to ValidMind API")
        raise e

    return vm_dataset


async def log_figure(data_or_path, key, metadata):
    """Logs a figure
    Args:
        data_or_path (str or matplotlib.figure.Figure): The path of the image or the data of the plot
        key (str): Identifier of the figure
        metadata (dict): Python data structure

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
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

    try:
        return await _post(
            "log_figure",
            data={"type": type_, "key": key, "metadata": metadata_json},
            files=files,
        )
    except Exception as e:
        print("Error logging figure to ValidMind API")
        raise e


async def log_metadata(content_id, text=None, extra_json=None):
    """Logs free-form metadata to ValidMind API.

    Args:
        content_id (str): Unique content identifier for the metadata
        text (str, optional): Free-form text to assign to the metadata. Defaults to None.
        extra_json (dict, optional): Free-form key-value pairs to assign to the metadata. Defaults to None.

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    metadata_dict = {"content_id": content_id}
    if text is not None:
        metadata_dict["text"] = text
    if extra_json is not None:
        metadata_dict["extra_json"] = extra_json

    try:
        return await _post(
            "log_metadata",
            data=json.dumps(metadata_dict, cls=NumpyEncoder, allow_nan=False),
        )
    except Exception as e:
        print("Error logging metadata to ValidMind API")
        raise e


async def log_metrics(metrics):
    """Logs metrics to ValidMind API.

    Args:
        metrics (list): A list of Metric objects

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    try:
        return await _post(
            "log_metrics",
            data=json.dumps(
                [m.serialize() for m in metrics], cls=NumpyEncoder, allow_nan=False
            ),
        )
    except Exception as e:
        print("Error logging metrics to ValidMind API")
        raise e


async def log_model(vm_model):
    """Logs model metadata and hyperparameters to ValidMind API.

    Args:
        vm_model (validmind.VMModel): A VM model object

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    try:
        return await _post(
            "log_model",
            data=json.dumps(vm_model.serialize(), cls=NumpyEncoder, allow_nan=False),
        )
    except Exception as e:
        print("Error logging model to ValidMind API")
        raise e


async def log_test_result(result, dataset_type="training"):
    """Logs test results information

    This method will be called automatically from any function running tests but
    can also be called directly if the user wants to run tests on their own.

    Args:
        result (validmind.TestResults): A TestResults object
        dataset_type (str, optional): The type of dataset. Can be one of
            "training", "test", or "validation". Defaults to "training".

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    try:
        return await _post(
            "log_test_results",
            params={"dataset_type": dataset_type},
            data=json.dumps(result.serialize(), cls=NumpyEncoder, allow_nan=False),
        )
    except Exception as e:
        print("Error logging test results to ValidMind API")
        raise e


def log_test_results(results, dataset_type="training"):
    """Logs test results information

    This method will be called automatically be any function
    running tests but can also be called directly if the user wants to run tests on their own.

    Args:
        results (list): A list of TestResults objects
        dataset_type (str, optional): The type of dataset. Can be one of "training",
          "test", or "validation". Defaults to "training".

    Raises:
        Exception: If the API call fails

    Returns:
        list: list of responses from the API
    """
    try:
        return run_async(
            asyncio.gather(
                *[log_test_result(result, dataset_type) for result in results]
            )
        )
    except Exception as e:
        print("Error logging test results to ValidMind API")
        raise e


def start_run():
    """Starts a new test run.

    This method will return a test run CUID that needs to be
    passed to any functions logging test results to the ValidMind API.
    """
    global _run_cuid

    r = requests.post(
        f"{_api_host}/start_run",
        headers={
            "X-API-KEY": _api_key,
            "X-API-SECRET": _api_secret,
            "X-PROJECT-CUID": _project,
        },
    )

    if r.status_code != 200:
        print("Could not start data logging run with ValidMind API")
        raise Exception(r.text)

    test_run = r.json()
    # api_session.headers["X-RUN-CUID"] = test_run["cuid"]
    _run_cuid = test_run["cuid"]

    return test_run["cuid"]
