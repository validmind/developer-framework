"""
Entrypoint to any validation test exposed by the SDK
"""
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import ConfusionMatrixDisplay
from tabulate import tabulate
from tqdm import tqdm

from .config import Settings
from .data_quality_pandas import (
    class_imbalance,
    duplicates,
    high_cardinality,
    missing_values,
    pearson_correlation,
    skewness,
    zeros,
)
from .model_evaluation import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    get_x_and_y,
    permutation_importance,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
    shap_global_importance,
)
from ..client import log_evaluation_metrics, log_test_results, start_run, log_figure

config = Settings()


def _summarize_data_quality_results(results):
    """
    Summarize the results of the data quality test suite
    """
    test_results = []
    for result in results:
        num_passed = len([r for r in result.results if r.passed])
        num_failed = len([r for r in result.results if not r.passed])

        percent_passed = (
            1 if len(result.results) == 0 else num_passed / len(result.results)
        )
        test_results.append(
            [
                result.test_name,
                result.passed,
                num_passed,
                num_failed,
                percent_passed * 100,
            ]
        )

    return tabulate(
        test_results,
        headers=["Test", "Passed", "# Passed", "# Errors", "% Passed"],
        numalign="right",
    )


def _get_pfi_plot(results):
    pfi_values = None
    for result in results:
        if result["key"] == "pfi":
            pfi_values = result["value"]
            break

    if pfi_values is None:
        return None

    pfi_bar_values = []
    for feature, values in pfi_values.items():
        pfi_bar_values.append({"feature": feature, "value": values[0][0]})

    pfi_bar_values = sorted(pfi_bar_values, key=lambda d: d["value"], reverse=True)
    pfi_x_values = [d["value"] for d in pfi_bar_values]
    pfi_y_values = [d["feature"] for d in pfi_bar_values]

    # Plot a bar plot with horizontal bars
    _, ax = plt.subplots()
    ax.barh(pfi_y_values, pfi_x_values, color="darkorange")
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")
    ax.set_title("Permutation Feature Importance")
    ax.set_yticks(np.arange(len(pfi_y_values)))
    ax.set_yticklabels(pfi_y_values)
    ax.invert_yaxis()


def _get_roc_curve_plot(results):
    roc_auc_score = None
    roc_curve = None

    for result in results:
        if result["key"] == "roc_curve":
            roc_curve = result["value"]
            continue
        elif result["key"] == "roc_auc":
            roc_auc_score = result["value"]
            continue

    if roc_auc_score is None and roc_curve is None:
        return None

    _, ax = plt.subplots()

    ax.plot(
        roc_curve["fpr"],
        roc_curve["tpr"],
        color="darkorange",
        label="ROC curve (area = %0.2f)" % roc_auc_score[0],
    )
    ax.plot([0, 1], [0, 1], color="navy", linestyle="--")
    ax.axis(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.05)

    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("Receiver operating characteristic example")
    ax.legend(loc="lower right")


def _get_pr_curve_plot(results):
    pr_curve = None

    for result in results:
        if result["key"] == "pr_curve":
            pr_curve = result["value"]
            break

    if pr_curve is None:
        return None

    _, ax = plt.subplots()

    ax.plot(
        pr_curve["recall"],
        pr_curve["precision"],
        color="darkorange",
    )
    ax.axis(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.05)

    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision Recall Curve")


def _get_confusion_matrix_plot(results):
    """
    Get the confusion matrix plot from the results of the model evaluation test suite
    """
    cfm = None
    for result in results:
        if result["key"] == "confusion_matrix":
            cfm = np.asarray(
                [
                    [result["value"]["tn"], result["value"]["fp"]],
                    [result["value"]["fn"], result["value"]["tp"]],
                ]
            )
            break

    if cfm is None:
        return None

    cfm_plot = ConfusionMatrixDisplay(confusion_matrix=cfm)

    return cfm_plot


def _summarize_model_evaluation_results(results):
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


