"""
Entrypoint to Model Evaluation API
"""
from .classification import evaluate_classification_model
from .regression import evaluate_regression_model

from ..client import start_run
from ..model_utils import SUPPORTED_MODEL_TYPES


# TODO: rename once we extract metrics to its own function
def evaluate_model(
    model, test_set, train_set=None, eval_opts=None, send=True, run_cuid=None
):
    model_class = model.__class__.__name__

    if model_class not in SUPPORTED_MODEL_TYPES:
        raise ValueError(
            "Model type {} is not supported at the moment.".format(model_class)
        )

    if run_cuid is None:
        run_cuid = start_run()

    # Only supports xgboost classifiers at the moment
    if model_class == "XGBClassifier":
        return evaluate_classification_model(
            model, test_set, train_set, eval_opts, send, run_cuid
        )
    elif model_class == "XGBRegressor" or model_class == "LinearRegression":
        return evaluate_regression_model(
            model, test_set, train_set, eval_opts, send, run_cuid
        )
