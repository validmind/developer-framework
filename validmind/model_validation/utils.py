"""
TODO: update to work with test plans

Utils for Model Evaluation
"""
from tabulate import tabulate


def summarize_evaluation_results(results):
    """
    Summarize the results of the model evaluation test suite
    """
    test_results = []

    for result in results:
        for test_result in result.results:
            result_tuples = [(k, v) for k, v in test_result.values.items()]
            scenario = test_result.test_name or "Validation with default Test dataset"
            test_results.append(
                [
                    result.test_name,
                    scenario,
                    result_tuples,
                    test_result.passed,
                ]
            )

    table = tabulate(
        test_results,
        headers=["Test", "Scenario", "Results", "Acceptable"],
        numalign="right",
    )

    return table


def summarize_evaluation_metrics(metrics):
    """
    Summarize the results of the model evaluation test suite
    """
    metrics_rows = []

    for metric in metrics:
        # Not optimal to display confusion matrix or ROC curve inside a table
        if (
            metric.key == "confusion_matrix"
            or metric.key == "roc_curve"
            or metric.key == "pr_curve"
            or metric.key == "pfi"
            or metric.key == "shap"
        ):
            continue

        metrics_rows.append(
            [
                metric.key,
                metric.scope,
                metric.value[0],
            ]
        )

    table = tabulate(
        metrics_rows,
        headers=["Metric", "Scope", "Value"],
        numalign="right",
    )

    return table
