"""
Time Series Test Plans
"""
from ..vm_models import TestPlan
from ..data_validation.metrics import (
    TimeSeriesUnivariateInspectionHistogram,
    TimeSeriesUnivariateInspectionRaw,
)


class TimeSeriesUnivariateInspection(TestPlan):
    """
    Test plan to perform univariate inspection tests.
    """

    name = "time_series_univariate_inspection"
    required_context = ["dataset"]
    tests = [TimeSeriesUnivariateInspectionHistogram, TimeSeriesUnivariateInspectionRaw]
