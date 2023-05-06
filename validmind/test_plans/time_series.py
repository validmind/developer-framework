"""
Time Series Test Plans
"""
from ..vm_models import TestPlan
from ..data_validation.metrics import (
    TimeSeriesHistogram,
    TimeSeriesLinePlot,
    ScatterPlot,
    LaggedCorrelationHeatmap,
    AutoAR,
    AutoMA,
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
