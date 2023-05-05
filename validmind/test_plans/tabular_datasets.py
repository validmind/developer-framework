"""
Test plan for tabular datasets

Ideal setup is to have the API client to read a
custom test plan from the project's configuration
"""

from ..vm_models import TestPlan
from ..data_validation.metrics import (
    DatasetCorrelations,
    DatasetDescription,
    DatasetMetadata,
)
from ..data_validation.threshold_tests import (
    ClassImbalanceTest,
    DuplicatesTest,
    HighCardinalityTest,
    HighPearsonCorrelationTest,
    MissingValuesTest,
    SkewnessTest,
    UniqueRowsTest,
    ZerosTest,
    OutliersTest,
    TimeSeriesMissingValuesTest
)


class TabularDatasetDescription(TestPlan):
    """
    Test plan to extract metadata and descriptive
    statistics from a tabular dataset
    """

    name = "tabular_dataset_description"
    required_context = ["dataset"]
    tests = [
        DatasetMetadata,
        DatasetDescription,
        DatasetCorrelations,
    ]


class TabularDataQuality(TestPlan):
    """
    Test plan for data quality on tabular datasets
    """

    name = "tabular_data_quality"
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
        OutliersTest,
        TimeSeriesMissingValuesTest
    ]


class TabularDataset(TestPlan):
    """
    Test plan for generic tabular datasets
    """

    name = "tabular_dataset"
    required_context = ["dataset"]
    test_plans = [
        TabularDatasetDescription,
        TabularDataQuality,
    ]
