"""
Evaluation Functions for Classification Models
"""
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import ConfusionMatrixDisplay
from tqdm import tqdm

from .utils import summarize_evaluation_results
from ..client import log_evaluation_metrics, log_figure, log_test_results
from ..tests.config import Settings
from ..tests.model_evaluation import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    permutation_importance,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
    shap_global_importance,
)

config = Settings()


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


def get_model_metrics(
    model,
    test_set,
    test_preds,
    train_set=None,
    train_preds=None,
    send=True,
    run_cuid=None,
):
    """
    Extract all available (TBD via configuration) model evaluation metrics
    """
    print("Computing model evaluation metrics...")
    x_test, y_test = test_set
    y_pred, class_pred = test_preds

    tests = [
        precision_score,
        recall_score,
        roc_curve,
        confusion_matrix,
        precision_recall_curve,
        permutation_importance,
    ]
    evaluation_metrics = []
    evaluation_plots = []

    # 1) All tests that take y_true, y_pred as input and 2) permutation_importance and shap_global_importance
    with tqdm(total=len(tests) + 1) as pbar:
        for test in tests:
            evaluation_metric_result = test(model, test_set, test_preds)

            if evaluation_metric_result.get("metric", False):
                evaluation_metrics.append(evaluation_metric_result.get("metric"))
            if evaluation_metric_result.get("plot", False):
                evaluation_plots.append(evaluation_metric_result.get("plots"))

            pbar.update(1)

        shap_results = shap_global_importance(model, x_test)
        figures = shap_results.pop("plots")
        evaluation_metrics.append(shap_results)
        pbar.update(1)

    if send:
        print(f"Sending {len(evaluation_metrics)} metrics results to ValidMind...")
        log_evaluation_metrics(evaluation_metrics, run_cuid=run_cuid)

        print(f"Sending {len(figures)} figures to ValidMind...")
        for figure in figures:
            log_figure(figure["figure"], key=figure["key"], metadata=figure["metadata"])

    print("\nSummary of metrics:\n")
    table = summarize_evaluation_results(evaluation_metrics)
    print(table)

    # print("\nPlotting model evaluation results...")
    # cfm_plot = _get_confusion_matrix_plot(evaluation_metrics)
    # cfm_plot.plot()
    # _get_roc_curve_plot(evaluation_metrics_results)
    # _get_pr_curve_plot(evaluation_metrics_results)
    # _get_pfi_plot(evaluation_metrics_results)

    return evaluation_metrics


def evaluate_classification_model(
    model, test_set, train_set=None, send=True, run_cuid=None
):
    """
    Run a suite of model evaluation tests and log their results to the API
    """
    x_test, y_test = test_set

    print("Generating model predictions on test dataset...")
    y_pred = model.predict_proba(x_test)[:, -1]
    # TBD: support class threshold
    class_pred = [round(value) for value in y_pred]

    print("Running evaluation tests...")
    tests_with_test_results = [
        accuracy_score,
        f1_score,
        roc_auc_score,
    ]

    get_model_metrics(
        model, test_set, (y_pred, class_pred), send=send, run_cuid=run_cuid
    )
    evaluation_metrics_results = []
    test_results = []

    # 1) All tests that take y_true, y_pred as input and 2) permutation_importance and shap_global_importance
    with tqdm(total=len(tests_with_test_results)) as pbar:

        for test in tests_with_test_results:
            evaluation_metric_result, test_result = test(
                y_test, y_pred, config=config, class_pred=class_pred
            )
            evaluation_metrics_results.append(evaluation_metric_result)
            test_results.append(test_result)
            pbar.update(1)

    print("\nModel evaluation tests have completed.")
    if send:
        print(f"Sending {len(test_results)} test results to ValidMind...")
        log_test_results(
            test_results,
            run_cuid=run_cuid,
            dataset_type="training",  # TBD: need to support registering test dataset
        )

    return evaluation_metrics_results
