"""
Test plan for tabular datasets

Ideal setup is to have the API client to read a
custom test plan from the project's configuration
"""

from ... import TestPlan


class GenericDatasetTestPlan(TestPlan):
    """
    Test plan for generic tabular datasets
    """

    def run(self):
        """
        Runs the test plan
        """
        self.client.run_dataset_tests(self.config, **self.kwargs)
