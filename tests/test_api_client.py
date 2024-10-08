import asyncio
import json
import os
import unittest
from unittest.mock import call, MagicMock, Mock, patch

import matplotlib.pyplot as plt
from aiohttp.formdata import FormData

# simluate environment variables being set
os.environ["VM_API_KEY"] = "your_api_key"
os.environ["VM_API_SECRET"] = "your_api_secret"
os.environ["VM_API_HOST"] = "your_api_host"
os.environ["VM_API_MODEL"] = "your_model"

import validmind.api_client as api_client
from validmind.errors import MissingAPICredentialsError, MissingProjectIdError
from validmind.utils import md_to_html
from validmind.vm_models.figure import Figure


loop = asyncio.new_event_loop()


def mock_figure():
    fig = plt.figure()
    plt.plot([1, 2, 3])
    return Figure(key="key", figure=fig, metadata={"asdf": 1234})


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
    def tearDownClass():
        loop.close()

    def run_async(self, func, *args, **kwargs):
        return loop.run_until_complete(func(*args, **kwargs))

    @patch("requests.get")
    def test_init_successful(self, mock_requests_get):
        mock_data = {
            "project": {"name": "test_project", "cuid": os.environ["VM_API_MODEL"]}
        }
        mock_response = Mock(status_code=200, json=Mock(return_value=mock_data))
        mock_requests_get.return_value = mock_response

        success = api_client.init()
        self.assertIsNone(success)

        mock_requests_get.assert_called_once_with(
            f"{os.environ['VM_API_HOST']}/ping",
            headers={
                "X-API-KEY": os.environ["VM_API_KEY"],
                "X-API-SECRET": os.environ["VM_API_SECRET"],
                "X-PROJECT-CUID": os.environ["VM_API_MODEL"],
                "X-MONITORING": "False",
            },
        )

    def test_get_api_config(self):
        config = api_client.get_api_config()
        self.assertEqual(config["VM_API_KEY"], "your_api_key")
        self.assertEqual(config["VM_API_SECRET"], "your_api_secret")
        self.assertEqual(config["VM_API_HOST"], "your_api_host")
        self.assertEqual(config["VM_API_MODEL"], "your_model")

    def test_get_api_host(self):
        host = api_client.get_api_host()
        self.assertEqual(host, "your_api_host")

    def test_get_api_model(self):
        project = api_client.get_api_model()
        self.assertEqual(project, "your_model")

    @patch("requests.get")
    def test_init_missing_project_id(self, mock_requests_get):
        mock_requests_get.return_value = Mock()

        project = os.environ.pop("VM_API_MODEL")
        with self.assertRaises(MissingProjectIdError):
            api_client.init(project=None)

        os.environ["VM_API_MODEL"] = project

        mock_requests_get.assert_not_called()

    @patch("requests.get")
    def test_init_missing_api_key_secret(self, mock_requests_get):
        mock_requests_get.return_value = Mock()

        api_key = os.environ.pop("VM_API_KEY")
        api_secret = os.environ.pop("VM_API_SECRET")

        with self.assertRaises(MissingAPICredentialsError):
            api_client.init(project="project_id", api_key=None, api_secret=None)

        os.environ["VM_API_KEY"] = api_key
        os.environ["VM_API_SECRET"] = api_secret

        mock_requests_get.assert_not_called()

    @patch("requests.get")
    def test_init_unsuccessful_ping(self, mock_requests_get):
        mock_response = Mock(status_code=500)
        mock_response.text = "Internal Server Error"
        mock_requests_get.return_value = mock_response

        with self.assertRaises(Exception) as cm:
            api_client.init()

        self.assertEqual(str(cm.exception), "Internal Server Error")

        mock_requests_get.assert_called_once_with(
            f"{os.environ['VM_API_HOST']}/ping",
            headers={
                "X-API-KEY": os.environ["VM_API_KEY"],
                "X-API-SECRET": os.environ["VM_API_SECRET"],
                "X-PROJECT-CUID": os.environ["VM_API_MODEL"],
                "X-MONITORING": "False",
            },
        )

    @patch("aiohttp.ClientSession.get")
    def test_get_metadata(self, mock_get: MagicMock):
        res_json = [{"cuid": "1234"}]
        mock_response = MockResponse(200, json=res_json)
        mock_get.return_value = mock_response

        response = self.run_async(api_client.get_metadata, "content_id")

        url = f"{os.environ['VM_API_HOST']}/get_metadata/content_id"
        url += f""
        mock_get.assert_called_with(url)

        self.assertEqual(response, res_json)

    @patch("aiohttp.ClientSession.post")
    def test_log_figure_matplot(self, mock_post: MagicMock):
        mock_response = MockResponse(200, json={"cuid": "1234"})
        mock_post.return_value = mock_response

        self.run_async(api_client.log_figure, mock_figure())

        url = f"{os.environ['VM_API_HOST']}/log_figure"
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args[0][0], url)
        self.assertIsInstance(mock_post.call_args[1]["data"], FormData)

    # @patch("aiohttp.ClientSession.post")
    # def test_log_figures(self, mock_post: MagicMock):
    #     mock_response = MockResponse(200, json=[{"cuid": "1234"}, {"cuid": "5678"}])
    #     mock_post.return_value = mock_response
    #     api_client.client_config.feature_flags["log_figures"] = True

    #     self.run_async(api_client.log_figures, [mock_figure(), mock_figure()])

    #     url = f"{os.environ['VM_API_HOST']}/log_figures"
    #     mock_post.assert_called_once()
    #     self.assertEqual(len(mock_post.call_args), 2)
    #     self.assertEqual(mock_post.call_args[0][0], url)
    #     self.assertIsInstance(mock_post.call_args[1]["data"], FormData)

    @patch("aiohttp.ClientSession.post")
    def test_log_metadata(self, mock_post: MagicMock):
        mock_response = MockResponse(200, json={"cuid": "abc1234"})
        mock_post.return_value = mock_response

        self.run_async(
            api_client.log_metadata,
            "1234",
            text="Some Text",
            _json={"key": "value"},
        )

        url = f"{os.environ['VM_API_HOST']}/log_metadata"
        mock_post.assert_called_with(
            url,
            data=json.dumps(
                {
                    "content_id": "1234",
                    "text": "Some Text",
                    "json": {"key": "value"},
                }
            ),
        )

    @patch("aiohttp.ClientSession.post")
    def test_log_metrics(self, mock_post):
        metrics = [Mock(serialize=MagicMock(return_value={"key": "value"}))]

        mock_response = MockResponse(200, json={"cuid": "abc1234"})
        mock_post.return_value = mock_response

        self.run_async(api_client.log_metrics, metrics, inputs=["input1"])

        url = f"{os.environ['VM_API_HOST']}/log_metrics"
        mock_post.assert_called_with(
            url, data=json.dumps([{"key": "value", "inputs": ["input1"]}])
        )

    @patch("aiohttp.ClientSession.post")
    def test_log_test_result(self, mock_post):
        result = Mock(serialize=MagicMock(return_value={"key": "value"}))

        mock_response = MockResponse(200, json={"cuid": "abc1234"})
        mock_post.return_value = mock_response

        self.run_async(api_client.log_test_result, result, ["input1"])

        url = f"{os.environ['VM_API_HOST']}/log_test_results"

        mock_post.assert_called_with(
            url, data=json.dumps({"key": "value", "inputs": ["input1"]})
        )

    @patch("validmind.api_client.log_test_result")
    def test_log_test_results(self, mock_log_test_result: MagicMock):
        results = [Mock(), Mock()]
        api_client.log_test_results(results, inputs=["input1"])

        mock_log_test_result.assert_has_calls(
            [
                call(results[0], ["input1"]),
                call(results[1], ["input1"]),
            ]
        )


if __name__ == "__main__":
    unittest.main()
