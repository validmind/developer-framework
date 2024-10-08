"""Test all of the public synchronous functions that call the async api client functions"""

import json
import os
import unittest
from unittest.mock import call, MagicMock, Mock, patch

import matplotlib.pyplot as plt
import pandas as pd
from aiohttp.formdata import FormData

# simluate environment variables being set
os.environ["VM_API_KEY"] = "your_api_key"
os.environ["VM_API_SECRET"] = "your_api_secret"
os.environ["VM_API_HOST"] = "your_api_host"
os.environ["VM_API_MODEL"] = "your_model"

import validmind as vm
from validmind.vm_models.figure import Figure
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
    def test_log_figure_matplot(self, mock_post: MagicMock):
        mock_response = MockResponse(200, json={"cuid": "1234"})
        mock_post.return_value = mock_response

        fig = plt.figure()
        plt.plot([1, 2, 3])
        figure = Figure(key="key", figure=fig, metadata={"asdf": 1234})
        vm.log_figure(figure)

        url = f"{os.environ['VM_API_HOST']}/log_figure"
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args[0][0], url)
        self.assertIsInstance(mock_post.call_args[1]["data"], FormData)

    @patch("aiohttp.ClientSession.post")
    def test_log_metrics(self, mock_post):
        metrics = [Mock(serialize=MagicMock(return_value={"key": "value"}))]

        mock_response = MockResponse(200, json={"cuid": "abc1234"})
        mock_post.return_value = mock_response

        vm.log_metrics(metrics, inputs=["input1"])

        url = f"{os.environ['VM_API_HOST']}/log_metrics"
        mock_post.assert_called_with(
            url, data=json.dumps([{"key": "value", "inputs": ["input1"]}])
        )

    @patch("validmind.api_client.log_test_result")
    def test_log_test_results(self, mock_log_test_result: MagicMock):
        results = [Mock(), Mock()]
        vm.log_test_results(results, inputs=["input1"])

        mock_log_test_result.assert_has_calls(
            [
                call(results[0], ["input1"]),
                call(results[1], ["input1"]),
            ]
        )


if __name__ == "__main__":
    unittest.main()
