"""
Client interface for all data and model validation functions
"""
from .api_client import (
    log_dataset,
    log_model,
    log_training_metrics,
)

from .model_validation import evaluate_model as mod_evaluate_model
from .tests import run_dataset_tests


def analyze_dataset(
    dataset,
    dataset_type,
    dataset_options=None,
    targets=None,
    features=None,
    send=True,
):
    """
    Analyzes a dataset by extracting summary statistics and running data quality tests
    on it. Results are logged to the ValidMind API

    :param pd.DataFrame dataset: We only support Pandas DataFrames at the moment
    :param str dataset_type: The dataset type is necessary for mapping and relating multiple datasets together.
        Can be one of training, validation, test or generic
    :param dict dataset_options: A dictionary of options for the dataset
    :param vm.vm.DatasetTargets targets: A list of target variables
    :param list features: An optional list of extra attributes for any feature
    :param bool send: Whether to post the test results to the API. send=False is useful for testing
    """
    print("Analyzing dataset...")
    vm_dataset = log_dataset(
        dataset,
        dataset_type,
        dataset_options=dataset_options,
        targets=targets,
        features=features,
    )

    print("Running data quality tests...")
    results = run_dataset_tests(
        dataset=dataset,
        dataset_type=dataset_type,
        vm_dataset=vm_dataset,
        send=send,
    )

    return results


def evaluate_model(model, train_set, val_set, test_set, eval_opts=None, send=True):
    """
    Evaluates a model and logs results to the ValidMind API. This function will log information
    about the trained model (parameters, etc.), training metrics, test metrics, and run model
    evaluation tests.

    :param model: The model to evaluate. Only scikit-learn and XGBoost models are supported at the moment
    :param (pd.DataFrame, pd.DataFrame) train_set: (x_train, y_train) tuple
    :param (pd.DataFrame, pd.DataFrame) val_set: (x_val, y_val) tuple
    :param (pd.DataFrame, pd.DataFrame) test_set: (x_test, y_test) tuple
    :param dict eval_opts: A dictionary of options for the model evaluation
    :param bool send: Whether to post the test results to the API. send=False is useful for testing
    """
    print("Logging model metadata and parameters...")
    log_model(model)

    print("Extracting training/validation set metrics from trained model...")
    x_train, y_train = train_set
    x_val, y_val = val_set

    log_training_metrics(
        model, x_train.copy(), y_train.copy(), x_val.copy(), y_val.copy()
    )

    print("Running model evaluation tests...")
    eval_results = mod_evaluate_model(
        model,
        test_set=test_set,
        train_set=train_set,
        eval_opts=eval_opts,
        send=send,
    )

    return eval_results
