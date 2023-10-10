from validmind.vm_models import TestSuite


class RegressionMetrics(TestSuite):
    """
    Test suite for performance metrics of regression metrics
    """

    suite_id = "regression_metrics"
    tests = [
        "validmind.data_validation.DatasetSplit",
        "validmind.model_validation.ModelMetadata",
        "validmind.model_validation.sklearn.PermutationFeatureImportance",
    ]


class RegressionPerformance(TestSuite):
    """
    Test suite for regression model performance
    """

    suite_id = "regression_performance"
    tests = [
        "validmind.model_validation.sklearn.RegressionErrors",
        "validmind.model_validation.sklearn.RegressionR2Square",
    ]
