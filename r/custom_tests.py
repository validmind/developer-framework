from validmind.test_suites import register_test_suite
from validmind.vm_models import TestSuite

from validmind.test_suites import (
    RegressionModelDescription,
    RegressionModelsEvaluation,
    TabularDatasetDescription,
    TabularDataQuality,
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
        }
        {
            "section_id": TabularDatasetDescription.suite_id,
            "section_description": TabularDatasetDescription.__doc__,
            "section_tests": TabularDatasetDescription.tests,
        }
        {
            "section_id": TabularDataQualityExtra.suite_id,
            "section_description": TabularDataQualityExtra.__doc__,
            "section_tests": TabularDataQualityExtra.tests,
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
            "section_id": RegressionTestsExtra.suite_id,
            "section_description": RegressionTestsExtra.__doc__,
            "section_tests": RegressionTestsExtra.tests,
        },
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
    ]


register_test_suite("tabular_data_quality_extra", TabularDataQualityExtra)
register_test_suite("custom_tabular_dataset", CustomTabularDataset)

register_test_suite("regression_extra", RegressionTestsExtra)
register_test_suite("custom_regression_suite", RegressionSuite)
