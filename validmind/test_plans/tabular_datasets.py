# This software is proprietary and confidential. Unauthorized copying,
# modification, distribution or use of this software is strictly prohibited.
# Please refer to the LICENSE file in the root directory of this repository
# for more information.
#
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
    required_context = ["dataset"]
    tests = [
        "validmind.data_validation.DatasetMetadata",
        "validmind.data_validation.DatasetDescription",
        "validmind.data_validation.DescriptiveStatistics",
        "validmind.data_validation.PearsonCorrelationMatrix",
        "validmind.data_validation.DatasetCorrelations",
    ]


class TabularDataQuality(TestPlan):
    """
    Test plan for data quality on tabular datasets
    """

    name = "tabular_data_quality"
    required_context = ["dataset"]
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
    required_context = ["dataset"]
    tests = [
        "validmind.data_validation.TimeSeriesOutliers",
        "validmind.data_validation.TimeSeriesMissingValues",
        "validmind.data_validation.TimeSeriesFrequency",
    ]
