"""
Regression functions from the sklearn interface
"""
from sklearn.metrics import (
    mean_absolute_error as mean_absolute_error_sklearn,
    mean_squared_error as mean_squared_error_sklearn,
    r2_score as r2_score_sklearn,
)

from ....vm_models import Metric, MetricResult


def mae_score(model, test_set, test_preds, train_set, train_preds):
    """
    Compute Mean Absolute Error score metric from sklearn.
    """
    _, y_true = test_set
    y_pred, _ = test_preds

    return MetricResult(
        api_metric=Metric(
            type="evaluation",
            scope="test",
            key="mae",
            value=[mean_absolute_error_sklearn(y_true, y_pred)],
        )
    )


def mse_score(model, test_set, test_preds, train_set, train_preds):
    """
    Compute Mean Squared Error score metric from sklearn.
    """
    _, y_true = test_set
    y_pred, _ = test_preds

    return MetricResult(
        api_metric=Metric(
            type="evaluation",
            scope="test",
            key="mse",
            value=[mean_squared_error_sklearn(y_true, y_pred)],
        )
    )


def r2_score(model, test_set, test_preds, train_set, train_preds):
    """
    Compute R-Squared score metric from sklearn.
    """
    _, y_train_true = train_set
    y_train_pred, _ = train_preds

    _, y_test_true = test_set
    y_test_pred, _ = test_preds

    return [
        MetricResult(
            api_metric=Metric(
                type="evaluation",
                scope="training_dataset",
                key="r2",
                value=[r2_score_sklearn(y_train_true, y_train_pred)],
            )
        ),
        MetricResult(
            api_metric=Metric(
                type="evaluation",
                scope="test",
                key="r2",
                value=[r2_score_sklearn(y_test_true, y_test_pred)],
            )
        ),
    ]


def adjusted_r2_score(model, test_set, test_preds, train_set, train_preds):
    """
    Compute R-Squared score metric from sklearn.
    """
    _, y_train_true = train_set
    y_train_pred, _ = train_preds

    _, y_test_true = test_set
    y_test_pred, _ = test_preds

    adjusted_r2_train = 1 - (
        (1 - r2_score_sklearn(y_train_true, y_train_pred))
        * (len(y_train_true) - 1)
        / (len(y_train_true) - len(model.coef_) - 1)
    )

    adjusted_r2_test = 1 - (1 - r2_score_sklearn(y_test_true, y_test_pred)) * (
        (len(y_test_true) - 1) / (len(y_test_true) - len(model.coef_) - 1)
    )

    return [
        MetricResult(
            api_metric=Metric(
                type="evaluation",
                scope="training_dataset",
                key="adjusted_r2",
                value=[adjusted_r2_train],
            )
        ),
        MetricResult(
            api_metric=Metric(
                type="evaluation",
                scope="test",
                key="adjusted_r2",
                value=[adjusted_r2_test],
            )
        ),
    ]
