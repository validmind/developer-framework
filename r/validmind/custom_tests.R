#' Run a Test Function with Named Inputs
#'
#' This function allows you to run a specified function with a given set of named inputs. 
#' The function will be executed with the inputs provided, and the results will be returned.
#'
#' @param func A function to be executed. This should be an R function that can be called with the inputs provided.
#' @param inputs A named list of inputs to be passed to the function. The names of the list elements should match 
#'   the argument names expected by the function.
#'
#' @return The result of executing the function with the provided inputs. The return value can be of any type depending 
#'   on the function being executed.
#'
#' @examples
#' # Define a simple function to add two numbers
#' add_numbers <- function(a, b) {
#'   return(a + b)
#' }
#'
#' # Run the test function with named inputs
#' result <- run_test(add_numbers, list(a = 5, b = 3))
#' print(result)  # Should print 8
#'
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
#' # Assuming 'model' is a trained model and 'dataset' is a data frame
#' # Run the test function with the confusion matrix example
#' result <- run_test(confusion_matrix, list(model = model, dataset = dataset, response_var = "Exited"))
#'
#' @export
run_test <- function(func, inputs) {
    # Check if inputs is a named list
    if (!is.list(inputs) || is.null(names(inputs))) {
        stop("Inputs must be a named list.")
    }
    
    # Execute the function with the provided inputs
    result <- do.call(func, inputs)
    
    # Return the result
    return(result)
}
