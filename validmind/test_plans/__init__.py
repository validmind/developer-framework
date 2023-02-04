"""
Test Plans entry point
"""


class TestPlan:
    """
    Base class for test plans. Test plans are used to define any
    arbitrary grouping of tests that will be run on a dataset or model.
    """

    def __init__(self, client, config=None, **kwargs):
        """
        :param client: ValidMind client instance
        :param config: The test plan configuration
        :param dict kwargs: Additional keyword arguments
        """
        self.client = client
        self.config = config
        self.kwargs = kwargs

    def run():
        """
        Runs the test plan
        """
        raise NotImplementedError
