from validmind.test_plans import register_test_plan
from validmind.test_suites import register_test_suite
from validmind.vm_models import TestPlan, TestSuite


class TabularDataQualityExtra(TestPlan):
    """
    Expanded test plan for data quality on tabular datasets
    """

    name = "tabular_data_quality_extra"
    tests = [
        "validmind.data_validation.FeatureTargetCorrelationPlot",
        "validmind.data_validation.IQROutliersBarPlot",
        "validmind.data_validation.IQROutliersTable",
        "validmind.data_validation.ScatterPlot",
        "validmind.data_validation.TabularCategoricalBarPlots",
        "validmind.data_validation.TabularNumericalHistograms",
    ]


class CustomTabularDataset(TestSuite):
    """
    Test suite for tabular datasets.
    """

    name = "custom_tabular_dataset"

    test_plans = [
        "tabular_dataset_description",
        "tabular_data_quality",
        "tabular_data_quality_extra",
    ]


class RegressionTestsExtra(TestPlan):
    """
    Expanded test plan for regression models
    """

    name = "regression_extra"
    tests = [
        "validmind.model_validation.statsmodels.RegressionCoeffsPlot",
    ]


class RegressionSuite(TestSuite):
    """
    Test suite for regression models.
    """

    name = "custom_regression_suite"

    test_plans = [
        "regression_extra",
        "regression_model_description",
        "regression_models_evaluation",
    ]


register_test_plan("tabular_data_quality_extra", TabularDataQualityExtra)
register_test_suite("custom_tabular_dataset", CustomTabularDataset)

register_test_plan("regression_extra", RegressionTestsExtra)
register_test_suite("custom_regression_suite", RegressionSuite)
