# Copyright © 2023 ValidMind Inc. All rights reserved.

"""ValidMind API client

Note that this takes advantage of the fact that python modules are singletons to store and share
the configuration and session across the entire project regardless of where the client is imported.
"""
import asyncio
import atexit
import json
import os
import urllib.parse
from io import BytesIO
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import aiohttp
import requests
from aiohttp import FormData

from .client_config import client_config
from .errors import MissingAPICredentialsError, MissingProjectIdError, raise_api_error
from .logging import get_logger, init_sentry, send_single_error
from .utils import NumpyEncoder, run_async
from .vm_models import Figure, Metric, ThresholdTestResults, VMDataset

# TODO: can't import types from vm_models because of circular dependency

logger = get_logger(__name__)

_api_key = os.environ.get("VM_API_KEY")
_api_secret = os.environ.get("VM_API_SECRET")
_api_host = os.environ.get("VM_API_HOST")

_project = os.environ.get("VM_API_PROJECT")
_run_cuid = os.environ.get("VM_RUN_CUID")

__api_session: aiohttp.ClientSession = None


@atexit.register
def _close_session():
    """Closes the async client session"""
    global __api_session

    if __api_session is not None:
        try:
            asyncio.run(__api_session.close())
        except Exception:
            pass


def get_api_config() -> Dict[str, Optional[str]]:
    return {
        "VM_API_KEY": _api_key,
        "VM_API_SECRET": _api_secret,
        "VM_API_HOST": _api_host,
        "VM_API_PROJECT": _project,
        "VM_RUN_CUID": _run_cuid,
    }


def get_api_host() -> Optional[str]:
    return _api_host


def get_api_project() -> Optional[str]:
    return _project


def init(
    project: Optional[str] = None,
    api_key: Optional[str] = None,
    api_secret: Optional[str] = None,
    api_host: Optional[str] = None,
):
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
    """
    global _api_key, _api_secret, _api_host, _run_cuid, _project

    if api_host == "...":
        # special case to detect when running a notebook with the standard init snippet
        # will override with environment variables so we don't have to keep updating
        # the notebook
        api_host = None
        api_key = None
        api_secret = None
        project = None

    _project = project or os.environ.get("VM_API_PROJECT")

    if _project is None:
        raise MissingProjectIdError()

    _api_key = api_key or os.environ.get("VM_API_KEY")
    _api_secret = api_secret or os.environ.get("VM_API_SECRET")

    if _api_key is None or _api_secret is None:
        raise MissingAPICredentialsError()

    _api_host = api_host or os.environ.get(
        "VM_API_HOST", "http://127.0.0.1:5000/api/v1/tracking"
    )
    _run_cuid = os.environ.get("VM_RUN_CUID", None)

    try:
        __ping()
    except Exception as e:
        # if the api host is https, assume we're not in dev mode and send to sentry
        if _api_host.startswith("https://"):
            send_single_error(e)
        raise e


async def _get_session() -> aiohttp.ClientSession:
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


def __ping() -> Dict[str, Any]:
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
        raise_api_error(r.text)

    client_info = r.json()

    init_sentry(client_info.get("sentry_config", {}))

    client_config.project = client_info["project"]
    client_config.documentation_template = client_info.get("documentation_template", {})
    client_config.feature_flags = client_info.get("feature_flags", {})

    logger.info(
        f"Connected to ValidMind. Project: {client_config.project['name']}"
        f" ({client_config.project['cuid']})"
    )


async def __get_url(endpoint: str, params: Optional[Dict[str, str]] = None) -> str:
    if not _run_cuid:
        start_run()

    params = params or {}
    params["run_cuid"] = _run_cuid

    return f"{_api_host}/{endpoint}?{urllib.parse.urlencode(params)}"


async def _get(
    endpoint: str, params: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    url = await __get_url(endpoint, params)
    session = await _get_session()
    session.headers.update({"X-RUN-CUID": _run_cuid})

    async with session.get(url) as r:
        if r.status != 200:
            raise_api_error(await r.text())

        return await r.json()


async def _post(
    endpoint: str,
    params: Optional[Dict[str, str]] = None,
    data: Optional[Union[dict, FormData]] = None,
    files: Optional[Dict[str, Tuple[str, BytesIO, str]]] = None,
) -> Dict[str, Any]:
    url = await __get_url(endpoint, params)
    session = await _get_session()
    session.headers.update({"X-RUN-CUID": _run_cuid})

    if not isinstance(data, (dict)) and files is not None:
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
            raise_api_error(await r.text())

        return await r.json()


async def get_metadata(content_id: str) -> Dict[str, Any]:
    """Gets a metadata object from ValidMind API.

    Args:
        content_id (str): Unique content identifier for the metadata

    Raises:
        Exception: If the API call fails

    Returns:
        dict: Metadata object
    """
    # TODO: add a more accurate type hint/documentation
    return await _get(f"get_metadata/{content_id}")


async def log_dataset(vm_dataset: VMDataset) -> Dict[str, Any]:
    """Logs metadata and statistics about a dataset to ValidMind API.

    Args:
        vm_dataset (validmind.VMDataset): A VM dataset object

    Returns:
        dict: The response from the API
    """
    try:
        return await _post(
            "log_dataset",
            data=json.dumps(vm_dataset.serialize(), cls=NumpyEncoder, allow_nan=False),
        )
    except Exception as e:
        logger.error("Error logging dataset to ValidMind API")
        raise e


async def log_figure(figure: Figure) -> Dict[str, Any]:
    """Logs a figure

    Args:
        figure (Figure): The Figure object wrapper

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    try:
        return await _post(
            "log_figure",
            data=figure.serialize(),
            files=figure.serialize_files(),
        )
    except Exception as e:
        logger.error("Error logging figure to ValidMind API")
        raise e


