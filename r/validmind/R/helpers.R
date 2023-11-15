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

  if (isTRUE(grepl("TestSuiteDatasetResult", result_class))) {
    # Ignore for now
    # print("TestPlanDatasetResult")
  } else if (isTRUE(grepl("TestSuiteMetricResult", result_class))) {
    summarize_metric_result(result)
  } else if (isTRUE(grepl("TestSuiteTestResult", result_class))) {
    summarize_test_result(result)
  }
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


#' From
#'
#' @return The HTML required for nice display of multiple output tables
#'
#' @param plotly_figure The result returned from summarize_result()
#'
#' @importFrom plotly plotly_build
#'
#' @export
build_r_plotly <- function(plotly_figure) {
  # Grab the plotly code as a list
  fig_list <- plotly_figure$figure$to_dict()

  # Extract data and layout
  p <- plotly_build(fig_list)

  # Return the R plotly plot
  return(p)
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
process_result <- function(results) {

  overall_result <- list()

  # Sequentially process every result in the result set
  for (index in 1:length(results$sections)) {
    # Grab the test suite
    suite <- results$sections[[index]]
    overall_result[[suite$section_id]] <- list()

    # Grab the individual test
    # print(glue("Test Suite Results: {suite$section_id}\n"))

    # Get path to temporary directory
    tmp_dir <- tempdir()

    # Process every result in that particular suite
    for (full_result in suite$tests) {
      if (!("title" %in% names(full_result))) full_result$title <- full_result$name
      # print(full_result$title)

      overall_result[[suite$section_id]][[full_result$title]] <- list()

      # Store a list of the possible results we will display
      plotly_images <- list()
      matplotlib_images <- list()
      result_tables <- list()

      result <- full_result$result
      description <- result$result_metadata[[1]]$text

      # Summarize the tables
      if ("metric" %in% names(result)) {
        if (!is.null(result$metric$summary)) {
          table_res <- result$metric$summary$results
          for (tbl in table_res) {
            try({
              result_tables[[length(result_tables) + 1]] <- bind_rows(tbl$data)
            }, silent = TRUE)
          }
        }
      }

      # Process and bind together all the summarized tabular results
      if ("test_results" %in% names(result)) {
        try({
          table_res <- result$test_results$results

          full_table <- list()
          for (res in table_res) {
              my_tbl <- try({
                bind_rows(c(list("Column" = res$column), res$values))
              }, silent = TRUE)

              if (inherits(my_tbl, "try-error")) {
                my_tbl <- bind_rows(res$values)
              }

              full_table[[length(full_table) + 1]] <- my_tbl
          }

          full_table <- bind_rows(full_table)

          if (!is.null(full_table) && nrow(full_table) > 0) {
            result_tables[[length(result_tables) + 1]] <- full_table
          }
        }, silent = TRUE)
      }

      # Check if we actually have figures to process
      if ("figures" %in% names(result)) {

        # Process each figure one by one
        for (figure in result$figures) {

          # First check if it's a plotly figure
          if (figure$is_plotly_figure()) {
            plotly_images[[length(plotly_images) + 1]] <- build_r_plotly(figure)
          # Otherwise, it's a matplotlib figure
          } else if (figure$is_matplotlib_figure()) {

            # Original name
            orig_name <- figure$metadata$`_name`
            full_path <- file.path(tmp_dir, paste0(orig_name, ".png"))

            # Store if we haven't yet
            if (!(full_path %in% unlist(matplotlib_images))) {
              figure$figure$savefig(full_path)

              matplotlib_images[[length(matplotlib_images) + 1]] <- full_path
            }
          }
        }
      }

      final_result <- list(description = description,
                           plotly_images = plotly_images,
                           matplotlib_images = matplotlib_images,
                           result_tables = result_tables)

      overall_result[[suite$section_id]][[full_result$title]] <- final_result
    }
  }

  return(overall_result)
}

#' Produce RMarkdown-compatible output of all results
#'
#' @param processed_results A list of processed result objects
#'
#' @importFrom dplyr %>%
#' @importFrom base64enc dataURI
#' @importFrom htmltools div HTML tags
#' @importFrom DT datatable
#'
#' @return A formatted rmarkdown
#' @export
display_report <- function(processed_results) {
  all_widgets <- list()

  for (section in names(processed_results)) {
    test_suites <- processed_results[[section]]
    for (suite in names(test_suites)) {
      # Create a temporary file for the markdown content
      temp_markdown_file <- tempfile(fileext = ".md")
      orig_text <- processed_results[[section]][[suite]]$description
      text_to_write <- glue(paste0("### {suite}\n\n", orig_text), "\n\n")
      widget_list <- list()

      if (is.character(orig_text)) {
        # Write the markdown string to the temporary file
        writeLines(text_to_write, temp_markdown_file)

        # Convert markdown to HTML
        temp_html_file <- tempfile(fileext = ".html")
        rmarkdown::pandoc_convert(
          input = temp_markdown_file,
          to = "html",
          output = temp_html_file
        )

        # Read the HTML content
        html_content <- readLines(temp_html_file, warn = FALSE)
        html_content <- paste(html_content, collapse = "\n")

        # Create a single widget
        widget_list <- list(description = div(style="color: black;", HTML(html_content)))
      }

      for (t1 in processed_results[[section]][[suite]]$result_tables) {
        widget_list[[length(widget_list) + 1]] <- datatable(t1)
      }

      for (p in processed_results[[section]][[suite]]$plotly_images) {
        res <- try(capture.output(print(p)), silent = TRUE)

        if (!inherits(res, "try-error")) {
          widget_list[[length(widget_list) + 1]] <- p
        }
      }

      res = unlist(processed_results[[section]][[suite]]$matplotlib_images)

      if (!is.null(res)) {
        for (im in res) {
          img_data <- dataURI(file = im, mime = "image/png")

          img_tag <- tags$img(src = img_data,
                              alt = "Description of image",
                              width = "100%", height = "auto")

          widget_list[[length(widget_list) + 1]] <- img_tag
        }
      }

      if (length(widget_list) > 0) {
        combined_widget <- do.call(htmltools::tagList, widget_list)
        class(combined_widget) <- c(suite, section, "shiny.tag.list")

        # print(combined_widget)
        all_widgets[[length(all_widgets) + 1]] <- combined_widget
      }
    }
  }

  return(all_widgets)
}
