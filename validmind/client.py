"""
Client interface for all data and model validation functions
"""

# from .model_validation import evaluate_model as mod_evaluate_model
from .test_plans import get_by_name
from .vm_models import Dataset, Model, ModelAttributes


def init_dataset(
    dataset,
    type="training",
    options=None,
    targets=None,
    target_column=None,
    class_labels=None,
):
    """
    Initializes a VM Dataset, which can then be passed to other functions
    that can perform additional analysis and tests on the data. This function
    also ensures we are reading a valid dataset type. We only support Pandas
    DataFrames at the moment.

    :param pd.DataFrame dataset: We only support Pandas DataFrames at the moment
    :param str type: The dataset split type is necessary for mapping and relating multiple
        datasets together. Can be one of training, validation, test or generic
    :param dict options: A dictionary of options for the dataset
    :param vm.vm.DatasetTargets targets: A list of target variables
    :param str target_column: The name of the target column in the dataset
    :param dict class_labels: A list of class labels for classification problems
    """
    dataset_class = dataset.__class__.__name__

    # TODO: when we accept numpy datasets we can convert them to/from pandas
    if dataset_class == "DataFrame":
        print("Pandas dataset detected. Initializing VM Dataset instance...")
        vm_dataset = Dataset.init_from_pd_dataset(
            dataset, options, targets, target_column, class_labels
        )
    else:
        raise ValueError("Only Pandas datasets are supported at the moment.")

    vm_dataset.type = type

    return vm_dataset


def init_model(model):
    """
    Initializes a VM Model, which can then be passed to other functions
    that can perform additional analysis and tests on the data. This function
    also ensures we are reading a supported model type.

    :param model: A trained model instance
    """

    if not Model.is_supported_model(model):
        raise ValueError(
            "Model type {} is not supported at the moment.".format(
                model.__class__.__name__
            )
        )

    vm_model = Model(model=model, attributes=ModelAttributes())

    return vm_model


def run_test_plan(test_plan_name, send=True, **kwargs):
    """High Level function for running a test plan

    This function provides a high level interface for running a test plan. It removes the need
    to manually initialize a TestPlan instance and run it. This function will automatically
    find the correct test plan class based on the test_plan_name, initialize the test plan, and
    run it.

    :param str test_plan_name: The test plan name (e.g. 'sklearn_classifier')
    :param bool send: Whether to post the test results to the API. send=False is useful for testing
    :param dict kwargs: Additional keyword arguments to pass to the test plan. These will provide
        the TestPlan instance with the necessary context to run the tests. e.g. dataset, model etc.
        See the documentation for the specific test plan for more details.
    """
    try:
        Plan = get_by_name(test_plan_name)
    except ValueError as exc:
        raise ValueError(
            "Error retrieving test plan {}. {}".format(test_plan_name, str(exc))
        )

    try:
        plan = Plan(**kwargs)
    except ValueError as exc:
        raise ValueError(
            "Error initializing test plan {}. {}".format(test_plan_name, str(exc))
        )

    plan.run(send=send)


# def evaluate_model(model, train_set, val_set, test_set, eval_opts=None, send=True):
#     """
#     Evaluates a model and logs results to the ValidMind API. This function will log information
#     about the trained model (parameters, etc.), training metrics, test metrics, and run model
#     evaluation tests.

#     :param model: The model to evaluate. Only scikit-learn and XGBoost models are supported at the moment
#     :param (pd.DataFrame, pd.DataFrame) train_set: (x_train, y_train) tuple
#     :param (pd.DataFrame, pd.DataFrame) val_set: (x_val, y_val) tuple
#     :param (pd.DataFrame, pd.DataFrame) test_set: (x_test, y_test) tuple
#     :param dict eval_opts: A dictionary of options for the model evaluation
#     :param bool send: Whether to post the test results to the API. send=False is useful for testing
#     """
#     print("Logging model metadata and parameters...")
#     log_model(model)

#     print("Extracting training/validation set metrics from trained model...")
#     x_train, y_train = train_set
#     x_val, y_val = val_set

#     log_training_metrics(
#         model, x_train.copy(), y_train.copy(), x_val.copy(), y_val.copy()
#     )

#     print("Running model evaluation tests...")
#     eval_results = mod_evaluate_model(
#         model,
#         test_set=test_set,
#         train_set=train_set,
#         eval_opts=eval_opts,
#         send=send,
#     )

#     return eval_results