async def log_figures(figures: List[Figure]) -> Dict[str, Any]:
    """Logs a list of figures

    Args:
        figures (list): A list of Figure objects

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    if client_config.can_log_figures():  # check if the backend supports batch logging
        try:
            data = {}
            files = {}
            for figure in figures:
                data.update(
                    {f"{k}-{figure.key}": v for k, v in figure.serialize().items()}
                )
                files.update(
                    {
                        f"{k}-{figure.key}": v
                        for k, v in figure.serialize_files().items()
                    }
                )

            return await _post(
                "log_figures",
                data=data,
                files=files,
            )
        except Exception as e:
            logger.error("Error logging figures to ValidMind API")
            raise e

    else:
        return await asyncio.gather(*[log_figure(figure) for figure in figures])


async def log_metadata(
    content_id: str,
    text: Optional[str] = None,
    extra_json: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
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
        logger.error("Error logging metadata to ValidMind API")
        raise e


async def log_metrics(metrics: List[Metric]) -> Dict[str, Any]:
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
        logger.error("Error logging metrics to ValidMind API")
        raise e


async def log_test_result(
    result: ThresholdTestResults, dataset_type: str = "training"
) -> Dict[str, Any]:
    """Logs test results information

    This method will be called automatically from any function running tests but
    can also be called directly if the user wants to run tests on their own.

    Args:
        result (validmind.ThresholdTestResults): A ThresholdTestResults object
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
        logger.error("Error logging test results to ValidMind API")
        raise e


def log_test_results(
    results: List[ThresholdTestResults], dataset_type: str = "training"
) -> List[Callable[..., Dict[str, Any]]]:
    """Logs test results information

    This method will be called automatically be any function
    running tests but can also be called directly if the user wants to run tests on their own.

    Args:
        results (list): A list of ThresholdTestResults objects
        dataset_type (str, optional): The type of dataset. Can be one of "training",
          "test", or "validation". Defaults to "training".

    Raises:
        Exception: If the API call fails

    Returns:
        list: list of responses from the API
    """
    try:
        responses = []  # TODO: use asyncio.gather
        for result in results:
            responses.append(run_async(log_test_result, result, dataset_type))
    except Exception as e:
        logger.error("Error logging test results to ValidMind API")
        raise e

    return responses


def start_run() -> str:
    """Starts a new test run

    This function will take care of updating the api client with the new run CUID
    and will be called automatically when logging starts if no run CUID is set.

    Raises:
        Exception: If the API call fails

    Returns:
        str: The test run CUID
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
        logger.error("Could not start data logging run with ValidMind API")
        raise_api_error(r.text)

    test_run = r.json()
    _run_cuid = test_run["cuid"]

    return test_run["cuid"]
