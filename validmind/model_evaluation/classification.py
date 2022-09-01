"""
Evaluation Functions for Classification Models
"""
import matplotlib.pyplot as plt

from IPython.display import display
from tqdm import tqdm

from .utils import summarize_evaluation_metrics, summarize_evaluation_results
from ..client import log_metrics, log_figure, log_test_results
from ..metrics.classification import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from ..metrics.generic import (
    permutation_importance,
    shap_global_importance,
)
from ..tests.config import Settings
from ..tests.model_evaluation import (
    base_accuracy_test,
    base_f1_score_test,
    base_roc_auc_score_test,
    training_better_than_test,
    training_test_degradation_test,
)
from ..utils import is_notebook

config = Settings()

DEFAULT_DECISION_THRESHOLD = 0.5


# TODO: same function as classification and regression, refactor
# TODO: refactor this function since C901 means it's too complex
def get_model_metrics(  # noqa: C901
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

    metrics = [
        accuracy_score,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
        roc_curve,
        confusion_matrix,
        precision_recall_curve,
        permutation_importance,
        shap_global_importance,
    ]
    evaluation_metrics = []
    evaluation_figures = []
    report_figures = []

    plt.ioff()

    with tqdm(total=len(metrics)) as pbar:
        for metric_fn in metrics:
            evaluation_metric_result = metric_fn(model, test_set, test_preds)

            if evaluation_metric_result.api_metric:
                evaluation_metrics.append(evaluation_metric_result.api_metric)

            if evaluation_metric_result.api_figures:
                evaluation_figures.extend(evaluation_metric_result.api_figures)
                # extract plots from "figure" key on each api_figure so
                # we can also display the figures that are going to be
                # sent to the ValidMind API
                for api_figure in evaluation_metric_result.api_figures:
                    report_figures.append(api_figure.figure)

            if evaluation_metric_result.plots:
                report_figures.extend(evaluation_metric_result.plots)

            pbar.update(1)

    if send:
        print(f"Sending {len(evaluation_metrics)} metrics results to ValidMind...")
        log_metrics(evaluation_metrics, run_cuid=run_cuid)

        print(f"Sending {len(evaluation_figures)} figures to ValidMind...")
        for figure in evaluation_figures:
            log_figure(figure.figure, key=figure.key, metadata=figure.metadata)

    print("\nSummary of metrics:\n")
    table = summarize_evaluation_metrics(evaluation_metrics)
    print(table)

    if len(report_figures) and is_notebook():
        print("\nPlotting model evaluation metrics...")

        for figure in report_figures:
            if hasattr(figure, "canvas"):
                display(figure)
            elif hasattr(figure, "plot"):
                figure.plot()
                plt.show()

    return evaluation_metrics


def run_model_tests(
    model,
    test_set,
    test_preds,
    train_set=None,
    train_preds=None,
    send=True,
    run_cuid=None,
):
    """
    Run all available (TBD via configuration) model tests
    """
    print("Running evaluation tests...")
    tests = [
        base_accuracy_test,
        base_f1_score_test,
        base_roc_auc_score_test,
        training_better_than_test,
        training_test_degradation_test,
    ]

    test_results = []

    # 1) All tests that take y_true, y_pred as input and 2) permutation_importance and shap_global_importance
    with tqdm(total=len(tests)) as pbar:
        for test in tests:
            test_result = test(
                model,
                test_set,
                test_preds,
                train_set=train_set,
                train_preds=train_preds,
                config=config,
            )
            if test_result:
                test_results.append(test_result)

            pbar.update(1)

    print("\nModel evaluation tests have completed.")
    if send:
        print(f"Sending {len(test_results)} test results to ValidMind...")
        log_test_results(
            test_results,
            run_cuid=run_cuid,
            # TBD: test results can be associated with anything but right now we're
            # requiring a dataset_type on the API
            dataset_type="training",
        )

    print("\nSummary of evaluation tests:\n")
    table = summarize_evaluation_results(test_results)
    print(table)

    return test_results


def evaluate_classification_model(
    model, test_set, train_set=None, eval_opts=None, send=True, run_cuid=None
):
    """
    Run a suite of model evaluation tests and log their results to the API
    """
    decision_threshold = (
        eval_opts and eval_opts.get("decision_threshold", DEFAULT_DECISION_THRESHOLD)
    ) or DEFAULT_DECISION_THRESHOLD

    x_test, _ = test_set

    print("Generating model predictions on test dataset...")
    y_pred = model.predict_proba(x_test)[:, -1]

    if decision_threshold != DEFAULT_DECISION_THRESHOLD:
        print(f"Using custom decision threshold for evaluation: {decision_threshold}")
    else:
        print("Using default decision threshold for evaluation: 0.5")

    class_pred = (y_pred > decision_threshold).astype(int)

    y_train_pred = None
    train_class_pred = None

    if train_set is not None:
        x_train, _ = train_set
        print("Generating model predictions on training dataset...")
        y_train_pred = model.predict_proba(x_train)[:, -1]
        train_class_pred = (y_train_pred > decision_threshold).astype(int)

    results = []
    results.extend(
        get_model_metrics(
            model,
            test_set,
            test_preds=(y_pred, class_pred),
            train_set=train_set,
            train_preds=(y_train_pred, train_class_pred),
            send=send,
            run_cuid=run_cuid,
        )
    )
    results.extend(
        run_model_tests(
            model,
            test_set,
            test_preds=(y_pred, class_pred),
            train_set=train_set,
            train_preds=(y_train_pred, train_class_pred),
            send=send,
            run_cuid=run_cuid,
        )
    )

    return results
