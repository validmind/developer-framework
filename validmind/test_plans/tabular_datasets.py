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
    DescriptiveStatistics,
    PearsonCorrelationMatrix,
)
from ..data_validation.threshold_tests import (
    ClassImbalance,
    Duplicates,
    HighCardinality,
    HighPearsonCorrelation,
    MissingValues,
    Skewness,
    UniqueRows,
    TooManyZeroValues,
    TimeSeriesOutliers,
    TimeSeriesMissingValues,
    TimeSeriesFrequency,
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
        DescriptiveStatistics,
        PearsonCorrelationMatrix,
        DatasetCorrelations,
    ]


class TabularDataQuality(TestPlan):
    """
    Test plan for data quality on tabular datasets
    """

    name = "tabular_data_quality"
    required_context = ["dataset"]
    tests = [
        ClassImbalance,
        Duplicates,
        HighCardinality,
        HighPearsonCorrelation,
        MissingValues,
        Skewness,
        UniqueRows,
        TooManyZeroValues,
    ]


class TimeSeriesDataQuality(TestPlan):
    """
    Test plan for data quality on time series datasets
    """

    name = "time_series_data_quality"
    required_context = ["dataset"]
    tests = [TimeSeriesOutliers, TimeSeriesMissingValues, TimeSeriesFrequency]
