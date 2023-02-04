"""
Data Validation module
"""

from tabulate import tabulate

from . import threshold_tests


def get_threshold_tests(pretty: bool = False):
    """
    Returns a list of all available threshold tests
    """
    tests = [
        getattr(threshold_tests, name)
        for name in dir(threshold_tests)
        if name.endswith("Test") and name != "ThresholdTest"
    ]
    if pretty:
        return tabulate(
            [(test.category, test.name, test.default_params) for test in tests],
            headers=["Category", "Name", "Default Params"],
        )

    return threshold_tests
