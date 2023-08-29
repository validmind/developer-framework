summarize_results <- function(results) {
  for (result in results$results[[1]]) {
    metric <- result$metric
    print(glue("Results for metric: {metric$key}\n"))
    if (!is.null(metric$summary$summarize)) {
      summaries <- result$metric$summary$summarize()
      for (summary in summaries) {
        print.AsIs(summary)
      }
    }
    cat("\n\n")
  }
}

save_model <- function(model) {
    random_name <- paste(sample(letters, 10, replace = TRUE), collapse = "")
    file_path <- paste0("/tmp/", random_name, ".RData")
    save(model, file = file_path)
}