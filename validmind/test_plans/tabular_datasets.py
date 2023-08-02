# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Test plan for tabular datasets

Ideal setup is to have the API client to read a
custom test plan from the project's configuration
"""

from validmind.vm_models import TestPlan


class TabularDatasetDescription(TestPlan):
    """
    Test plan to extract metadata and descriptive
    statistics from a tabular dataset
    """

    name = "tabular_dataset_description"
    tests = [
        "validmind.data_validation.DatasetMetadata",
        "validmind.data_validation.DatasetDescription",
        "validmind.data_validation.DescriptiveStatistics",
        "validmind.data_validation.PearsonCorrelationMatrix",
    ]


class TabularDataQuality(TestPlan):
    """
    Test plan for data quality on tabular datasets
    """

    name = "tabular_data_quality"
    tests = [
        "validmind.data_validation.ClassImbalance",
        "validmind.data_validation.Duplicates",
        "validmind.data_validation.HighCardinality",
        "validmind.data_validation.HighPearsonCorrelation",
        "validmind.data_validation.MissingValues",
        "validmind.data_validation.Skewness",
        "validmind.data_validation.UniqueRows",
        "validmind.data_validation.TooManyZeroValues",
    ]


class TimeSeriesDataQuality(TestPlan):
    """
    Test plan for data quality on time series datasets
    """

    name = "time_series_data_quality"
    tests = [
        "validmind.data_validation.TimeSeriesOutliers",
        "validmind.data_validation.TimeSeriesMissingValues",
        "validmind.data_validation.TimeSeriesFrequency",
    ]
