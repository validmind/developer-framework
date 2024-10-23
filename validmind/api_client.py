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
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlencode, urljoin

import aiohttp
import requests
from aiohttp import FormData

from .client_config import client_config
from .errors import MissingAPICredentialsError, MissingModelIdError, raise_api_error
from .logging import get_logger, init_sentry, send_single_error
from .utils import NumpyEncoder, run_async
from .vm_models import Figure, MetricResult, ThresholdTestResults

# TODO: can't import types from vm_models because of circular dependency

logger = get_logger(__name__)

_api_key = os.getenv("VM_API_KEY")
_api_secret = os.getenv("VM_API_SECRET")
_api_host = os.getenv("VM_API_HOST")
_model_cuid = os.getenv("VM_API_MODEL")
_monitoring = False

__api_session: Optional[aiohttp.ClientSession] = None


@atexit.register
def _close_session():
    """Closes the async client session at exit"""
    global __api_session

    if __api_session and not __api_session.closed:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(__api_session.close())
            else:
                loop.run_until_complete(__api_session.close())
        except Exception as e:
            logger.exception("Error closing aiohttp session at exit: %s", e)


def get_api_host() -> Optional[str]:
    return _api_host


def get_api_model() -> Optional[str]:
    return _model_cuid


def _get_api_headers() -> Dict[str, str]:
    return {
        "X-API-KEY": _api_key,
        "X-API-SECRET": _api_secret,
        "X-MODEL-CUID": _model_cuid,
        "X-MONITORING": str(_monitoring),
    }


def _get_session() -> aiohttp.ClientSession:
    """Initializes the async client session"""
    global __api_session

    if not __api_session or __api_session.closed:
        __api_session = aiohttp.ClientSession(
            headers=_get_api_headers(),
            timeout=aiohttp.ClientTimeout(total=600),
            connector=aiohttp.TCPConnector(force_close=True),
        )

    return __api_session


