"""
Time Series Test Plans from statsmodels
"""
from ..vm_models import TestPlan
from ..model_validation.statsmodels.metrics import (
    DurbinWatsonTest,
    LJungBox,
    JarqueBera,
    KolmogorovSmirnov,
    ShapiroWilk,
    Lilliefors,
    ADFTest,
    KPSSTest,
    PhillipsPerronTest,
    ZivotAndrewsTest,
    DFGLSTest,
    SeasonalDecomposeMetricWithFigure,
    ResidualsVisualInspection,
)


class AutocorrelationTestPlan(TestPlan):
    """
    Test plan to perform autocorrelation tests.
    """

    name = "autocorrelation_test_plan"
    required_context = ["train_ds", "test_ds"]
    tests = [LJungBox, DurbinWatsonTest]


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


class SesonalityTestPlan(TestPlan):
    """
    Test plan to perform seasonality tests.
    """

    name = "seasonality_test_plan"
    required_context = ["train_ds", "test_ds"]
    tests = [SeasonalDecomposeMetricWithFigure]
    test_plans = [ResidualsTestPlan]


class UnitRootTestPlan(TestPlan):
    """
    Test plan to perform unit root tests.
    """

    name = "unit_root_test_plan"
    required_context = ["train_ds", "test_ds"]
    tests = [ADFTest, KPSSTest, PhillipsPerronTest, ZivotAndrewsTest, DFGLSTest]


class StationarityTestPlan(TestPlan):
    """
    Test plan to perform stationarity tests.
    """

    name = "stationarity_test_plan"
    required_context = ["train_ds", "test_ds"]
    test_plans = [UnitRootTestPlan]


class TimeSeriesTestPlan(TestPlan):
    """
    Test plan for time series statsmodels that includes
    both metrics and validation tests
    """

    name = "timeseries_test_plan"
    required_context = ["train_ds", "test_ds"]
    test_plans = [SesonalityTestPlan, StationarityTestPlan]
