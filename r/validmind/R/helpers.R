#' Retrieve a validmind (vm) object using reticulate
#'
#' @param api_key The ValidMind API key
#' @param api_secret The ValidMind API secret
#' @param project The ValidMind project
#' @param python_version The Python Version to use
#' @param api_host The ValidMind host, defaulting to local
#'
#' @importFrom reticulate import use_python py_config
#'
#' @export
vm <- function(api_key, api_secret, project, python_version,
               api_host = "http://localhost:3000/api/v1/tracking") {
  use_python(python_version)

  vm <- import("validmind")

  vm$init(
    api_host=api_host,
    api_key=api_key,
    api_secret=api_secret,
    project=project
  )

  return(vm)
}

#' Print a summary table
#'
#' @importFrom glue glue
#'
#' @param result_summary A summary of the results
#'
#' @importFrom glue glue
#'
#' @export
print_summary_tables <- function(result_summary) {
  return(result_summary$serialize(as_df=TRUE))
}

#' Provide a summarization of a single metric result
#'
#' @param result The result object
#'
#' @export
summarize_metric_result <- function(result) {
  if (result$result_id == "dataset_description") {
    return(NULL)
  }

  metric <- result$metric

  return(metric$summary)
}

#' Provide a summarization of a single test result
#'
#' @param result The result object
#'
#' @export
summarize_test_result <- function(result) {
  if (result$result_id == "dataset_description") {
    return(NULL)
  }

  metric <- result$test_results

  return(metric$summary)
}

#' Provide a summarization of a single result
#'
#' @param result The result object
#'
#' @export
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

#' Provide a summarization of all results
#'
#' @param results A list of result objects
#'
#' @importFrom dplyr bind_rows
#'
#' @return A numeric vector giving number of characters (code points) in each
#'    element of the character vector. Missing string have missing length.
#' @export
summarize_results <- function(results) {
  # Run the Python function
  result_list <- list()

  for (index in 1:length(results$results)) {
    suite <- results$results[index][[1]]
    print(glue("Test Suite Results: {results$test_plans[index]}\n"))
    for (result in suite) {
      result_list[[length(result_list) + 1]] <- summarize_result(result)
    }
    cat("\n\n")
  }

  i = 0
  my_chunks <- list()
  my_datasets <- list()
  for (result in result_list) {
    for (res in result$results) {
      test <- bind_rows(res$data)

      if (!is.null(test) && nrow(test) > 0) {
        my_datasets[[length(my_datasets) + 1]] <- test
        names(my_datasets)[[length(my_datasets)]] <- res$metadata$title
      }
    }
  }

  return(my_datasets)
}

#' Save a model to a given file path
#'
#' @return A numeric vector giving number of characters (code points) in each
#'    element of the character vector. Missing string have missing length.
#'
#' @param model The model object
#'
#' @export
#'
#' @examples
#' my_model <- lm(Sepal.Width ~ Sepal.Length, data = iris)
#' save_model(my_model)
save_model <- function(model) {
    random_name <- paste(sample(letters, 10, replace = TRUE), collapse = "")
    file_path <- paste0("/tmp/", random_name, ".RData")
    save(model, file = file_path)

    return(file_path)
}

#' Pretty print a list of tables
#'
#' @return The HTML required for nice display of multiple output tables
#'
#' @param datasets The result returned from summarize_results()
#'
#' @importFrom purrr imap
#' @importFrom knitr kable
#' @importFrom kableExtra kable_styling row_spec
#'
#' @export
pretty_print_tables <- function(datasets) {
  imap(datasets, ~{
    kable(.x, caption = .y) %>%
      kable_styling("striped") %>%
      row_spec(0:nrow(.x), color = 'black')
  })
}
