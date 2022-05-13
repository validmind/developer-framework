"""
API Client
"""
import os

import requests

from .model import Model, ModelAttributes
from .model_utils import get_info_from_model_instance, get_params_from_model_instance


API_HOST = os.environ.get("API_HOST", "http://127.0.0.1:5000/api/v1/tracking")
ENV_API_KEY = os.environ.get("VM_API_KEY")
ENV_API_SECRET = os.environ.get("VM_API_SECRET")

vm_api_key = None
vm_api_secret = None

api_session = requests.Session()


def __ping():
    r = api_session.get(f"{API_HOST}/ping")
    assert r.status_code == 200
    return True


def init(project, api_key=None, api_secret=None):
    """
    Initializes the API client instances and /pings the API
    to ensure the provided credentials are valid.
    """
    vm_api_key = api_key or ENV_API_KEY
    vm_api_secret = api_secret or ENV_API_SECRET

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


def log_model(model_instance, vm_model=None):
    if vm_model is None:
        vm_model = Model(
            attributes=ModelAttributes(),
        )

    model_info = get_info_from_model_instance(model_instance)

    if vm_model.task is None:
        vm_model.task = model_info["task"]
    if vm_model.subtask is None:
        vm_model.subtask = model_info["subtask"]
    if vm_model.attributes.framework is None:
        vm_model.attributes.framework = model_info["framework"]
    if vm_model.attributes.framework_version is None:
        vm_model.attributes.framework_version = model_info["framework_version"]
    if vm_model.attributes.architecture is None:
        vm_model.attributes.architecture = model_info["architecture"]

    vm_model.params = get_params_from_model_instance(model_instance)

    r = api_session.post(f"{API_HOST}/log_model", json=vm_model.serialize())
    assert r.status_code == 200

    return True
