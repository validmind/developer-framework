# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""ValidMind API client

Note that this takes advantage of the fact that python modules are singletons to store and share
the configuration and session across the entire project regardless of where the client is imported.
"""
import asyncio
import atexit
import json
import os
from io import BytesIO
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from urllib.parse import urlencode, urljoin

import aiohttp
import requests
from aiohttp import FormData

from .client_config import client_config
from .errors import MissingAPICredentialsError, MissingProjectIdError, raise_api_error
from .logging import get_logger, init_sentry, send_single_error
from .utils import NumpyEncoder, run_async
from .vm_models import Figure, MetricResult, ThresholdTestResults

# TODO: can't import types from vm_models because of circular dependency

logger = get_logger(__name__)

_api_key = os.getenv("VM_API_KEY")
_api_secret = os.getenv("VM_API_SECRET")
_api_host = os.getenv("VM_API_HOST")

_project = os.getenv("VM_API_PROJECT")
_run_cuid = os.getenv("VM_RUN_CUID")

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


def get_api_headers() -> Dict[str, str]:
    return {
        "X-API-KEY": _api_key,
        "X-API-SECRET": _api_secret,
        "X-PROJECT-CUID": _project,
    }


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

    if api_key == "...":
        # special case to detect when running a notebook with the standard init snippet
        # will override with environment variables so we don't have to keep updating
        # the notebook
        api_host = api_key = api_secret = project = None

    _project = project or os.getenv("VM_API_PROJECT")

    if _project is None:
        raise MissingProjectIdError()

    _api_key = api_key or os.getenv("VM_API_KEY")
    _api_secret = api_secret or os.getenv("VM_API_SECRET")

    if _api_key is None or _api_secret is None:
        raise MissingAPICredentialsError()

    _api_host = api_host or os.getenv(
        "VM_API_HOST", "http://127.0.0.1:5000/api/v1/tracking/"
    )

    _run_cuid = os.getenv("VM_RUN_CUID", None)

    try:
        __ping()
    except Exception as e:
        # if the api host is https, assume we're not in dev mode and send to sentry
        if _api_host.startswith("https://"):
            send_single_error(e)
        raise e


def _get_session() -> aiohttp.ClientSession:
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
        __get_url("ping", should_start_run=False),
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

    # Only show this confirmation the first time we connect to the API
    ack_connected = False
    if client_config.project is None:
        ack_connected = True

    client_config.project = client_info["project"]
    client_config.documentation_template = client_info.get("documentation_template", {})
    client_config.feature_flags = client_info.get("feature_flags", {})

    if ack_connected:
        logger.info(
            f"Connected to ValidMind. Project: {client_config.project['name']}"
            f" ({client_config.project['cuid']})"
        )


def reload():
    """Reconnect to the ValidMind API and reload the project configuration"""

    try:
        __ping()
    except Exception as e:
        # if the api host is https, assume we're not in dev mode and send to sentry
        if _api_host.startswith("https://"):
            send_single_error(e)
        raise e


def __get_url(
    endpoint: str,
    params: Optional[Dict[str, str]] = None,
    should_start_run: bool = True,
) -> str:
    global _api_host

    params = params or {}

    if not _run_cuid and should_start_run:
        start_run()

    if should_start_run:
        params["run_cuid"] = _run_cuid

    if not _api_host.endswith("/"):
        _api_host += "/"

    if params:
        return f"{urljoin(_api_host, endpoint)}?{urlencode(params)}"

    return urljoin(_api_host, endpoint)


async def _get(
    endpoint: str, params: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    url = __get_url(endpoint, params)
    session = _get_session()
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
    url = __get_url(endpoint, params)
    session = _get_session()
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
    # this actually slows things down - better to log them in parallel
    # if client_config.can_log_figures():  # check if the backend supports batch logging
    #     try:
    #         data = {}
    #         files = {}
    #         for figure in figures:
    #             data.update(
    #                 {f"{k}-{figure.key}": v for k, v in figure.serialize().items()}
    #             )
    #             files.update(
    #                 {
    #                     f"{k}-{figure.key}": v
    #                     for k, v in figure.serialize_files().items()
    #                 }
    #             )

    #         return await _post(
    #             "log_figures",
    #             data=data,
    #             files=files,
    #         )
    #     except Exception as e:
    #         logger.error("Error logging figures to ValidMind API")
    #         raise e

    # else:
    return await asyncio.gather(*[log_figure(figure) for figure in figures])


async def log_metadata(
    content_id: str,
    text: Optional[str] = None,
    _json: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Logs free-form metadata to ValidMind API.

    Args:
        content_id (str): Unique content identifier for the metadata
        text (str, optional): Free-form text to assign to the metadata. Defaults to None.
        _json (dict, optional): Free-form key-value pairs to assign to the metadata. Defaults to None.

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    metadata_dict = {"content_id": content_id}
    if text is not None:
        metadata_dict["text"] = text
    if _json is not None:
        metadata_dict["json"] = _json

    try:
        return await _post(
            "log_metadata",
            data=json.dumps(metadata_dict, cls=NumpyEncoder, allow_nan=False),
        )
    except Exception as e:
        logger.error("Error logging metadata to ValidMind API")
        raise e


async def log_metrics(
    metrics: List[MetricResult],
    inputs: List[str],
    output_template: str = None,
    section_id: str = None,
    position: int = None,
) -> Dict[str, Any]:
    """Logs metrics to ValidMind API.

    Args:
        metrics (list): A list of MetricResult objects
        inputs (list): A list of input keys (names) that were used to run the test
        output_template (str): The optional output template for the test
        section_id (str): The section ID add a test driven block to the documentation
        position (int): The position in the section to add the test driven block

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    params = {}
    if section_id:
        params["section_id"] = section_id
    if position is not None:
        params["position"] = position

    data = []

    for metric in metrics:
        metric_data = {
            **metric.serialize(),
            "inputs": inputs,
        }

        if output_template and client_config.can_log_output_template():
            metric_data["output_template"] = output_template

        data.append(metric_data)

    try:
        return await _post(
            "log_metrics",
            params=params,
            data=json.dumps(data, cls=NumpyEncoder, allow_nan=False),
        )
    except Exception as e:
        logger.error("Error logging metrics to ValidMind API")
        raise e


