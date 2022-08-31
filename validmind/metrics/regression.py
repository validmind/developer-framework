"""
Regression Metrics
"""
from sklearn.metrics import (
    mean_absolute_error as mean_absolute_error_sklearn,
    mean_squared_error as mean_squared_error_sklearn,
    r2_score as r2_score_sklearn,
)

from ..models import APIMetric, MetricResult


def mae_score(model, test_set, test_preds):
    """
    Compute Mean Absolute Error score metric from sklearn.
    """
    _, y_true = test_set
    y_pred, _ = test_preds

    return MetricResult(
        api_metric=APIMetric(
            type="evaluation",
            scope="test",
            key="mae",
            value=[mean_absolute_error_sklearn(y_true, y_pred)],
        )
    )


def mse_score(model, test_set, test_preds):
    """
    Compute Mean Squared Error score metric from sklearn.
    """
    _, y_true = test_set
    y_pred, _ = test_preds

    return MetricResult(
        api_metric=APIMetric(
            type="evaluation",
            scope="test",
            key="mse",
            value=[mean_squared_error_sklearn(y_true, y_pred)],
        )
    )


def r2_score(model, test_set, test_preds):
    """
    Compute R-Squared score metric from sklearn.
    """
    _, y_true = test_set
    y_pred, _ = test_preds

    return MetricResult(
        api_metric=APIMetric(
            type="evaluation",
            scope="test",
            key="r2",
            value=[r2_score_sklearn(y_true, y_pred)],
        )
    )
