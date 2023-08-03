# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Client interface for all data and model validation functions
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.linear_model import LinearRegression, LogisticRegression

from .client_config import client_config
from .errors import (
    GetTestPlanError,
    GetTestSuiteError,
    InitializeTestPlanError,
    InitializeTestSuiteError,
    InvalidXGBoostTrainedModelError,
    MissingDocumentationTemplate,
    MissingRExtrasError,
    UnsupportedDatasetError,
    UnsupportedRModelError,
    UnsupportedModelError,
)
from .logging import get_logger
from .template import (
    get_template_test_suite,
    preview_template as _preview_template,
    run_template as _run_template,
)
from .test_plans import get_by_id as get_test_plan_by_id
from .test_suites import get_by_id as get_test_suite_by_id

from .vm_models import (
    Model,
    ModelAttributes,
    R_MODEL_TYPES,
    TestPlan,
    TestSuite,
)
from .vm_models.dataset import (
    VMDataset,
    NumpyDataset,
    DataFrameDataset,
    TorchDataset,
)

pd.option_context("format.precision", 2)

logger = get_logger(__name__)


def init_dataset(
    dataset,
    index=None,
    index_name: str = None,
    column_names: list = None,
    options: dict = None,
    text_column: str = None,
    target_column: str = None,
    class_labels: dict = None,
    type: str = None,
) -> VMDataset:
    """
    Initializes a VM Dataset, which can then be passed to other functions
    that can perform additional analysis and tests on the data. This function
    also ensures we are reading a valid dataset type. We only support Pandas
    DataFrames at the moment.

    Args:
        dataset (pd.DataFrame): We only support Pandas DataFrames at the moment
        options (dict): A dictionary of options for the dataset
        targets (vm.vm.DatasetTargets): A list of target variables
        target_column (str): The name of the target column in the dataset
        class_labels (dict): A list of class labels for classification problems

    Raises:
        ValueError: If the dataset type is not supported

    Returns:
        vm.vm.Dataset: A VM Dataset instance
    """
    # Show deprecation notice if type is passed
    if type is not None:
        logger.info(
            "The 'type' argument to init_dataset() argument is deprecated and no longer required."
        )

    dataset_class = dataset.__class__.__name__
    # Instantiate supported dataset types here
    if dataset_class == "DataFrame":
        logger.info("Pandas dataset detected. Initializing VM Dataset instance...")
        vm_dataset = DataFrameDataset(
            raw_dataset=dataset,
            target_column=target_column,
            text_column=text_column,
            target_class_labels=class_labels,
        )
    elif dataset_class == "ndarray":
        logger.info("Numpy ndarray detected. Initializing VM Dataset instance...")
        vm_dataset = NumpyDataset(
            raw_dataset=dataset,
            index=index,
            index_name=index_name,
            column_names=column_names,
            target_column=target_column,
            text_column=text_column,
            target_class_labels=class_labels,
        )
    elif dataset_class == "TensorDataset":
        logger.info("Torch TensorDataset detected. Initializing VM Dataset instance...")
        vm_dataset = TorchDataset(
            raw_dataset=dataset,
            index=index,
            index_name=index_name,
            column_names=column_names,
            target_column=target_column,
            text_column=text_column,
            target_class_labels=class_labels,
        )
    else:
        raise UnsupportedDatasetError(
            "Only Pandas datasets and Tensor Datasets are supported at the moment."
        )

    return vm_dataset


def init_model(
    model: object,
    train_ds: VMDataset = None,
    test_ds: VMDataset = None,
    validation_ds: VMDataset = None,
) -> Model:
    """
    Initializes a VM Model, which can then be passed to other functions
    that can perform additional analysis and tests on the data. This function
    also ensures we are reading a supported model type.

    Args:
        model: A trained sklearn model

    Raises:
        ValueError: If the model type is not supported

    Returns:
        vm.vm.Model: A VM Model instance
    """

    if not Model.is_supported_model(model):
        raise UnsupportedModelError(
            f"Model type {Model.model_library(model)}.{Model.model_class(model)} is not supported at the moment."
        )

    return Model.init_vm_model(
        model, train_ds, test_ds, validation_ds, attributes=ModelAttributes()
    )


