#' Register a Custom Test Function in ValidMind
#'
#' Registers an R function as a custom test within the ValidMind testing framework, allowing it to be used as a metric in model validation.
#'
#' @param func An R function to be registered as a custom test.
#' @param test_id A unique identifier for the test. If \code{NULL}, a default ID is generated based on the function name.
#' @param description A description of the test. If \code{NULL}, the function's \code{description} attribute is used, or "No description" if not available.
#' @param required_inputs A character vector specifying the required inputs for the test. If \code{NULL}, the function's formal argument names are used.
#'
#' @details
#' The function converts the provided R function into a Python callable using \code{\link[reticulate]{r_to_py}}, and then defines a Python class that wraps this callable.
#' This Python class inherits from ValidMind's \code{Metric} class and is registered in ValidMind's test store.
#'
#' The custom test can then be used within ValidMind's testing framework to validate models.
#'
#' @return Invisibly returns \code{NULL}. This function is called for its side effects.
#'
#' @examples
#' \dontrun{
#' # Define a custom test function in R
#' my_custom_metric <- function(predictions, targets) {
#'   # Custom metric logic
#'   mean(abs(predictions - targets))
#' }
#'
#' # Register the custom test
#' register_test(
#'   func = my_custom_metric,
#'   test_id = "custom.mae",
#'   description = "Custom Mean Absolute Error",
#'   required_inputs = c("predictions", "targets")
#' )
#' }
#'
#' @seealso \code{\link[reticulate]{r_to_py}}, \code{\link[reticulate]{import_main}}, \code{\link[reticulate]{py_run_string}}
#'
#' @import reticulate
#' @export
register_test <- function(func, test_id = NULL, description = NULL, required_inputs = NULL) {
    if (is.null(test_id)) {
        test_id <- paste0("validmind.custom_metrics.", deparse(substitute(func)))
    }
    if (is.null(description)) {
        description <- attr(func, "description")
        if (is.null(description)) {
            description <- "No description"
        }
    }
    if (is.null(required_inputs)) {
        required_inputs <- names(formals(func))
    }
    # Convert your R function to a Python callable
    py_func <- r_to_py(func)
    # Access the main Python namespace
    py_main <- import_main()
    py_main$py_func <- py_func
    # Define a Python class that calls your R function
    py_env <- py_run_string("
from validmind.vm_models import Metric
from validmind.tests._store import test_store

class CustomMetric(Metric):
    '''Description'''
    required_inputs = []
    default_params = {}

    def run(self):
        inputs_dict = {key: getattr(self.inputs, key) for key in self.required_inputs}
        return py_func(**inputs_dict)

", convert = TRUE)
    
    # Set attributes of the Python class
    CustomMetric <- py_env$CustomMetric
    CustomMetric$`__doc__` <- description
    CustomMetric$required_inputs <- required_inputs
    
    # Register the custom test
    test_store <- import("validmind.tests._store")$test_store
    test_store$register_custom_test(test_id, CustomMetric)
}
