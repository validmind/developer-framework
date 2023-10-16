# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Client interface for all data and model validation functions
"""

import pandas as pd

from .client_config import client_config
from .errors import (
    GetTestSuiteError,
    InitializeTestSuiteError,
    MissingDocumentationTemplate,
    MissingRExtrasError,
    UnsupportedDatasetError,
    UnsupportedModelError,
)
from .logging import get_logger
from .models.r_model import RModel
from .template import get_template_test_suite
from .template import preview_template as _preview_template
from .template import run_template as _run_template
from .test_suites import get_by_id as get_test_suite_by_id
from .vm_models import TestContext, TestSuite, TestSuiteRunner
from .vm_models.dataset import DataFrameDataset, NumpyDataset, TorchDataset, VMDataset
from .vm_models.model import VMModel, get_model_class

pd.option_context("format.precision", 2)

logger = get_logger(__name__)


def init_dataset(
    dataset,
    index=None,
    index_name: str = None,
    date_time_index: bool = False,
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
            date_time_index=date_time_index,
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
            date_time_index=date_time_index,
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
) -> VMModel:
    """
    Initializes a VM Model, which can then be passed to other functions
    that can perform additional analysis and tests on the data. This function
    also ensures we are creating a model supported libraries.

    Args:
        model: A trained model

    Raises:
        ValueError: If the model type is not supported

    Returns:
        vm.VMModel: A VM Model instance
    """
    class_obj = get_model_class(model=model)
    if not class_obj:
        raise UnsupportedModelError(
            f"Model type {class_obj} is not supported at the moment."
        )

    vm_model = class_obj(
        model=model,  # Trained model instance
        train_ds=train_ds,
        test_ds=test_ds,
        validation_ds=validation_ds,
        attributes=None,
    )
    return vm_model


def init_r_model(
    model_path: str,
    train_ds: VMDataset = None,
    test_ds: VMDataset = None,
    validation_ds: VMDataset = None,
) -> VMModel:
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

    # TODO: proper check for supported models
    #
    # if model.get("method") not in R_MODEL_METHODS:
    #     raise UnsupportedRModelError(
    #         "R model method must be one of {}. Got {}".format(
    #             R_MODEL_METHODS, model.get("method")
    #         )
    #     )

    # first we need to load the model using rpy2
    # since rpy2 is an extra we need to conditionally import it
    try:
        import rpy2.robjects as robjects
    except ImportError:
        raise MissingRExtrasError()

    r = robjects.r
    loaded_objects = r.load(model_path)
    model_name = loaded_objects[0]
    model = r[model_name]

    vm_model = RModel(
        r=r,
        model=model,
        train_ds=train_ds,
        test_ds=test_ds,
        validation_ds=validation_ds,
    )

    return vm_model


def run_test_plan(test_plan_name, send=True, fail_fast=False, **kwargs):
    """DEPRECATED! Use `vm.run_test_suite` instead."""
    logger.warning(
        "`vm.run_test_plan` is deprecated. Please use `vm.run_test_suite` instead"
    )
    return run_test_suite(
        test_suite_id=test_plan_name,
        send=send,
        fail_fast=fail_fast,
        **kwargs,
    )


def get_test_suite(
    test_suite_id: str = None,
    section: str = None,
    *args,
    **kwargs,
) -> TestSuite:
    """Gets a TestSuite object for the current project or a specific test suite

    This function provides an interface to retrieve the TestSuite instance for the
    current project or a specific TestSuite instance identified by test_suite_id.
    The project Test Suite will contain sections for every section in the project's
    documentation template and these Test Suite Sections will contain all the tests
    associated with that template section.

    Args:
        test_suite_id (str, optional): The test suite name. If not passed, then the
            project's test suite will be returned. Defaults to None.
        section (str, optional): The section of the documentation template from which
            to retrieve the test suite. This only applies if test_suite_id is None.
            Defaults to None.
        args: Additional arguments to pass to the TestSuite
        kwargs: Additional keyword arguments to pass to the TestSuite
    """
    if test_suite_id is None:
        if client_config.documentation_template is None:
            raise MissingDocumentationTemplate(
                "No documentation template found. Please run `vm.init()`"
            )

        return get_template_test_suite(
            client_config.documentation_template,
            section=section,
            *args,
            **kwargs,
        )

    return get_test_suite_by_id(test_suite_id)(*args, **kwargs)


def run_test_suite(test_suite_id, send=True, fail_fast=False, config=None, **kwargs):
    """High Level function for running a test suite

    This function provides a high level interface for running a test suite. A test suite is
    a collection of tests. This function will automatically find the correct test suite
    class based on the test_suite_id, initialize each of the tests, and run them.

    Args:
        test_suite_id (str): The test suite name (e.g. 'classifier_full_suite')
        config (dict, optional): A dictionary of parameters to pass to the tests in the
            test suite. Defaults to None.
        send (bool, optional): Whether to post the test results to the API. send=False
            is useful for testing. Defaults to True.
        fail_fast (bool, optional): Whether to stop running tests after the first failure. Defaults to False.
        **kwargs: Additional keyword arguments to pass to the test suite. These will provide
            the TestSuite instance with the necessary context to run the tests. e.g. dataset, model etc.
            See the documentation for the specific metric or threshold test for more details.

    Raises:
        ValueError: If the test suite name is not found or if there is an error initializing the test suite

    Returns:
        TestSuite: the TestSuite instance
    """
    try:
        Suite: TestSuite = get_test_suite_by_id(test_suite_id)
    except ValueError as exc:
        raise GetTestSuiteError(
            "Error retrieving test suite {}. {}".format(test_suite_id, str(exc))
        )

    try:
        suite = Suite()
    except ValueError as exc:
        raise InitializeTestSuiteError(
            "Error initializing test suite {}. {}".format(test_suite_id, str(exc))
        )

    TestSuiteRunner(
        suite=suite,
        context=TestContext(**kwargs),
        config=config or {},
    ).run(fail_fast=fail_fast, send=send)

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


def run_documentation_tests(section: str = None, send=True, fail_fast=False, **kwargs):
    """Collect and run all the tests associated with a template

    This function will analyze the current project's documentation template and collect
    all the tests associated with it into a test suite. It will then run the test
    suite, log the results to the ValidMind API and display them to the user.

    Args:
        section (str, optional): The section to preview. Defaults to None.
        send (bool, optional): Whether to send the results to the ValidMind API. Defaults to True.
        fail_fast (bool, optional): Whether to stop running tests after the first failure. Defaults to False.
        **kwargs: Keyword arguments to pass to the TestSuite

    Returns:
        TestSuite: The completed TestSuite instance

    Raises:
        ValueError: If the project has not been initialized
    """
    if client_config.documentation_template is None:
        raise MissingDocumentationTemplate(
            "No documentation template found. Please run `vm.init()`"
        )

    return _run_template(
        template=client_config.documentation_template,
        section=section,
        send=send,
        fail_fast=fail_fast,
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
