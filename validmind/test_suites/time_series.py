# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Time Series Test Suites
"""
from validmind.vm_models import TestSuite

from .statsmodels_timeseries import (
    RegressionModelDescription,
    RegressionModelsEvaluation,
)


class TimeSeriesDataQuality(TestSuite):
    """
    Test suite for data quality on time series datasets
    """

    suite_id = "time_series_data_quality"
    tests = [
        "validmind.data_validation.TimeSeriesOutliers",
        "validmind.data_validation.TimeSeriesMissingValues",
        "validmind.data_validation.TimeSeriesFrequency",
    ]


class TimeSeriesUnivariate(TestSuite):
    """
    This test suite provides a preliminary understanding of the target variable(s)
    used in the time series dataset. It visualizations that present the raw time
    series data and a histogram of the target variable(s).

    The raw time series data provides a visual inspection of the target variable's
    behavior over time. This helps to identify any patterns or trends in the data,
    as well as any potential outliers or anomalies. The histogram of the target
    variable displays the distribution of values, providing insight into the range
    and frequency of values observed in the data.
    """

    suite_id = "time_series_univariate"
    tests = [
        "validmind.data_validation.TimeSeriesLinePlot",
        "validmind.data_validation.TimeSeriesHistogram",
        "validmind.data_validation.ACFandPACFPlot",
        "validmind.data_validation.SeasonalDecompose",
        "validmind.data_validation.AutoSeasonality",
        "validmind.data_validation.AutoStationarity",
        "validmind.data_validation.RollingStatsPlot",
        "validmind.data_validation.AutoAR",
        "validmind.data_validation.AutoMA",
    ]


class TimeSeriesMultivariate(TestSuite):
    """
    This test suite provides a preliminary understanding of the features
    and relationship in multivariate dataset. It presents various
    multivariate visualizations that can help identify patterns, trends,
    and relationships between pairs of variables. The visualizations are
    designed to explore the relationships between multiple features
    simultaneously. They allow you to quickly identify any patterns or
    trends in the data, as well as any potential outliers or anomalies.
    The individual feature distribution can also be explored to provide
    insight into the range and frequency of values observed in the data.
    This multivariate analysis test suite aims to provide an overview of
    the data structure and guide further exploration and modeling.
    """

    suite_id = "time_series_multivariate"
    tests = [
        "validmind.data_validation.ScatterPlot",
        "validmind.data_validation.LaggedCorrelationHeatmap",
        "validmind.data_validation.EngleGrangerCoint",
        "validmind.data_validation.SpreadPlot",
    ]


class TimeSeriesForecast(TestSuite):
    """
    This test suite computes predictions from statsmodels OLS linear regression models
    against a list of models and plots the historical data alongside the forecasted data.
    The purpose of this test suite is to evaluate the performance of each model in predicting
    future values of a time series based on historical data. By comparing the historical
    values with the forecasted values, users can visually assess the accuracy of each model
    and determine which one best fits the data. In addition, this test suite can help users
    identify any discrepancies between the models and the actual data, allowing for potential
    improvements in model selection and parameter tuning.
    """

    suite_id = "time_series_forecast"
    tests = ["validmind.model_validation.statsmodels.RegressionModelForecastPlotLevels"]


class TimeSeriesSensitivity(TestSuite):
    """
    This test suite performs sensitivity analysis on a statsmodels OLS linear regression model
    by applying distinct shocks to each input variable individually and then computing the
    model's predictions. The aim of this test suite is to investigate the model's responsiveness
    to variations in its inputs. By juxtaposing the model's predictions under baseline and shocked
    conditions, users can visually evaluate the sensitivity of the model to changes in each
    variable. This kind of analysis can also shed light on potential model limitations, including
    over-reliance on specific variables or insufficient responsiveness to changes in inputs. As a
    result, this test suite can provide insights that may be beneficial for refining the model
    structure, improving its robustness, and ensuring a more reliable prediction performance.
    """

    suite_id = "time_series_sensitivity"
    tests = ["validmind.model_validation.statsmodels.RegressionModelSensitivityPlot"]


class TimeSeriesDataset(TestSuite):
    """
    Test suite for time series datasets.
    """

    suite_id = "time_series_dataset"
    tests = [
        {
            "section_id": TimeSeriesDataQuality.suite_id,
            "section_description": TimeSeriesDataQuality.__doc__,
            "section_tests": TimeSeriesDataQuality.tests,
        },
        {
            "section_id": TimeSeriesUnivariate.suite_id,
            "section_description": TimeSeriesUnivariate.__doc__,
            "section_tests": TimeSeriesUnivariate.tests,
        },
        {
            "section_id": TimeSeriesMultivariate.suite_id,
            "section_description": TimeSeriesMultivariate.__doc__,
            "section_tests": TimeSeriesMultivariate.tests,
        },
    ]


class TimeSeriesModelValidation(TestSuite):
    """
    Test suite for time series model validation.
    """

    suite_id = "time_series_model_validation"
    tests = [
        {
            "section_id": RegressionModelDescription.suite_id,
            "section_description": RegressionModelDescription.__doc__,
            "section_tests": RegressionModelDescription.tests,
        },
        {
            "section_id": RegressionModelsEvaluation.suite_id,
            "section_description": RegressionModelsEvaluation.__doc__,
            "section_tests": RegressionModelsEvaluation.tests,
        },
        {
            "section_id": TimeSeriesForecast.suite_id,
            "section_description": TimeSeriesForecast.__doc__,
            "section_tests": TimeSeriesForecast.tests,
        },
        {
            "section_id": TimeSeriesSensitivity.suite_id,
            "section_description": TimeSeriesSensitivity.__doc__,
            "section_tests": TimeSeriesSensitivity.tests,
        },
    ]
