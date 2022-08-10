"""
API Client
"""
import json
import math
import os
from io import BytesIO

import numpy as np
import requests

from .dataset_utils import analyze_vm_dataset, init_vm_dataset
from .model import Model, ModelAttributes
from .model_utils import (
    get_info_from_model_instance,
    get_params_from_model_instance,
    get_training_metrics,
)
from .type_utils import get_full_typename, is_matplotlib_typename

API_HOST = os.environ.get("VM_API_HOST", "http://127.0.0.1:5000/api/v1/tracking")
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


def log_dataset(
    dataset,
    dataset_type,
    dataset_options=None,
    analyze=True,
    targets=None,
    features=None,
):
    """
    Logs metadata and statistics about a dataset to ValidMind API.

    :param dataset: A dataset. Only supports Pandas datasets at the moment.
    :param dataset_type: The type of dataset. Can be one of "training", "test", or "validation".
    :param dataset_options: Additional dataset options for analysis
    :param dataset_targets: A list of targets for the dataset.
    :param features: Optional. A list of features metadata.
    :type dataset_targets: validmind.DatasetTargets, optional
    """
    vm_dataset = init_vm_dataset(
        dataset, dataset_type, dataset_options, targets, features
    )
    analyze_results = None

    if analyze:
        analyze_results = analyze_vm_dataset(dataset, vm_dataset)
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

    if analyze_results:
        for corr_plot in analyze_results["correlations_plots"]["pearson"]:
            log_figure(corr_plot["figure"], corr_plot["key"], corr_plot["metadata"])

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


def log_training_metrics(model, x_train, y_train, run_cuid=None):
    """
    Logs training metrics to ValidMind API.

    :param model: A model instance. Only supports XGBoost at the moment.
    :param x_train: The training dataset.
    :param y_train: The training dataset targets.
    """
    if run_cuid is None:
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


def log_evaluation_metrics(metrics, run_cuid):
    """
    Logs evaluation metrics to ValidMind API.

    :param model: A model instance. Only supports XGBoost at the moment.
    :param x_train: The training dataset.
    :param y_train: The training dataset targets.
    """
    r = api_session.post(
        f"{API_HOST}/log_metrics?run_cuid={run_cuid}",
        data=json.dumps(metrics, cls=NumpyEncoder),
        headers={"Content-Type": "application/json"},
    )

    if r.status_code != 200:
        print("Could not log evaluation metrics to ValidMind API")
        raise Exception(r.text)

    print("Successfully logged evaluation metrics")

    return True


def log_test_results(results, run_cuid, dataset_type):
    """
    Logs test results information. This method will be called automatically be any function
    running tests but can also be called directly if the user wants to run tests on their own.

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
        data_or_path.savefig(buffer)
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
