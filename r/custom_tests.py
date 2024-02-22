from validmind.test_suites import register_test_suite
from validmind.vm_models import TestSuite

from validmind.test_suites import (
    TabularDatasetDescription,
    RegressionMetrics
)


class TabularDataQualityExtra(TestSuite):
    """
    Expanded test suite for data quality on tabular datasets
    """

    suite_id = "tabular_data_quality_extra"
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

    suite_id = "custom_tabular_dataset"
    tests = [
        {
            "section_id": TabularDataQualityExtra.suite_id,
            "section_description": TabularDataQualityExtra.__doc__,
            "section_tests": TabularDataQualityExtra.tests,
        },
        {
            "section_id": TabularDatasetDescription.suite_id,
            "section_description": TabularDatasetDescription.__doc__,
            "section_tests": TabularDatasetDescription.tests,
        }
    ]

class RegressionTestsExtra(TestSuite):
    """
    Expanded test suite for regression models
    """

    suite_id = "regression_extra"
    tests = [
        "validmind.model_validation.statsmodels.RegressionCoeffsPlot",
    ]


class RegressionSuite(TestSuite):
    """
    Test suite for regression models.
    """

    suite_id = "custom_regression_suite"
    tests = [
        {
            "section_id": RegressionMetrics.suite_id,
            "section_description": RegressionMetrics.__doc__,
            "section_tests": RegressionMetrics.tests,
        },
        {
            "section_id": TabularDatasetDescription.suite_id,
            "section_description": TabularDatasetDescription.__doc__,
            "section_tests": TabularDatasetDescription.tests,
        }
    ]


register_test_suite("tabular_data_quality_extra", TabularDataQualityExtra)
register_test_suite("custom_tabular_dataset", CustomTabularDataset)

register_test_suite("regression_extra", RegressionTestsExtra)
register_test_suite("custom_regression_suite", RegressionSuite)