def _get_url(
    endpoint: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    global _api_host

    params = params or {}

    if not _api_host.endswith("/"):
        _api_host += "/"

    if params:
        return f"{urljoin(_api_host, endpoint)}?{urlencode(params)}"

    return urljoin(_api_host, endpoint)


async def _get(
    endpoint: str, params: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    url = _get_url(endpoint, params)
    session = _get_session()

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
    url = _get_url(endpoint, params)
    session = _get_session()

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


def _ping() -> Dict[str, Any]:
    """Validates that we can connect to the ValidMind API (does not use the async session)"""
    r = requests.get(
        url=_get_url("ping"),
        headers=_get_api_headers(),
    )
    if r.status_code != 200:
        raise_api_error(r.text)

    client_info = r.json()

    init_sentry(client_info.get("sentry_config", {}))

    # Only show this confirmation the first time we connect to the API
    ack_connected = not client_config.model

    client_config.documentation_template = client_info.get("documentation_template", {})
    client_config.feature_flags = client_info.get("feature_flags", {})
    client_config.model = client_info.get("model", {})
    client_config.document_type = client_info.get(
        "document_type", "model_documentation"
    )

    if ack_connected:
        logger.info(
            f"🎉 Connected to ValidMind!\n"
            f"📊 Model: {client_config.model.get('name', 'N/A')} "
            f"(ID: {client_config.model.get('cuid', 'N/A')})\n"
            f"📁 Document Type: {client_config.document_type}"
        )


def init(
    project: Optional[str] = None,
    api_key: Optional[str] = None,
    api_secret: Optional[str] = None,
    api_host: Optional[str] = None,
    model: Optional[str] = None,
    monitoring=False,
):
    """
    Initializes the API client instances and calls the /ping endpoint to ensure
    the provided credentials are valid and we can connect to the ValidMind API.

    If the API key and secret are not provided, the client will attempt to
    retrieve them from the environment variables `VM_API_KEY` and `VM_API_SECRET`.

    Args:
        project (str, optional): The project CUID. Alias for model. Defaults to None. [DEPRECATED]
        model (str, optional): The model CUID. Defaults to None.
        api_key (str, optional): The API key. Defaults to None.
        api_secret (str, optional): The API secret. Defaults to None.
        api_host (str, optional): The API host. Defaults to None.
        monitoring (str, optional): The ongoing monitoring flag. Defaults to False.

    Raises:
        ValueError: If the API key and secret are not provided
    """
    global _api_key, _api_secret, _api_host, _model_cuid, _monitoring

    if api_key == "...":
        # special case to detect when running a notebook placeholder (...)
        # will override with environment variables for easier local development
        api_host = api_key = api_secret = project = None

    _model_cuid = project or model or os.getenv("VM_API_MODEL")
    if _model_cuid is None:
        raise MissingModelIdError()

    _api_key = api_key or os.getenv("VM_API_KEY")
    _api_secret = api_secret or os.getenv("VM_API_SECRET")
    if _api_key is None or _api_secret is None:
        raise MissingAPICredentialsError()

    _api_host = api_host or os.getenv(
        "VM_API_HOST", "http://localhost:5000/api/v1/tracking/"
    )

    _monitoring = monitoring

    reload()


def reload():
    """Reconnect to the ValidMind API and reload the project configuration"""

    try:
        _ping()
    except Exception as e:
        # if the api host is https, assume we're not in dev mode and send to sentry
        if _api_host.startswith("https://"):
            send_single_error(e)
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


async def log_metric_result(
    metric: MetricResult,
    inputs: List[str],
    output_template: str = None,
    section_id: str = None,
    position: int = None,
) -> Dict[str, Any]:
    """Logs metrics to ValidMind API.

    Args:
        metric (MetricResult): A MetricResult object
        inputs (list): A list of input keys (names) that were used to run the test
        output_template (str): The optional output template for the test
        section_id (str): The section ID add a test driven block to the documentation
        position (int): The position in the section to add the test driven block

    Raises:
        Exception: If the API call fails

    Returns:
        dict: The response from the API
    """
    request_params = {}
    if section_id:
        request_params["section_id"] = section_id
    if position is not None:
        request_params["position"] = position

    metric_data = {
        **metric.serialize(),
        "inputs": inputs,
    }
    if output_template:
        metric_data["output_template"] = output_template

    try:
        return await _post(
            "log_metrics",
            params=request_params,
            data=json.dumps([metric_data], cls=NumpyEncoder, allow_nan=False),
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
    request_params = {}
    if section_id:
        request_params["section_id"] = section_id
    if position is not None:
        request_params["position"] = position

    try:
        return await _post(
            "log_test_results",
            params=request_params,
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


def log_input(input_id: str, type: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Logs input information - internal use for now (don't expose via public API)

    Args:
        input_id (str): The input_id of the input
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
                    "name": input_id,
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


async def alog_metric(
    key: str,
    value: float,
    inputs: Optional[List[str]] = None,
    params: Optional[Dict[str, Any]] = None,
    recorded_at: Optional[str] = None,
):
    """See log_metric for details"""
    if not key or not isinstance(key, str):
        raise ValueError("`key` must be a non-empty string")

    if not value or not isinstance(value, (int, float)):
        raise ValueError("`value` must be a scalar (int or float)")

    try:
        return await _post(
            "log_unit_metric",
            data=json.dumps(
                {
                    "key": key,
                    "value": value,
                    "inputs": inputs or [],
                    "params": params or {},
                    "recorded_at": recorded_at,
                },
                cls=NumpyEncoder,
                allow_nan=False,
            ),
        )
    except Exception as e:
        logger.error("Error logging metric to ValidMind API")
        raise e


def log_metric(
    key: str,
    value: float,
    inputs: Optional[List[str]] = None,
    params: Optional[Dict[str, Any]] = None,
    recorded_at: Optional[str] = None,
):
    """Logs a unit metric

    Unit metrics are key-value pairs where the key is the metric name and the value is
    a scalar (int or float). These key-value pairs are associated with the currently
    selected model (inventory model in the ValidMind Platform) and keys can be logged
    to over time to create a history of the metric. On the platform, these metrics
    will be used to create plots/visualizations for documentation and dashboards etc.

    Args:
        key (str): The metric key
        value (float): The metric value
        inputs (list, optional): A list of input IDs that were used to compute the metric.
        params (dict, optional): Dictionary of parameters used to compute the metric.
        recorded_at (str, optional): The timestamp of the metric. Server will use
            current time if not provided.
    """
    run_async(alog_metric, key, value, inputs, params, recorded_at)


def get_ai_key() -> Dict[str, Any]:
    """Calls the api to get an api key for our LLM proxy"""
    r = requests.get(
        url=_get_url("ai/key"),
        headers=_get_api_headers(),
    )

    if r.status_code != 200:
        # TODO: improve error handling when there's no Open AI API or AI key available
        # logger.error("Could not get AI key from ValidMind API")
        raise_api_error(r.text)

    return r.json()
