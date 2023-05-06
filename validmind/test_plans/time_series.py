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
)


class TimeSeriesUnivariate(TestPlan):
    """
    Test plan to perform univariate inspection tests.
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
        This section provides a preliminary understanding of the target variable(s)
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
    Test plan to perform univariate inspection tests.
    """

    name = "time_series_multivariate"
    required_context = ["dataset"]
    tests = [ScatterPlot, LaggedCorrelationHeatmap]

    def description(self):
        return """
        This section provides a preliminary understanding of the features
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


class Seasonality(TestPlan):
    """
    Test plan to perform seasonality tests.
    """

    name = "seasonality"
    required_context = ["dataset"]
    tests = [ACFandPACFPlot, SeasonalDecompose, AutoSeasonality]

    def description(self):
        return """
        This test plan aims to detect seasonality in the provided dataset. It provides various visualizations and statistical tests to identify the presence of seasonality in the time series. The ACF and PACF plots help to identify the order of the autoregressive (AR) and moving average (MA) components in the time series, while the seasonal decomposition test provides insights into the trend and seasonality components. The auto-seasonality test uses different periods to test seasonality and identify the best fit. The results of these tests can help guide further exploration and modeling of the time series data.
        """


class Stationarity(TestPlan):
    """
    Test plan to perform stationarity tests.
    """

    name = "stationarity"
    required_context = ["dataset"]
    tests = [AutoStationarity, RollingStatsPlot]