def run_dataset_tests(df, dataset_type, vm_dataset, send=False, run_cuid=None):
    """
    Run all or a subset of tests on the given dataframe. For now we allow this
    function to automatically start a run for us.

    :param pd.DataFrame df: Dataframe for a dataset. Should contain dependent and independent variables
    :param str dataset_type: The dataset type is necessary for mapping and relating multiple datasets together.
        Can be one of training, validation, test or generic
    :param vm_dataset: VM Dataset metadata
    :param bool send: Whether to post the test results to the API. send=False is useful for testing
    """
    print(f'Running data quality tests for "{dataset_type}" dataset...\n')
    if run_cuid is None:
        run_cuid = start_run()

    tests = [
        class_imbalance,
        duplicates,
        high_cardinality,
        missing_values,
        pearson_correlation,
        skewness,
        # unique, # ignore unique for now
        zeros,
    ]
    results = []

    config.target_column = vm_dataset.targets.target_column
    for test in tqdm(tests):
        results.append(test(df, vm_dataset, config))

    print("\nTest suite has completed.")
    if send:
        print("Sending results to ValidMind...")
        log_test_results(results, run_cuid=run_cuid, dataset_type=dataset_type)

    print("\nSummary of results:\n")
    print(_summarize_data_quality_results(results))
    print()

    return results


def run_model_tests(
    model, df, y_test=None, target_column=None, send=False, run_cuid=None
):
    """
    Run a suite of model evaluation tests and log their results to the API
    """
    if y_test is None and target_column is None:
        raise Exception("Either y_test or target_column must be provided")
    elif target_column is not None and y_test is None:
        x_test, y_test = get_x_and_y(df, target_column)
    else:
        x_test = df

    if run_cuid is None:
        run_cuid = start_run()

    print("Generating model predictions on test dataset...")
    y_pred = model.predict_proba(x_test)[:, -1]
    predictions = [round(value) for value in y_pred]

    print("Running evaluation tests...")
    tests_with_test_results = [
        accuracy_score,
        f1_score,
        roc_auc_score,
    ]

    tests = [
        precision_score,
        recall_score,
        roc_curve,
        confusion_matrix,
        precision_recall_curve,
    ]
    evaluation_metrics_results = []
    test_results = []

    # 1) All tests that take y_true, y_pred as input and 2) permutation_importance and shap_global_importance
    with tqdm(total=len(tests) + 1) as pbar:
        for test in tests:
            evaluation_metric_result = test(y_test, y_pred, rounded_y_pred=predictions)
            evaluation_metrics_results.append(evaluation_metric_result)
            pbar.update(1)

        for test in tests_with_test_results:
            evaluation_metric_result, test_result = test(y_test, y_pred, config=config, rounded_y_pred=predictions)
            evaluation_metrics_results.append(evaluation_metric_result)
            test_results.append(test_result)
            pbar.update(1)

        evaluation_metrics_results.append(permutation_importance(model, x_test, y_test))
        pbar.update(1)

        shap_results = shap_global_importance(model, x_test)
        figures = shap_results.pop("plots")
        evaluation_metrics_results.append(shap_results)
        pbar.update(1)

    print("\nModel evaluation tests have completed.")
    if send:
        print(f"Sending {len(evaluation_metrics_results)} metrics results to ValidMind...")
        log_evaluation_metrics(evaluation_metrics_results, run_cuid=run_cuid)

        print(f"Sending {len(test_results)} test results to ValidMind...")
        log_test_results(
            test_results,
            run_cuid=run_cuid,
            dataset_type="test"
        )

        print(f"Sending {len(figures)} figures to ValidMind...")
        for figure in figures:
            log_figure(figure["figure"], key=figure["key"], metadata=figure["metadata"])

    print("\nSummary of results:\n")
    table = _summarize_model_evaluation_results(evaluation_metrics_results)
    print(table)

    print("\nPlotting model evaluation results...")
    cfm_plot = _get_confusion_matrix_plot(evaluation_metrics_results)
    cfm_plot.plot()
    _get_roc_curve_plot(evaluation_metrics_results)
    _get_pr_curve_plot(evaluation_metrics_results)
    _get_pfi_plot(evaluation_metrics_results)

    return evaluation_metrics_results
