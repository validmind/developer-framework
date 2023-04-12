import sys

from dataclasses import dataclass
from typing import ClassVar

from ..vm_models import TestContext, TestContextUtils, TestPlanModelResult

SUPPORTED_STATSMODELS_FAMILIES = {
    "statsmodels.genmod.families.family.Poisson": "poisson",
    "statsmodels.genmod.families.family.Gaussian": "gaussian",
}

SUPPORTED_STATSMODELS_LINK_FUNCTIONS = {
    "statsmodels.genmod.families.links.log": "log",
    "statsmodels.genmod.families.links.identity": "identity",
}


def get_sklearn_version():
    if "sklearn" in sys.modules:
        return sys.modules["sklearn"].__version__

    return "n/a"


def get_statsmodels_version():
    if "statsmodels" in sys.modules:
        return sys.modules["statsmodels"].__version__

    return "n/a"


def get_xgboost_objective(model):
    """
    Attempts to extract the model subtask (binary, multi-class, etc.)
    from the model's objective. Only binary classification is supported
    at the moment
    """
    if model.objective == "binary:logistic":
        return "binary"

    return "n/a"


def get_xgboost_version():
    if "xgboost" in sys.modules:
        return sys.modules["xgboost"].__version__

    return "n/a"


def get_info_from_model_instance(model):
    """
    Attempts to extract all model info from a model object instance
    """
    model_class = model.__class__.__name__

    if model_class == "XGBClassifier":
        architecture = "Extreme Gradient Boosting"
        task = "classification"
        subtask = get_xgboost_objective(model)
        framework = "XGBoost"
        framework_version = get_xgboost_version()
    elif model_class == "XGBRegressor":
        architecture = "Extreme Gradient Boosting"
        task = "regression"
        subtask = "regression"
        framework = "XGBoost"
        framework_version = get_xgboost_version()
    elif model_class == "LogisticRegression":
        architecture = "Linear Regression"
        task = "classification"
        subtask = "binary"
        framework = "Scikit-learn"
        framework_version = get_sklearn_version()
    elif model_class == "LinearRegression":
        architecture = "Ordinary least squares Linear Regression"
        task = "regression"
        subtask = "regression"
        framework = "Scikit-learn"
        framework_version = get_sklearn_version()
    elif model_class == "GLMResultsWrapper":
        architecture = "Generalized Linear Model (GLM)"
        task = "regression"
        subtask = "regression"
        framework = "statsmodels"
        framework_version = get_statsmodels_version()

    return {
        "architecture": architecture,
        "task": task,
        "subtask": subtask,
        "framework": framework,
        "framework_version": framework_version,
    }


def get_statsmodels_model_params(model):
    """
    Extracts the fit() method's parametesr from a
    statsmodels model object instance
    """
    model_instance = model.model
    family_class = model_instance.family.__class__.__name__
    link_class = model_instance.family.link.__class__.__name__

    return {
        "family": SUPPORTED_STATSMODELS_FAMILIES.get(family_class, family_class),
        "link": SUPPORTED_STATSMODELS_LINK_FUNCTIONS.get(link_class, link_class),
        "formula": model_instance.formula,
        "method": model.method,
        "cov_type": model.cov_type,
    }


def get_params_from_model_instance(model):
    """
    Attempts to extract model hyperparameters from a model object instance
    """
    model_class = model.__class__.__name__

    # Only supports xgboot classifiers at the moment
    if model_class == "XGBClassifier" or model_class == "XGBRegressor":
        params = model.get_xgb_params()
    elif model_class == "GLMResultsWrapper":
        params = get_statsmodels_model_params(model)
    # Default to SKLearn models at the moment
    else:
        params = model.get_params()

    return params


@dataclass
class ModelMetadata(TestContextUtils):
    """
    Custom class to collect the following metadata for a model:
    - Model architecture
    - Model hyperparameters
    - Model task type
    """

    # Test Context
    test_context: TestContext

    # Class Variables
    test_type: ClassVar[str] = "ModelMetadata"
    default_params: ClassVar[dict] = {}

    # Instance Variables
    params: dict = None
    name = "model_metadata"
    result: TestPlanModelResult = None

    def __post_init__(self):
        """
        Set default params if not provided
        """
        if self.params is None:
            self.params = self.default_params

    def run(self):
        """
        Just set the model to the result attribute of the test plan result
        and it will be logged via the `log_model` function
        """
        trained_model = self.model.model
        model_info = get_info_from_model_instance(trained_model)

        if self.model.task is None:
            self.model.task = model_info["task"]
        if self.model.subtask is None:
            self.model.subtask = model_info["subtask"]
        if self.model.attributes.framework is None:
            self.model.attributes.framework = model_info["framework"]
        if self.model.attributes.framework_version is None:
            self.model.attributes.framework_version = model_info["framework_version"]
        if self.model.attributes.architecture is None:
            self.model.attributes.architecture = model_info["architecture"]

        self.model.params = get_params_from_model_instance(trained_model)
        self.result = TestPlanModelResult(model=self.model)

        return self.result
