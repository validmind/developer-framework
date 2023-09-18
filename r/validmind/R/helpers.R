print_summary_tables <- function(result_summary) {
  tables <- result_summary$serialize(as_df=TRUE)
  for (table in tables) {
    if (!is.null(table$metadata)) {
      print(glue("{table$metadata$title}\n"))
    }
    print(table$data)
  }
}

summarize_metric_result <- function(result) {
  if (result$result_id == "dataset_description") {
    return()
  }

  metric <- result$metric
  print(glue("Results for metric: {metric$key}\n"))
  if (!is.null(metric$summary)) {
    print_summary_tables(metric$summary)
  }
  cat("\n\n")
}

summarize_test_result <- function(result) {
  test_result <- result$test_results
  print(glue("Results for test result: {test_result$test_name}\n"))
  if (!is.null(test_result$summary)) {
    print_summary_tables(test_result$summary)
  }
  cat("\n\n")
}

summarize_result <- function(result) {
  result_class <- class(result)[[1]]

  if (isTRUE(grepl("TestPlanDatasetResult", result_class))) {
    # Ignore for now
    # print("TestPlanDatasetResult")
  } else if (isTRUE(grepl("TestPlanMetricResult", result_class))) {
    summarize_metric_result(result)
  } else if (isTRUE(grepl("TestPlanTestResult", result_class))) {
    summarize_test_result(result)
  }
}

summarize_results <- function(results) {
  for (index in 1:length(results$results)) {
    suite <- results$results[index][[1]]
    print(glue("Test Suite Results: {results$test_plans[index]}\n"))
    for (result in suite) {
      summarize_result(result)
    }
    cat("\n\n")
  }
}

#' Save a model to a given file path
#'
#' @return A numeric vector giving number of characters (code points) in each
#'    element of the character vector. Missing string have missing length.
#' @export
#' @examples
#' my_model <- lm(Sepal.Width ~ Sepal.Length, data = iris)
#' save_model(my_model)
save_model <- function(model) {
    random_name <- paste(sample(letters, 10, replace = TRUE), collapse = "")
    file_path <- paste0("/tmp/", random_name, ".RData")
    save(model, file = file_path)
    return(file_path)
}
