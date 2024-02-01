# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import importlib.util
import os
import sys

import requests

from validmind.logging import get_logger

logger = get_logger(__name__)


class GithubTestProviderDownloadError(Exception):
    """
    When the remote file can't be downloaded from the repo.
    """

    pass


class GithubTestProviderWriteFileError(Exception):
    """
    When the remote file can't be downloaded from the repo.
    """

    pass


class GithubTestProviderLoadModuleError(Exception):
    """
    When the remote file was downloaded but the module can't be loaded.
    """

    pass


class GithubTestProviderLoadTestError(Exception):
    """
    When the module was loaded but the test class can't be located.
    """

    pass


class LocalTestProviderLoadModuleError(Exception):
    """
    When the local file module can't be loaded.
    """

    pass


class LocalTestProviderLoadTestError(Exception):
    """
    When local file module was loaded but the test class can't be located.
    """

    pass


class GithubTestProvider:
    """
    A class used to download python files from a Github repository and
    dynamically load and execute the tests from those files.
    """

    BASE_URL = "https://api.github.com/repos"

    def __init__(self, org: str, repo: str, token: str):
        """
        Initialize the GithubTestProvider with the given org, repo, and token.

        Args:
            org (str): The Github organization.
            repo (str): The Github repository.
            token (str): The Github access token.
        """
        self.org = org
        self.repo = repo
        self.token = token

    def _download_file(self, test_path: str) -> str:
        """
        Download the file at the given test_path from the Github repository.

        Args:
            test_path (str): The path of the file in the repository.

        Returns:
            str: The local file path where the file was downloaded.

        Raises:
            Exception: If the file can't be downloaded or written.
        """
        url = f"{self.BASE_URL}/{self.org}/{self.repo}/contents/{test_path}"

        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3.raw",
            "X-Github-Api-Version": "2022-11-28",
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            raise GithubTestProviderDownloadError(
                f"Failed to download the file at {url}. Error: {str(e)}"
            )

        file_path = f"/tmp/{os.path.basename(test_path)}"
        try:
            with open(file_path, "w") as file:
                file.write(response.text)
        except IOError as e:
            raise GithubTestProviderWriteFileError(
                f"Failed to write the file to {file_path}. Error: {str(e)}"
            )

        return file_path

    def load_test(self, test_id):
        """
        Load the test identified by the given test_id.

        Args:
            test_id (str): The identifier of the test. This corresponds to the
            relative path of the python file in the repository, with slashes replaced by dots.

        Returns:
            The test class that matches the last part of the test_id.

        Raises:
            Exception: If the test can't be imported or loaded.
        """
        test_path = f"{test_id.replace('.', '/')}.py"
        file_path = self._download_file(test_path)

        try:
            spec = importlib.util.spec_from_file_location(test_id, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            raise GithubTestProviderLoadModuleError(
                f"Failed to load the module from {file_path}. Error: {str(e)}"
            )

        try:
            # find the test class that matches the last part of the test_id
            return getattr(module, test_id.split(".")[-1])
        except AttributeError as e:
            raise GithubTestProviderLoadTestError(
                f"Failed to find the test class in the module. Error: {str(e)}"
            )


class LocalTestProvider:
    """
    Test providers in ValidMind are responsible for loading tests from different sources,
    such as local files, databases, or remote services. The LocalTestProvider specifically
    loads tests from the local file system.

    To use the LocalTestProvider, you need to provide the root_folder, which is the
    root directory for local tests. The test_id is a combination of the namespace (set
    when registering the test provider) and the path to the test class module, where
    slashes are replaced by dots and the .py extension is left out.

    Example usage:

    ```
    # Create an instance of LocalTestProvider with the root folder
    test_provider = LocalTestProvider("/path/to/tests/folder")

    # Register the test provider with a namespace
    register_test_provider("my_namespace", test_provider)

    # Load a test using the test_id (namespace + path to test class module)
    test = test_provider.load_test("my_namespace.my_test_class")
    # full path to the test class module is /path/to/tests/folder/my_test_class.py
    ```

    Attributes:
        root_folder (str): The root directory for local tests.
    """

    def __init__(self, root_folder: str):
        """
        Initialize the LocalTestProvider with the given root_folder
        (see class docstring for details)

        Args:
            root_folder (str): The root directory for local tests.
        """
        self.root_folder = root_folder

    def load_test(self, test_id: str):
        """
        Load the test identified by the given test_id.

        Args:
            test_id (str): The identifier of the test. This corresponds to the relative
            path of the python file from the root folder, with slashes replaced by dots

        Returns:
            The test class that matches the last part of the test_id.

        Raises:
            Exception: If the test can't be imported or loaded.
        """
        test_path = f"{test_id.replace('.', '/')}.py"
        file_path = os.path.join(self.root_folder, test_path)

        logger.debug(f"Loading test {test_id} from {file_path}")

        # Check if the module uses relative imports
        with open(file_path, "r") as file:
            lines = file.readlines()

        # handle test with relative imports
        if any(line.strip().startswith("from .") for line in lines):
            logger.debug("Found relative imports, using alternative import method")

            parent_folder = os.path.dirname(file_path)
            if parent_folder not in sys.path:
                sys.path.append(os.path.dirname(parent_folder))

            try:
                module = importlib.import_module(
                    f"{os.path.basename(parent_folder)}.{test_id.split('.')[-1]}"
                )
            except Exception as e:
                # error will be handled/re-raised by `load_test` func
                raise LocalTestProviderLoadModuleError(
                    f"Failed to load the module from {file_path}. Error: {str(e)}"
                )

        else:
            try:
                spec = importlib.util.spec_from_file_location(test_id, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            except Exception as e:
                # error will be handled/re-raised by `load_test` func
                raise LocalTestProviderLoadModuleError(
                    f"Failed to load the module from {file_path}. Error: {str(e)}"
                )

        try:
            # find the test class that matches the last part of the test_id
            return getattr(module, test_id.split(".")[-1])
        except AttributeError as e:
            raise LocalTestProviderLoadTestError(
                f"Failed to find the test class in the module. Error: {str(e)}"
            )
