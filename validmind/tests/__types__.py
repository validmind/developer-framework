# Copyright © 2023 ValidMind Inc. All rights reserved.

"""All Tests for ValidMind"""

from typing import Any, Dict, Protocol


class ExternalTest(Protocol):
    """Protocol for user-defined tests"""

    test_type: str

    def description(self) -> str:
        """Return the test description (optional)

        If this method is not implemented, the test description will be
        automatically generated from the docstring of the test class.

        Returns:
            str: The test description
        """
        ...

    def run(self) -> Dict[str, Any]:
        """Run the test and return the results

        Returns:
            dict: The test results object to be saved
        """
        ...

    def summary(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize the test results

        Args:
            test_results (dict): The test results object

        Returns:
            dict: The test summary object to be displayed
        """
        ...


class ExternalTestProvider(Protocol):
    """Protocol for user-defined test providers"""

    def load_test(self, test_id: str) -> ExternalTest:
        """Load the test by test ID

        Args:
            test_id (str): The test ID (does not contain the namespace under which
                the test is registered)

        Returns:
            ExternalTest: The test object

        Raises:
            FileNotFoundError: If the test is not found
        """
        ...
