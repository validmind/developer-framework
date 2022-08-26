"""
Utils for Model Evaluation
"""
from tabulate import tabulate


def summarize_evaluation_results(results):
    """
    Summarize the results of the model evaluation test suite
    """
    test_results = []

    for result in results:
        # Not optimal to display confusion matrix or ROC curve inside a table
        if (
            result["key"] == "confusion_matrix"
            or result["key"] == "roc_curve"
            or result["key"] == "pr_curve"
            or result["key"] == "pfi"
            or result["key"] == "shap"
        ):
            continue

        test_results.append(
            [
                result["key"],
                result["value"][0],
                "Validation with default Test dataset",
            ]
        )

    table = tabulate(
        test_results,
        headers=["Test", "Score", "Scenario"],
        numalign="right",
    )

    return table
