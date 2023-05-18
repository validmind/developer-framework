import asyncio
import json
import os
import unittest
from unittest.mock import MagicMock, Mock, patch

import aiohttp
import requests

from validmind.api_client import (
    get_api_config,
    get_api_host,
    get_api_project,
    init,
    get_metadata,
    log_dataset,
    log_figure,
    log_metadata,
    log_metrics,
    log_model,
    log_test_result,
    log_test_results,
    start_run,
)

class TestYourModule(unittest.TestCase):

    def setUp(self):
        os.environ["VM_API_KEY"] = "your_api_key"
        os.environ["VM_API_SECRET"] = "your_api_secret"
        os.environ["VM_API_HOST"] = "your_api_host"
        os.environ["VM_PROJECT"] = "your_project"
        os.environ["VM_RUN_CUID"] = "your_run_cuid"

    def tearDown(self):
        os.environ.pop("VM_API_KEY", None)
        os.environ.pop("VM_API_SECRET", None)
        os.environ.pop("VM_API_HOST", None)
        os.environ.pop("VM_PROJECT", None)
        os.environ.pop("VM_RUN_CUID", None)

    def test_get_api_config(self):
        config = get_api_config()
        self.assertEqual(config["VM_API_KEY"], "your_api_key")
        self.assertEqual(config["VM_API_SECRET"], "your_api_secret")
        self.assertEqual(config["VM_API_HOST"], "your_api_host")
        self.assertEqual(config["VM_PROJECT"], "your_project")
        self.assertEqual(config["VM_RUN_CUID"], "your_run_cuid")

    def test_get_api_host(self):
        host = get_api_host()
        self.assertEqual(host, "your_api_host")

    def test_get_api_project(self):
        project = get_api_project()
        self.assertEqual(project, "your_project")

    @patch("requests.get")
    def test_init_successful(self, mock_requests_get):
        mock_response = Mock(status_code=200)
        mock_requests_get.return_value = mock_response

        success = init(project="project_id", api_key="api_key", api_secret="api_secret", api_host="api_host")
        self.assertTrue(success)

        mock_requests_get.assert_called_once_with(
            "api_host/ping",
            headers={
                "X-API-KEY": "api_key",
                "X-API-SECRET": "api_secret",
                "X-PROJECT-CUID": "project_id",
            },
        )

    @patch("requests.get")
    def test_init_missing_project_id(self, mock_requests_get):
        mock_response = Mock(status_code=200)
        mock_requests_get.return_value = mock_response

        with self.assertRaises(ValueError):
            init(project=None)

        mock_requests_get.assert_not_called()

    @patch("requests.get")
    def test_init_missing_api_key_secret(self, mock_requests_get):
        mock_response = Mock(status_code=200)
        mock_requests_get.return_value = mock_response

        with self.assertRaises(ValueError):
            init(project="project_id", api_key=None, api_secret=None)

        mock_requests_get.assert_not_called()

    @patch("requests.get")
    def test_init_unsuccessful_ping(self, mock_requests_get):
        mock_response = Mock(status_code=500)
        mock_response.text = "Internal Server Error"
        mock_requests_get.return_value = mock_response

        with self.assertRaises(Exception) as cm:
            init(project="project_id", api_key="api_key", api_secret="api_secret", api_host="api_host")

        self.assertEqual(str(cm.exception), "Internal Server Error")

        mock_requests_get.assert_called_once_with(
            "api_host/ping",
            headers={
                "X-API-KEY": "api_key",
                "X-API-SECRET": "api_secret",
                "X-PROJECT-CUID": "project_id",
            },
        )

    @patch("aiohttp.ClientSession")
    def test_get_metadata(self, mock_client_session):
        mock_session = MagicMock()
        mock_client_session.return_value.__aenter__.return_value = mock_session
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json.return_value = {"metadata": "example"}
        mock_session.get.return_value.__aenter__.return_value = mock_response

        asyncio.run(get_metadata("content_id"))

        mock_session.get.assert_called_once_with("your_api_host/get_metadata/content_id")
        mock_response.json.assert_called_once()

    @patch("aiohttp.ClientSession")
    def test_log_dataset(self, mock_client_session):
        mock_session = MagicMock()
        mock_client_session.return_value.__aenter__.return_value = mock_session
        mock_response = Mock()
        mock_response.status = 200
        mock_session.post.return_value.__aenter__.return_value = mock_response

        dataset = {"key": "value"}
        asyncio.run(log_dataset(dataset))

        mock_session.post.assert_called_once_with(
            "your_api_host/log_dataset",
            data=json.dumps(dataset, cls=json.JSONEncoder, allow_nan=False),
        )

    @patch("aiohttp.ClientSession")
    def test_log_figure_with_file_path(self, mock_client_session):
        mock_session = MagicMock()
        mock_client_session.return_value.__aenter__.return_value = mock_session
        mock_response = Mock()
        mock_response.status = 200
        mock_session.post.return_value.__aenter__.return_value = mock_response

        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value = MagicMock()
            mock_open.return_value.__enter__.return_value.read.return_value = "image_data"

            asyncio.run(log_figure("image.jpg", "figure_key", {}))

            mock_session.post.assert_called_once()
            _, kwargs = mock_session.post.call_args
            self.assertEqual(kwargs["data"], {"type": "file_path", "key": "figure_key", "metadata": "{}"})
            self.assertIn("files", kwargs)
            self.assertEqual(kwargs["files"], {"image": ("figure_key.jpg", mock_open.return_value, None)})

    @patch("aiohttp.ClientSession")
    def test_log_figure_with_plot(self, mock_client_session):
        mock_session = MagicMock()
        mock_client_session.return_value.__aenter__.return_value = mock_session
        mock_response = Mock()
        mock_response.status = 200
        mock_session.post.return_value.__aenter__.return_value = mock_response

        plot = MagicMock()
        plot.savefig.return_value = None

        asyncio.run(log_figure(plot, "figure_key", {}))

        mock_session.post.assert_called_once()
        _, kwargs = mock_session.post.call_args
        self.assertEqual(kwargs["data"], {"type": "plot", "key": "figure_key", "metadata": "{}"})
        self.assertIn("files", kwargs)
        self.assertEqual(kwargs["files"], {"image": ("figure_key.png", plot.savefig.return_value, "image/png")})

    @patch("aiohttp.ClientSession")
    def test_log_metadata(self, mock_client_session):
        mock_session = MagicMock()
        mock_client_session.return_value.__aenter__.return_value = mock_session
        mock_response = Mock()
        mock_response.status = 200
        mock_session.post.return_value.__aenter__.return_value = mock_response

        asyncio.run(log_metadata("content_id", "text", {"key": "value"}))

        mock_session.post.assert_called_once_with(
            "your_api_host/log_metadata",
            data=json.dumps(
                {
                    "content_id": "content_id",
                    "text": "text",
                    "extra_json": {"key": "value"},
                },
                cls=json.JSONEncoder,
                allow_nan=False,
            ),
        )

    @patch("aiohttp.ClientSession")
    def test_log_metrics(self, mock_client_session):
        mock_session = MagicMock()
        mock_client_session.return_value.__aenter__.return_value = mock_session
        mock_response = Mock()
        mock_response.status = 200
        mock_session.post.return_value.__aenter__.return_value = mock_response

        metrics = [{"name": "accuracy", "value": 0.8}]
        asyncio.run(log_metrics(metrics))

        mock_session.post.assert_called_once_with(
            "your_api_host/log_metrics",
            data=json.dumps(metrics, cls=json.JSONEncoder, allow_nan=False),
        )

    @patch("aiohttp.ClientSession")
    def test_log_model(self, mock_client_session):
        mock_session = MagicMock()
        mock_client_session.return_value.__aenter__.return_value = mock_session
        mock_response = Mock()
        mock_response.status = 200
        mock_session.post.return_value.__aenter__.return_value = mock_response

        model = {"name": "model"}
        asyncio.run(log_model(model))

        mock_session.post.assert_called_once_with(
            "your_api_host/log_model",
            data=json.dumps(model, cls=json.JSONEncoder, allow_nan=False),
        )

    @patch("aiohttp.ClientSession")
    def test_log_test_result(self, mock_client_session):
        mock_session = MagicMock()
        mock_client_session.return_value.__aenter__.return_value = mock_session
        mock_response = Mock()
        mock_response.status = 200
        mock_session.post.return_value.__aenter__.return_value = mock_response

        result = {"name": "result"}
        asyncio.run(log_test_result(result))

        mock_session.post.assert_called_once_with(
            "your_api_host/log_test_results",
            params={"dataset_type": "training"},
            data=json.dumps(result, cls=json.JSONEncoder, allow_nan=False),
        )

    @patch("aiohttp.ClientSession")
    def test_log_test_results(self, mock_client_session):
        mock_session = MagicMock()
        mock_client_session.return_value.__aenter__.return_value = mock_session
        mock_response = Mock()
        mock_response.status = 200
        mock_session.post.return_value.__aenter__.return_value = mock_response

        result1 = {"name": "result1"}
        result2 = {"name": "result2"}
        results = [result1, result2]
        asyncio.run(log_test_results(results))

        mock_session.post.assert_called_once_with(
            "your_api_host/log_test_results",
            params={"dataset_type": "training"},
            data=json.dumps(results, cls=json.JSONEncoder, allow_nan=False),
        )

    @patch("requests.post")
    def test_start_run_successful(self, mock_requests_post):
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {"cuid": "run_cuid"}
        mock_requests_post.return_value = mock_response

        run_cuid = start_run()
        self.assertEqual(run_cuid, "run_cuid")

        mock_requests_post.assert_called_once_with(
            "your_api_host/start_run",
            headers={
                "X-API-KEY": "your_api_key",
                "X-API-SECRET": "your_api_secret",
                "X-PROJECT-CUID": "your_project",
            },
        )

    @patch("requests.post")
    def test_start_run_unsuccessful(self, mock_requests_post):
        mock_response = Mock(status_code=500)
        mock_response.text = "Internal Server Error"
        mock_requests_post.return_value = mock_response

        with self.assertRaises(Exception) as cm:
            start_run()

        self.assertEqual(str(cm.exception), "Internal Server Error")

        mock_requests_post.assert_called_once_with(
            "your_api_host/start_run",
            headers={
                "X-API-KEY": "your_api_key",
                "X-API-SECRET": "your_api_secret",
                "X-PROJECT-CUID": "your_project",
            },
        )

if __name__ == "__main__":
    unittest.main()
