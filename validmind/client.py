"""
API Client
"""
import json
import math
import os

import numpy as np
import requests

from .dataset_utils import analyze_vm_dataset, init_vm_dataset
from .model import Model, ModelAttributes
from .model_utils import (
    get_info_from_model_instance,
    get_params_from_model_instance,
    get_training_metrics,
)

API_HOST = os.environ.get("API_HOST", "http://127.0.0.1:5000/api/v1/tracking")
VALID_DATASET_TYPES = ["training", "test", "validation"]

vm_api_key = None
vm_api_secret = None

api_session = requests.Session()


def nan_to_none(obj):
    if isinstance(obj, dict):
        return {k: nan_to_none(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [nan_to_none(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

    def encode(self, obj):
        obj = nan_to_none(obj)
        return super().encode(obj)

    def iterencode(self, obj, _one_shot: bool = ...):
        obj = nan_to_none(obj)
        return super().iterencode(obj, _one_shot)


def __ping():
    r = api_session.get(f"{API_HOST}/ping")

    if r.status_code != 200:
        print("Unsuccessful ping to ValidMind API")
        raise Exception(r.text)

    return True


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


def log_dataset(
    dataset,
    dataset_type,
    analyze=False,
    analyze_opts=None,
    targets=None,
):
    """
    Logs metadata and statistics about a dataset to ValidMind API.

    :param dataset: A dataset. Only supports Pandas datasets at the moment.
    :param dataset_type: The type of dataset. Can be one of "training", "test", or "validation".
    :param dataset_targets: A list of targets for the dataset.
    :type dataset_targets: validmind.DatasetTargets, optional
    """
    vm_dataset = init_vm_dataset(dataset, dataset_type, targets)

    if analyze:
        analyze_results = analyze_vm_dataset(dataset, vm_dataset.fields, analyze_opts)
        if "statistics" in analyze_results:
            vm_dataset.statistics = analyze_results["statistics"]
        if "correlations" in analyze_results:
            vm_dataset.correlations = analyze_results["correlations"]

    payload = json.dumps(vm_dataset.serialize(), cls=NumpyEncoder)
    r = api_session.post(
        f"{API_HOST}/log_dataset",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    if r.status_code != 200:
        print("Could not log dataset to ValidMind API")
        raise Exception(r.text)

    return True


def log_model(model_instance, vm_model=None):
    """
    Logs model metadata and hyperparameters to ValidMind API.

    :param model_instance: A model instance. Only supports XGBoost at the moment.
    :param vm_model: A ValidMind Model wrapper instance.
    :type vm_model: validmind.Model, optional
    """
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

    r = api_session.post(
        f"{API_HOST}/log_model",
        data=json.dumps(vm_model.serialize(), cls=NumpyEncoder),
        headers={"Content-Type": "application/json"},
    )

    if r.status_code != 200:
        print("Could not log model to ValidMind API")
        raise Exception(r.text)

    return True


def log_training_metrics(model, x_train, y_train):
    """
    Logs training metrics to ValidMind API.

    :param model: A model instance. Only supports XGBoost at the moment.
    :param x_train: The training dataset.
    :param y_train: The training dataset targets.
    """
    run_cuid = start_run()
    training_metrics = get_training_metrics(model, x_train, y_train)

    r = api_session.post(
        f"{API_HOST}/log_metrics?run_cuid={run_cuid}",
        data=json.dumps(training_metrics, cls=NumpyEncoder),
        headers={"Content-Type": "application/json"},
    )

    if r.status_code != 200:
        print("Could not log training metrics to ValidMind API")
        raise Exception(r.text)

    print("Successfully logged training metrics")

    return True


def log_test_results(results, run_cuid, dataset_type):
    """
    Logs test results information. This method will be called automatically be run_tests
    but can also be called directly if the user wants to run tests on their own.

    :param results: A list of TestResults objects
    """
    # TBD - parallelize API requests
    for result in results:
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


def start_run():
    """
    Starts a new test run. This method will return a test run CUID that needs to be
    passed to any functions logging test results to the ValidMind API.
    """
    r = api_session.post(f"{API_HOST}/start_run")

    if r.status_code != 200:
        print("Could not stat data logging run with ValidMind API")
        raise Exception(r.text)

    test_run = r.json()
    return test_run["cuid"]
