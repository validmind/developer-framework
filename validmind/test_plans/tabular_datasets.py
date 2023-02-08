"""
Test plan for tabular datasets

Ideal setup is to have the API client to read a
custom test plan from the project's configuration
"""

from .test_plan import TestPlan
from ..data_validation.threshold_tests import (
    ClassImbalanceTest,
    DuplicatesTest,
    HighCardinalityTest,
    HighPearsonCorrelationTest,
    MissingValuesTest,
    SkewnessTest,
    UniqueRowsTest,
    ZerosTest,
)


class GenericTabularDatasetTestPlan(TestPlan):
    """
    Test plan for generic tabular datasets
    """

    name = "generic_tabular_dataset"
    required_context = ["dataset"]
    tests = [
        ClassImbalanceTest,
        DuplicatesTest,
        HighCardinalityTest,
        HighPearsonCorrelationTest,
        MissingValuesTest,
        SkewnessTest,
        UniqueRowsTest,
        ZerosTest,
    ]
