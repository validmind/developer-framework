#' Register Test for Custom Metrics Function
#'
#' This function serves as a decorator to convert an R function into a custom metric class
#' compatible with the Python environment, particularly within the context of the `validmind` package.
#' It registers the custom metric using the test ID and relevant attributes such as tasks and tags.
#'
#' @param func Function. The R function to be converted into a custom metric class.
#'
#' @return The original function, after it has been registered as a custom test in the Python environment.
#'
#' @details
#' The `register_test` function takes an R function and performs the following operations:
#' - Converts the function name into a test ID if not provided.
#' - Inspects the function's formal arguments and creates a list of default parameters.
#' - Interacts with the Python environment using `reticulate` to create a corresponding Python class.
#' - Extracts any documentation, tasks, and tags associated with the function.
#' - Registers the custom test in the Python environment using the `test_store` object.
#'
#' The function uses the Python `type` function to dynamically create a metric class with the following properties:
#' - `run`: The method to execute the function.
#' - `required_inputs`: A list of required input arguments.
#' - `default_params`: A list of default parameter values.
#' - `__doc__`: The function's documentation string.
#' - `tasks`: A list of tasks associated with the function.
#' - `tags`: A list of tags associated with the function.
#'
#' @import reticulate
#'
#' @examples
#'
#' \dontrun{
#' ### Calling a Built In Function
#' # Load the validmind package
#' vm_r <- vm(
#'     api_key="<your_api_key_here>",
#'     api_secret="<your_api_secret_here>",
#'     project="<your_project_id_here>",
#'     python_version=python_version,
#'     api_host="https://api.dev.vm.validmind.ai/api/v1/tracking"
#' )
#' 
#' # Run the test function with named inputs
#' vm_raw_dataset = vm_r$init_dataset(
#'     dataset = iris,
#'     input_id = "iris_dataset",
#'     target_column = "Species",
#' )
#' 
#' vm_test = run_test(
#'     test_id = "validmind.data_validation.DescriptiveStatistics",
#'     inputs = list("dataset" = vm_raw_dataset)
#' )
#' 
#' print(vm_test)
#'
#' ### Registering a Custom Function
#' # Example with a more complex function
#' library(ggplot2)
#' library(caret)
#'
#' # Define a function to generate a confusion matrix and plot it
#' confusion_matrix <- function(model, dataset, response_var = "Exited") {
#'   y_true <- as.factor(dataset[[response_var]])
#'   y_pred <- predict(model, dataset)
#'   
#'   y_pred <- as.factor(ifelse(y_pred <= 0, 0, 1))
#'   cm <- confusionMatrix(y_pred, y_true)
#'   
#'   cm_data <- as.data.frame(cm$table)
#'   cm_data$Prediction <- factor(cm_data$Prediction, levels = rev(levels(cm_data$Prediction)))
#'   
#'   p <- ggplot(cm_data, aes(x = Prediction, y = Reference, fill = Freq)) +
#'     geom_tile() +
#'     geom_text(aes(label = Freq), vjust = 1) +
#'     scale_fill_gradient(low = "white", high = "red") +
#'     theme_minimal() +
#'     labs(title = "Confusion Matrix", x = "Predicted", y = "Actual")
#'   
#'   print(p)  # print the plot to display it
#'   
#'   return(p)  # return the ggplot object
#' }
#'
#' result <- register_test(confusion_matrix)
#' print(result)
#' }
#'
#' @export
register_test <- function(func) {
    # Convert the function name to the test_id
    test_id <- paste0("validmind.custom_metrics.", deparse(substitute(func)))
    
    # Inspect the R function's formals (equivalent to Python signature)
    inputs <- formals(func)
    params <- lapply(inputs, function(default_value) {
        list("default" = default_value)
    })
    
    # Use reticulate to access the Python environment
    py_run_string("import inspect")
    
    # Since the function is in R, we'll convert the inputs and params to Python dicts manually
    py_inputs <- reticulate::r_to_py(inputs)
    py_params <- reticulate::r_to_py(params)
    
    # Extract the function description (docstring) in R
    description <- if (!is.null(attr(func, "doc"))) attr(func, "doc") else NULL
    
    # Extract tasks and tags if they exist as attributes on the function
    tasks <- if (!is.null(attr(func, "__tasks__"))) attr(func, "__tasks__") else list()
    tags <- if (!is.null(attr(func, "__tags__"))) attr(func, "__tags__") else list()
    
    # Import the Metric class from the Python environment
    Metric <- reticulate::import("validmind.vm_models", as = "vm")$Metric
    
    # Create the metric_class in R, using the Python `type` function
    metric_class <- reticulate::py$`type`(
        deparse(substitute(func)),
        reticulate::tuple(Metric),
        list(
            "run" = py$`_get_run_method`(func, py_inputs, py_params),
            "required_inputs" = unlist(reticulate::py_to_r(py_inputs$keys())),
            "default_params" = reticulate::py_to_r(lapply(py_params, function(x) x["default"])),
            "__doc__" = description,
            "tasks" = tasks,
            "tags" = tags
        )
    )

    # Access the test_store object from the Python environment
    test_store <- reticulate::import("validmind.tests._store", as = "vm")$test_store
    
    # Register the custom test using reticulate
    test_store$register_custom_test(test_id, metric_class)
    
    return(func)
}
