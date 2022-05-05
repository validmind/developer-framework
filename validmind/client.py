"""
API Client
"""
import os

import requests


API_HOST = os.environ.get("API_HOST", "http://127.0.0.1:5000/api/v1/tracking")
ENV_API_KEY = os.environ.get("VM_API_KEY")
ENV_API_SECRET = os.environ.get("VM_API_SECRET")

vm_api_key = None
vm_api_secret = None

api_session = requests.Session()

def _ping():
    r = api_session.get(f"{API_HOST}/ping")
    return r.json()


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

    api_session.headers.update({
        "X-API-KEY": vm_api_key,
        "X-API-SECRET": vm_api_secret,
        "X-PROJECT-CUID": project,
    })

    return _ping()
