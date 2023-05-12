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

from ..model_validation.statsmodels.metrics import RegressionModelForecastPlot


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

    def description(self):
        return """
        This test plan aims to assess stationarity in the provided dataset. It provides various visualizations and statistical tests to determine if the time series is stationary. The rolling mean and rolling standard deviation plots help to visually identify any changing trends or variability in the time series. The Augmented Dickey-Fuller (ADF) test is a formal statistical test to determine the presence of a unit root, which indicates non-stationarity in the time series. If a time series is found to be non-stationary, it can be transformed using methods such as differencing or detrending to achieve stationarity before further analysis or modeling is performed. Assessing stationarity is an essential step in the analysis of time series data, as many time series models assume stationarity.
        """


class Cointegration(TestPlan):
    """
    Test plan to perform cointegration tests.
    """

    name = "cointegration"
    required_context = ["dataset"]
    tests = [EngleGrangerCoint, SpreadPlot]

    def description(self):
        return """
        This test plan aims to assess cointegration in the provided dataset. It provides various visualizations and statistical tests to determine if pairs of time series variables share a long-term, equilibrium relationship despite having individual trends. The spread plots help to visually identify any relationships between the time series pairs. The Engle-Granger test is a formal statistical test to determine the presence of cointegration between two time series variables, which suggests that they have a long-run relationship. If a pair of time series is found to be cointegrated, it can be used to build more accurate forecasting models that take into account the long-term relationship between the variables. Assessing cointegration is an essential step in the analysis of time series data, as it can provide valuable insights into the underlying relationships between variables.
        """


class TimeSeriesForecast(TestPlan):
    """
    Test plan to perform time series forecast tests.
    """

    name = "time_series_forecast"
    required_context = ["models"]
    tests = [RegressionModelForecastPlot]

    def description(self):
        return """
        This test plan computes predictions from statsmodels OLS linear regression models against a list of models and plots the historical data alongside the forecasted data. The purpose of this test plan is to evaluate the performance of each model in predicting future values of a time series based on historical data. By comparing the historical values with the forecasted values, users can visually assess the accuracy of each model and determine which one best fits the data. In addition, this test plan can help users identify any discrepancies between the models and the actual data, allowing for potential improvements in model selection and parameter tuning.
        """
