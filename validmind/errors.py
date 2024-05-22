# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
This module contains all the custom errors that are used in the developer framework.

The following base errors are defined for others:
- BaseError
- APIRequestError
"""
import json


class BaseError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

    def description(self, *args, **kwargs):
        return self.message

    def __str__(self):
        return self.description()


class APIRequestError(BaseError):
    """
    Generic error for API request errors that are not known.
    """

    pass


class GetTestSuiteError(BaseError):
    """
    When the test suite could not be found.
    """

    pass


class MissingCacheResultsArgumentsError(BaseError):
    """
    When the cache_results function is missing arguments.
    """

    pass


class MissingOrInvalidModelPredictFnError(BaseError):
    """
    When the pytorch model is missing a predict function or its predict
    method does not have the expected arguments.
    """

    pass


class InitializeTestSuiteError(BaseError):
    """
    When the test suite was found but could not be initialized.
    """

    pass


class InvalidAPICredentialsError(APIRequestError):
    def description(self, *args, **kwargs):
        return (
            self.message
            or "Invalid API credentials. Please ensure that you have provided the correct values for api_key and api_secret."
        )


class InvalidContentIdPrefixError(APIRequestError):
    """
    When an invalid text content_id is sent to the API.
    """


class InvalidFigureForObjectError(BaseError):
    """
    When a figure was constructed with an unsupported for_object value.
    """

    pass


class InvalidMetricResultsError(APIRequestError):
    """
    When an invalid metric results object is sent to the API.
    """

    pass


class InvalidProjectError(APIRequestError):
    def description(self, *args, **kwargs):
        return (
            self.message
            or "Invalid project ID. Please ensure that you have provided a project ID that belongs to your organization."
        )


class InvalidRequestBodyError(APIRequestError):
    """
    When a POST/PUT request is made with an invalid request body.
    """

    pass


class InvalidTestResultsError(APIRequestError):
    """
    When an invalid test results object is sent to the API.
    """

    pass


class InvalidTestParametersError(BaseError):
    """
    When an invalid parameters for the test.
    """

    pass


class InvalidInputError(BaseError):
    """
    When an invalid input object.
    """

    pass


class InvalidTextObjectError(APIRequestError):
    """
    When an invalid Metadat (Text) object is sent to the API.
    """

    pass


class InvalidValueFormatterError(BaseError):
    """
    When an invalid value formatter is provided when serializing results.
    """

    pass


class InvalidXGBoostTrainedModelError(BaseError):
    """
    When an invalid XGBoost trained model is used when calling init_r_model.
    """

    pass


class LoadTestError(BaseError):
    """
    Exception raised when an error occurs while loading a test
    """

    pass


class MismatchingClassLabelsError(BaseError):
    """
    When the class labels found in the dataset don't match the provided target labels.
    """

    pass


class MissingAPICredentialsError(BaseError):
    def description(self, *args, **kwargs):
        return (
            self.message
            or "API key and secret must be provided either as environment variables or as arguments to init."
        )


class MissingClassLabelError(BaseError):
    """
    When the one or more class labels are missing from provided dataset targets.
    """

    pass


class MissingDocumentationTemplate(BaseError):
    """
    When the client config is missing the documentation template.
    """

    pass


class MissingRequiredTestInputError(BaseError):
    """
    When a required test context variable is missing.
    """

    pass


class MissingRExtrasError(BaseError):
    """
    When the R extras have not been installed.
    """

    def description(self, *args, **kwargs):
        return (
            self.message
            or "ValidMind r-support needs to be installed: `pip install validmind[r-support]`"
        )


class MissingRunCUIDError(APIRequestError):
    """
    When data is being sent to the API but the run_cuid is missing.
    """

    pass


class MissingTextContentIdError(APIRequestError):
    """
    When a Text object is sent to the API without a content_id.
    """

    pass


class MissingTextContentsError(APIRequestError):
    """
    When a Text object is sent to the API without a "text" attribute.
    """

    pass


class MissingProjectIdError(BaseError):
    def description(self, *args, **kwargs):
        return (
            self.message
            or "Project ID must be provided either as an environment variable or as an argument to init."
        )


class StartTestRunFailedError(APIRequestError):
    """
    When the API was not able to start a test run.
    """

    pass


class TestRunNotFoundError(APIRequestError):
    """
    When a test run is not found in the API.
    """

    pass


class TestInputInvalidDatasetError(BaseError):
    """
    When an invalid dataset is used in a test context.
    """

    pass


class UnsupportedColumnTypeError(BaseError):
    """
    When an unsupported column type is found on a dataset.
    """

    pass


class UnsupportedDatasetError(BaseError):
    """
    When an unsupported dataset is used.
    """

    pass


class UnsupportedFigureError(BaseError):
    """
    When an unsupported figure object is constructed.
    """

    pass


class UnsupportedRModelError(BaseError):
    """
    When an unsupported R model is used.
    """

    pass


class UnsupportedModelError(BaseError):
    """
    When an unsupported model is used.
    """

    pass


class UnsupportedModelForSHAPError(BaseError):
    """
    When an unsupported model is used for SHAP importance.
    """

    pass


class SkipTestError(BaseError):
    """
    Useful error to throw when a test cannot be executed.
    """

    pass


def raise_api_error(error_string):
    """
    Safely try to parse JSON from the response message in case the API
    returns a non-JSON string or if the API returns a non-standard error
    """
    try:
        json_response = json.loads(error_string)
        api_code = json_response.get("code")
        api_description = json_response.get("description", json_response.get("message"))
    except json.decoder.JSONDecodeError:
        api_code = "unknown"
        api_description = error_string

    error_map = {
        "invalid_credentials": InvalidAPICredentialsError,
        "invalid_project": InvalidProjectError,
        "invalid_json": InvalidRequestBodyError,
        "missing_content_id": MissingTextContentIdError,
        "missing_text": MissingTextContentsError,
        "invalid_text_object": InvalidTextObjectError,
        "invalid_content_id_prefix": InvalidContentIdPrefixError,
        "missing_run_cuid": MissingRunCUIDError,
        "test_run_not_found": TestRunNotFoundError,
        "invalid_metric_results": InvalidMetricResultsError,
        "invalid_test_results": InvalidTestResultsError,
        "start_test_run_failed": StartTestRunFailedError,
    }

    error_class = error_map.get(api_code, APIRequestError)
    raise error_class(api_description)


def should_raise_on_fail_fast(error) -> bool:
    """
    Determine whether an error should be raised when fail_fast is True.
    """
    error_class = error.__class__.__name__
    return error_class not in [
        "MissingOrInvalidModelPredictFnError",
        "MissingRequiredTestInputError",
        "SkipTestError",
        "UnsupportedModelForSHAPError",
    ]