def init_r_model(model_path: str, model_type: str) -> Model:
    """
    Initializes a VM Model for an R model

    R models must be saved to disk and the filetype depends on the model type...
    Currently we support the following model types:

    - LogisticRegression `glm` model in R: saved as an RDS file with `saveRDS`
    - LinearRegression `lm` model in R: saved as an RDS file with `saveRDS`
    - XGBClassifier: saved as a .json or .bin file with `xgb.save`
    - XGBRegressor: saved as a .json or .bin file with `xgb.save`

    LogisticRegression and LinearRegression models are converted to sklearn models by extracting
    the coefficients and intercept from the R model. XGB models are loaded using the xgboost
    since xgb models saved in .json or .bin format can be loaded directly with either Python or R

    Args:
        model_path (str): The path to the R model saved as an RDS or XGB file
        model_type (str): The type of the model (one of R_MODEL_TYPES)

    Returns:
        vm.vm.Model: A VM Model instance
    """
    # first we need to load the model using rpy2
    # since rpy2 is an extra we need to conditionally import it
    try:
        import rpy2.robjects as robjects
    except ImportError:
        raise MissingRExtrasError()

    if model_type not in R_MODEL_TYPES:
        raise UnsupportedRModelError(
            "model_type must be one of {}. Got {}".format(R_MODEL_TYPES, model_type)
        )

    # convert the R model to an sklearn or xgboost estimator
    if model_type == "LogisticRegression":  # load the model
        r_model = robjects.r["readRDS"](model_path)
        intercept, *coefficients = robjects.r["coef"](r_model)

        model = LogisticRegression()
        model.intercept_ = intercept
        model.coef_ = np.array(coefficients).reshape(1, -1)
        model.classes_ = np.array([0, 1])
        model.feature_names_in_ = np.array(
            robjects.r["colnames"](robjects.r["model.matrix"](r_model))[1:]
        )

    elif model_type == "LinearRegression":
        r_model = robjects.r["readRDS"](model_path)
        intercept, *coefficients = robjects.r["coef"](r_model)

        model = LinearRegression()
        model.intercept_ = intercept
        model.coef_ = np.array(coefficients).reshape(1, -1)

    elif model_type == "XGBClassifier" or model_type == "XGBRegressor":
        # validate that path is a .json or .bin file not .rds
        if not model_path.endswith(".json") and not model_path.endswith(".bin"):
            raise InvalidXGBoostTrainedModelError(
                "XGBoost models must be a .json or .bin file. Got {}".format(model_path)
                + "Please use `xgb.save(model, 'model.json')` to save the model."
            )

        booster = xgb.Booster(model_file=model_path)

        model = (
            xgb.XGBClassifier() if model_type == "XGBClassifier" else xgb.XGBRegressor()
        )
        model._Booster = booster

    return init_model(model)


def run_test_plan(test_plan_name, send=True, **kwargs):
    """High Level function for running a test plan

    This function provides a high level interface for running a test plan. It removes the need
    to manually initialize a TestPlan instance and run it. This function will automatically
    find the correct test plan class based on the test_plan_name, initialize the test plan, and
    run it.

    Args:
        test_plan_name (str): The test plan name (e.g. 'binary_classifier')
        send (bool, optional): Whether to post the test results to the API. send=False is useful for testing. Defaults to True.
        **kwargs: Additional keyword arguments to pass to the test plan. These will provide
            the TestPlan instance with the necessary context to run the tests. e.g. dataset, model etc.
            See the documentation for the specific test plan for more details.

    Raises:
        ValueError: If the test plan name is not found or if there is an error initializing the test plan

    Returns:
        dict: A dictionary of test results
    """
    try:
        Plan: TestPlan = get_test_plan_by_id(test_plan_name)
    except ValueError as exc:
        raise GetTestPlanError(
            "Error retrieving test plan {}. {}".format(test_plan_name, str(exc))
        )

    try:
        plan = Plan(**kwargs)
    except ValueError as exc:
        raise InitializeTestPlanError(
            "Error initializing test plan {}. {}".format(test_plan_name, str(exc))
        )

    plan.run(send=send)

    return plan


