import json
import os
import urllib.parse
from io import BytesIO

import aiohttp

from .utils import NumpyEncoder
from .utils import get_full_typename, is_matplotlib_typename


class APIClient:
    def __init__(self, project=None, api_key=None, api_secret=None, api_host=None):
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
        self.api_key = api_key or os.environ.get("VM_API_KEY")
        self.api_secret = api_secret or os.environ.get("VM_API_SECRET")
        self.api_host = api_host or os.environ.get(
            "VM_API_HOST", "http://127.0.0.1:5000/api/v1/tracking"
        )

        if self.vm_api_key is None or self.vm_api_secret is None:
            raise ValueError(
                "API key and secret must be provided either as environment variables or as arguments to init."
            )

        self.project = project or os.environ.get("VM_API_PROJECT")

        self.api_session = aiohttp.ClientSession()
        self.api_session.headers.update(
            {
                "X-API-KEY": self.api_key,
                "X-API-SECRET": self.api_secret,
                "X-PROJECT-CUID": project,
            }
        )

        return self.__ping()

    async def __ping(self):
        async with self.api_session.get(f"{self.API_HOST}/ping") as r:
            if r.status != 200:
                print("Unsuccessful ping to ValidMind API")
                raise Exception(await r.text())

            project_info = await r.json()

            if "name" in project_info:
                print(
                    f"Connected to ValidMind. Project: {project_info['name']} ({project_info['cuid']})"
                )
            else:
                print("Connected to ValidMind")

    async def __get_url(self, endpoint, params=None):
        if not self.run_cuid:
            self.start_run()

        params = params or {}
        params["run_cuid"] = self.run_cuid

        return f"{self.API_HOST}/{endpoint}?{urllib.parse.urlencode(params)}"

    async def _get(self, endpoint, params=None):
        async with self.api_session.get(self.__get_url(endpoint, params)) as r:
            if r.status != 200:
                raise Exception(await r.text())

            return await r.json()

    async def _post(self, endpoint, params=None, data=None, files=None):
        async with self.api_session.post(
            self.__get_url(endpoint, params), data=data, files=files
        ) as r:
            if r.status != 200:
                raise Exception(await r.text())

            return await r.json()

    async def start_run(self):
        """Starts a new test run.

        This method will return a test run CUID that needs to be
        passed to any functions logging test results to the ValidMind API.
        """
        try:
            res_json = await self._post("start_run")
        except Exception as e:
            print("Could not start data logging run with ValidMind API")
            raise e

        self.run_cuid = res_json["run_cuid"]

    async def get_metadata(self, content_id):
        """Gets a metadata object from ValidMind API.

        Args:
            content_id (str): Unique content identifier for the metadata

        Raises:
            Exception: If the API call fails

        Returns:
            bool: Metadata object
        """
        try:
            return await self._get(f"get_metadata/{content_id}")
        except Exception as e:
            print("Could not retrieve metadata from ValidMind API")
            raise e

    async def log_dataset(self, vm_dataset):
        """Logs metadata and statistics about a dataset to ValidMind API.

        Args:
            vm_dataset (validmind.VMDataset): A VM dataset object

        Returns:
            validmind.VMDataset: The VMDataset object
        """
        try:
            await self._post(
                "log_dataset",
                data=json.dumps(
                    vm_dataset.serialize(), cls=NumpyEncoder, allow_nan=False
                ),
            )
        except Exception as e:
            print("Error logging dataset to ValidMind API")
            raise e

        return vm_dataset

    async def log_figure(self, data_or_path, key, metadata):
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
            return await self._post(
                "log_figure",
                data={"type": type_, "key": key, "metadata": metadata_json},
                files=files,
            )
        except Exception as e:
            print("Error logging figure to ValidMind API")
            raise e

    async def _log_metadata(self, content_id, text=None, extra_json=None):
        """Logs free-form metadata to ValidMind API. (not intended to be a public method)

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
            return await self._post(
                "log_metadata",
                data=json.dumps(metadata_dict, cls=NumpyEncoder, allow_nan=False),
            )
        except Exception as e:
            print("Error logging metadata to ValidMind API")
            raise e

    async def log_metrics(self, metrics):
        """Logs metrics to ValidMind API.

        Args:
            metrics (list): A list of Metric objects

        Raises:
            Exception: If the API call fails

        Returns:
            dict: The response from the API
        """
        try:
            return await self._post(
                "log_metrics",
                data=json.dumps(
                    [m.serialize() for m in metrics], cls=NumpyEncoder, allow_nan=False
                ),
            )
        except Exception as e:
            print("Error logging metrics to ValidMind API")
            raise e

    async def log_model(self, vm_model):
        """Logs model metadata and hyperparameters to ValidMind API.

        Args:
            vm_model (validmind.VMModel): A VM model object

        Raises:
            Exception: If the API call fails

        Returns:
            dict: The response from the API
        """
        try:
            return await self._post(
                "log_model",
                data=json.dumps(
                    vm_model.serialize(), cls=NumpyEncoder, allow_nan=False
                ),
            )
        except Exception as e:
            print("Error logging model to ValidMind API")
            raise e

    async def log_test_result(self, result, dataset_type="training"):
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
            return await self._post(
                "log_test_results",
                params={"dataset_type": dataset_type},
                data=json.dumps(result.serialize(), cls=NumpyEncoder, allow_nan=False),
            )
        except Exception as e:
            print("Error logging test results to ValidMind API")
            raise e