async def log_test_result(
    result: ThresholdTestResults,
    inputs: List[str],
    section_id: str = None,
    position: int = None,
) -> Dict[str, Any]:
    """Logs test results information

    This method will be called automatically from any function running tests but
    can also be called directly if the user wants to run tests on their own.

    Args:
        result (validmind.ThresholdTestResults): A ThresholdTestResults object
        inputs (list): A list of input keys (names) that were used to run the test
        section_id (str, optional): The section ID add a test driven block to the documentation
        position (int): The position in the section to add the test driven block

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    params = {}
    if section_id:
        params["section_id"] = section_id
    if position is not None:
        params["position"] = position

    try:
        return await _post(
            "log_test_results",
            params=params,
            data=json.dumps(
                {
                    **result.serialize(),
                    "inputs": inputs,
                },
                cls=NumpyEncoder,
                allow_nan=False,
            ),
        )
    except Exception as e:
        logger.error("Error logging test results to ValidMind API")
        raise e


def log_test_results(
    results: List[ThresholdTestResults], inputs
) -> List[Callable[..., Dict[str, Any]]]:
    """Logs test results information

    This method will be called automatically be any function
    running tests but can also be called directly if the user wants to run tests on their own.

    Args:
        results (list): A list of ThresholdTestResults objects
        inputs (list): A list of input keys (names) that were used to run the test

    Raises:
        Exception: If the API call fails

    Returns:
        list: list of responses from the API
    """
    try:
        responses = []  # TODO: use asyncio.gather
        for result in results:
            responses.append(run_async(log_test_result, result, inputs))
    except Exception as e:
        logger.error("Error logging test results to ValidMind API")
        raise e

    return responses


def log_input(name: str, type: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Logs input information - internal use for now (don't expose via public API)

    Args:
        name (str): The name of the input
        type (str): The type of the input
        metadata (dict): The metadata of the input

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    try:
        return run_async(
            _post,
            "log_input",
            data=json.dumps(
                {
                    "name": name,
                    "type": type,
                    "metadata": metadata,
                },
                cls=NumpyEncoder,
                allow_nan=False,
            ),
        )
    except Exception as e:
        logger.error("Error logging input to ValidMind API")
        raise e


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
        __get_url("start_run", should_start_run=False),
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


def get_ai_key() -> str:
    """Calls the api to get an api key for our LLM proxy"""
    r = requests.get(
        __get_url("ai/key", should_start_run=False),
        headers={
            "X-API-KEY": _api_key,
            "X-API-SECRET": _api_secret,
            "X-PROJECT-CUID": _project,
        },
    )

    if r.status_code != 200:
        # TODO: improve error handling when there's no Open AI API or AI key available
        # logger.error("Could not get AI key from ValidMind API")
        raise_api_error(r.text)

    return r.json()
