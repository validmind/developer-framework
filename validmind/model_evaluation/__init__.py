"""
Entrypoint to Model Evaluation API
"""
from .classification import evaluate_classification_model
from .regression import evaluate_regression_model

from ..dataset_utils import get_x_and_y
from ..model_utils import SUPPORTED_MODEL_TYPES


def evaluate_model(
    model, test_df, y_test=None, target_column=None, send=True, run_cuid=None
):
    model_class = model.__class__.__name__

    if model_class not in SUPPORTED_MODEL_TYPES:
        raise ValueError(
            "Model type {} is not supported at the moment.".format(model_class)
        )

    if y_test is None and target_column is None:
        raise Exception("Either y_test or target_column must be provided")
    elif target_column is not None and y_test is None:
        x_test, y_test = get_x_and_y(test_df, target_column)
    else:
        x_test = test_df

    # Only supports xgboost classifiers at the moment
    if model_class == "XGBClassifier":
        return evaluate_classification_model(model, x_test, y_test, send, run_cuid)
    elif model_class == "XGBRegressor" or model_class == "LinearRegression":
        return evaluate_regression_model(model, x_test, y_test, send, run_cuid)