def get_test_suite(
    test_suite_name: str = None,
    section: str = None,
    *args,
    **kwargs,
) -> TestSuite:
    """Gets a TestSuite object for the current project or a specific test suite

    This function provides an interface to retrieve the TestSuite instance for the
    current project or a specific TestSuite instance identified by test_suite_name.
    The project Test Suite will contain Test Plans for every section in the project's
    documentation template and these Test Plans will contain all the tests associated
    with that section.

    Args:
        test_suite_name (str, optional): The test suite name. If not passed, then the
            project's test suite will be returned. Defaults to None.
        section (str, optional): The section of the documentation template from which
            to retrieve the test suite. This only applies if test_suite_name is None.
            Defaults to None.
        args: Additional arguments to pass to the TestSuite
        kwargs: Additional keyword arguments to pass to the TestSuite
    """
    if test_suite_name is None:
        return get_template_test_suite(
            client_config.documentation_template,
            section=section,
            *args,
            **kwargs,
        )

    return get_test_suite_by_id(test_suite_name)(*args, **kwargs)


def run_test_suite(test_suite_name, send=True, **kwargs):
    """High Level function for running a test suite

    This function provides a high level interface for running a test suite. A test suite is
    a collection of test plans. This function will automatically find the correct test suite
    class based on the test_suite_name, initialize each of the test plans, and run them.

    Args:
        test_suite_name (str): The test suite name (e.g. 'binary_classifier_full_suite')
        send (bool, optional): Whether to post the test results to the API. send=False is useful for testing. Defaults to True.
        **kwargs: Additional keyword arguments to pass to the test suite. These will provide
            the TestSuite instance with the necessary context to run the tests. e.g. dataset, model etc.
            See the documentation for the specific test plan, metric or threshold test for more details.

    Raises:
        ValueError: If the test suite name is not found or if there is an error initializing the test suite

    Returns:
        TestSuite: the TestSuite instance
    """
    try:
        Suite: TestSuite = get_test_suite_by_id(test_suite_name)
    except ValueError as exc:
        raise GetTestSuiteError(
            "Error retrieving test suite {}. {}".format(test_suite_name, str(exc))
        )

    try:
        suite = Suite(**kwargs)
    except ValueError as exc:
        raise InitializeTestSuiteError(
            "Error initializing test suite {}. {}".format(test_suite_name, str(exc))
        )

    suite.run(send=send)

    return suite


def preview_template():
    """Preview the documentation template for the current project

    This function will display the documentation template for the current project. If
    the project has not been initialized, then an error will be raised.

    Raises:
        ValueError: If the project has not been initialized
    """
    if client_config.documentation_template is None:
        raise MissingDocumentationTemplate(
            "No documentation template found. Please run `vm.init()`"
        )

    _preview_template(client_config.documentation_template)


def run_documentation_tests(section: str = None, *args, **kwargs):
    """Collect and run all the tests associated with a template

    This function will analyze the current project's documentation template and collect
    all the tests associated with it into a test suite. It will then run the test
    suite, log the results to the ValidMind API and display them to the user.

    Args:
        section (str, optional): The section to preview. Defaults to None.
        *args: Arguments to pass to the TestSuite
        **kwargs: Keyword arguments to pass to the TestSuite

    Raises:
        ValueError: If the project has not been initialized
    """
    if client_config.documentation_template is None:
        raise MissingDocumentationTemplate(
            "No documentation template found. Please run `vm.init()`"
        )

    _run_template(
        template=client_config.documentation_template,
        section=section,
        *args,
        **kwargs,
    )


def run_template(*args, **kwargs):
    """DEPRECATED! Use `vm.run_documentation_tests` instead.

    _run_template(
        template=client_config.documentation_template,
        section=section,
        *args,
        **kwargs,
    )

    Collect and run all the tests associated with a template

    This function will analyze the current project's documentation template and collect
    all the tests associated with it into a test suite. It will then run the test
    suite, log the results to the ValidMind API and display them to the user.

    Args:
        *args: Arguments to pass to the TestSuite
        **kwargs: Keyword arguments to pass to the TestSuite

    Raises:
        ValueError: If the project has not been initialized
    """
    logger.warning(
        "`vm.run_template` is deprecated. "
        "Please use `vm.run_documentation_tests` instead"
    )
    run_documentation_tests(section=None, *args, **kwargs)
