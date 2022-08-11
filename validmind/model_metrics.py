"""
Utility functions for computing metrics for sklearn compatible models
"""
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DEFAULT_REGRESSION_METRICS = [
    "mae",
    "mse",
    "r2",
]


def mae(model, x, y):
    y_pred = model.predict(x)
    return mean_absolute_error(y, y_pred)


def mse(model, x, y):
    y_pred = model.predict(x)
    return mean_squared_error(y, y_pred)


def r2(model, x, y):
    y_pred = model.predict(x)
    return r2_score(y, y_pred)
