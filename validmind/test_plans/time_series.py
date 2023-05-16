"""
Time Series Test Plans
"""
from ..vm_models import TestPlan
from ..data_validation.metrics import (
    TimeSeriesLinePlot,
    TimeSeriesHistogram,
    ACFandPACFPlot,
    SeasonalDecompose,
    AutoSeasonality,
    AutoStationarity,
    RollingStatsPlot,
    AutoAR,
    AutoMA,
    ScatterPlot,
    LaggedCorrelationHeatmap,
    EngleGrangerCoint,
    SpreadPlot,
)

from ..model_validation.statsmodels.metrics import RegressionModelForecastPlotLevels


class TimeSeriesUnivariate(TestPlan):
    """
    Test plan to perform time series univariate analysis.
    """

    name = "time_series_univariate"
    required_context = ["dataset"]
    tests = [
        TimeSeriesLinePlot,
        TimeSeriesHistogram,
        ACFandPACFPlot,
        SeasonalDecompose,
        AutoSeasonality,
        AutoStationarity,
        RollingStatsPlot,
        AutoAR,
        AutoMA,
    ]

    def description(self):
        return """
        This test plan provides a preliminary understanding of the target variable(s)
        used in the time series dataset. It visualizations that present the raw time
        series data and a histogram of the target variable(s).

        The raw time series data provides a visual inspection of the target variable's
        behavior over time. This helps to identify any patterns or trends in the data,
        as well as any potential outliers or anomalies. The histogram of the target
        variable displays the distribution of values, providing insight into the range
        and frequency of values observed in the data.
        """


class TimeSeriesMultivariate(TestPlan):
    """
    Test plan to perform time series multivariate analysis.
    """

    name = "time_series_multivariate"
    required_context = ["dataset"]
    tests = [
        ScatterPlot,
        LaggedCorrelationHeatmap,
        EngleGrangerCoint,
        SpreadPlot,
    ]

    def description(self):
        return """
        This test plan provides a preliminary understanding of the features
        and relationship in multivariate dataset. It presents various
        multivariate visualizations that can help identify patterns, trends,
        and relationships between pairs of variables. The visualizations are
        designed to explore the relationships between multiple features
        simultaneously. They allow you to quickly identify any patterns or
        trends in the data, as well as any potential outliers or anomalies.
        The individual feature distribution can also be explored to provide
        insight into the range and frequency of values observed in the data.
        This multivariate analysis test plan aims to provide an overview of
        the data structure and guide further exploration and modeling.
        """


class TimeSeriesForecast(TestPlan):
    """
    Test plan to perform time series forecast tests.
    """

    name = "time_series_forecast"
    required_context = ["models"]
    tests = [RegressionModelForecastPlotLevels]

    def description(self):
        return """
        This test plan computes predictions from statsmodels OLS linear regression models against a list of models and plots the historical data alongside the forecasted data. The purpose of this test plan is to evaluate the performance of each model in predicting future values of a time series based on historical data. By comparing the historical values with the forecasted values, users can visually assess the accuracy of each model and determine which one best fits the data. In addition, this test plan can help users identify any discrepancies between the models and the actual data, allowing for potential improvements in model selection and parameter tuning.
        """
