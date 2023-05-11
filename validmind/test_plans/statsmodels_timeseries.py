"""
Time Series Test Plans from statsmodels
"""
from .time_series import TimeSeriesUnivariate
from ..vm_models import TestPlan
from ..model_validation.statsmodels.metrics import (
    LJungBox,
    BoxPierce,
    RunsTest,
    JarqueBera,
    KolmogorovSmirnov,
    ShapiroWilk,
    Lilliefors,
    ADF,
    KPSS,
    PhillipsPerronArch,
    ZivotAndrewsArch,
    DFGLSArch,
    ResidualsVisualInspection,
    RegressionModelSummary,
    RegressionModelOutsampleComparison,
    RegressionModelInsampleComparison,
)


class AutocorrelationTestPlan(TestPlan):
    """
    Test plan to perform autocorrelation tests.
    """

    name = "autocorrelation_test_plan"
    required_context = ["train_ds", "test_ds"]
    tests = [LJungBox, BoxPierce, RunsTest]


class NormalityTestPlan(TestPlan):
    """
    Test plan to perform normality tests.
    """

    name = "normality_test_plan"
    required_context = ["train_ds", "test_ds"]
    tests = [JarqueBera, KolmogorovSmirnov, ShapiroWilk, Lilliefors]


class ResidualsTestPlan(TestPlan):
    """
    Test plan to perform residual analysis tests.
    """

    name = "residuals_test_plan"
    required_context = ["train_ds", "test_ds"]
    tests = [ResidualsVisualInspection]
    test_plans = [AutocorrelationTestPlan, NormalityTestPlan]


class UnitRoot(TestPlan):
    """
    Test plan to perform unit root tests.
    """

    name = "unit_root"
    required_context = ["dataset"]
    tests = [ADF, KPSS, PhillipsPerronArch, ZivotAndrewsArch, DFGLSArch]


class SesonalityTestPlan(TestPlan):
    """
    Test plan to perform seasonality tests.
    """

    name = "seasonality_test_plan"
    required_context = ["train_ds", "test_ds"]

    test_plans = [ResidualsTestPlan, UnitRoot]


class StationarityTestPlan(TestPlan):
    """
    Test plan to perform stationarity tests.
    """

    name = "stationarity_test_plan"
    required_context = ["train_ds", "test_ds"]
    test_plans = [UnitRoot]


class TimeSeries(TestPlan):
    """
    Test plan for time series statsmodels that includes
    both metrics and validation tests
    """

    name = "timeseries"
    required_context = ["train_ds", "test_ds"]
    test_plans = [
        TimeSeriesUnivariate,
        SesonalityTestPlan,
        StationarityTestPlan,
    ]


class RegressionModelPerformance(TestPlan):
    """
    Test plan for performance metric of regression model of statsmodels library
    """

    name = "regression_model_performance"
    required_context = ["model"]
    tests = [RegressionModelSummary]


class RegressionModelsComparison(TestPlan):
    """
    Test plan for metrics comparison of regression model of statsmodels library
    """

    name = "regression_models_comparison"
    required_context = ["models"]
    tests = [RegressionModelOutsampleComparison, RegressionModelInsampleComparison]
