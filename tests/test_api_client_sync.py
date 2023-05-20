"""Test all of the public synchronous functions that call the async api client functions"""
import json
import os
import tempfile
import unittest
from unittest.mock import call, MagicMock, Mock, patch

import matplotlib.pyplot as plt
import pandas as pd
from aiohttp.formdata import FormData

# simluate environment variables being set
os.environ["VM_API_KEY"] = "your_api_key"
os.environ["VM_API_SECRET"] = "your_api_secret"
os.environ["VM_API_HOST"] = "your_api_host"
os.environ["VM_API_PROJECT"] = "your_project"
os.environ["VM_RUN_CUID"] = "your_run_cuid"

import validmind as vm
from validmind.utils import NumpyEncoder


class MockResponse:
    def __init__(self, status, text=None, json=None):
        self.status = status
        self._text = text
        self._json = json

    async def text(self):
        return self._text

    async def json(self):
        return self._json

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


class TestAPIClient(unittest.TestCase):
    @patch("aiohttp.ClientSession.post")
    def test_log_dataset(self, mock_post: MagicMock):
        dataset = vm.init_dataset(pd.DataFrame({"col1": [1, 2, 3]}))
        dataset_serial = json.dumps(
            dataset.serialize(), cls=NumpyEncoder, allow_nan=False
        )

        mock_response = MockResponse(200, json={"cuid": "1234"})
        mock_post.return_value = mock_response

        vm.log_dataset(dataset)

        url = f"{os.environ['VM_API_HOST']}/log_dataset?run_cuid={os.environ['VM_RUN_CUID']}"
        mock_post.assert_called_with(url, data=dataset_serial)

    @patch("aiohttp.ClientSession.post")
    def test_log_figure_path(self, mock_post: MagicMock):
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(b"asdf")
        f.close()

        mock_response = MockResponse(200, json={"cuid": "1234"})
        mock_post.return_value = mock_response

        vm.log_figure(f.name, "key", {"asdf": 1234})

        url = f"{os.environ['VM_API_HOST']}/log_figure?run_cuid={os.environ['VM_RUN_CUID']}"
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args[0][0], url)
        self.assertIsInstance(mock_post.call_args[1]["data"], FormData)

        os.remove(f.name)

    @patch("aiohttp.ClientSession.post")
    def test_log_figure_matplot(self, mock_post: MagicMock):
        mock_response = MockResponse(200, json={"cuid": "1234"})
        mock_post.return_value = mock_response

        fig = plt.figure()
        plt.plot([1, 2, 3])
        vm.log_figure(fig, "key", {"asdf": 1234})

        url = f"{os.environ['VM_API_HOST']}/log_figure?run_cuid={os.environ['VM_RUN_CUID']}"
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args[0][0], url)
        self.assertIsInstance(mock_post.call_args[1]["data"], FormData)

    @patch("aiohttp.ClientSession.post")
    def test_log_metrics(self, mock_post):
        metrics = [Mock(serialize=MagicMock(return_value={"key": "value"}))]

        mock_response = MockResponse(200, json={"cuid": "abc1234"})
        mock_post.return_value = mock_response

        vm.log_metrics(metrics)

        url = f"{os.environ['VM_API_HOST']}/log_metrics?run_cuid={os.environ['VM_RUN_CUID']}"
        mock_post.assert_called_with(url, data=json.dumps([{"key": "value"}]))

    @patch("validmind.api_client.log_test_result")
    def test_log_test_results(self, mock_log_test_result: MagicMock):
        results = [Mock(), Mock()]
        vm.log_test_results(results)

        mock_log_test_result.assert_has_calls([
            call(results[0], "training"),
            call(results[1], "training"),
        ])


if __name__ == "__main__":
    unittest.main()
