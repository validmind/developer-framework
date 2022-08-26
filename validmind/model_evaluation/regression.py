"""
Evaluation Functions for Regression Models
"""
from tqdm import tqdm

from .utils import summarize_evaluation_results
from ..client import log_evaluation_metrics, log_figure
from ..metrics.generic import (
    permutation_importance,
    shap_global_importance,
)
from ..metrics.regression import (
    mae_score,
    mse_score,
    r2_score,
)
from ..tests.config import Settings

config = Settings()


def evaluate_regression_model(
    model, test_set, train_set=None, send=False, run_cuid=None
):
    """
    Run a suite of model evaluation tests and log their results to the API
    """
    x_test, y_test = test_set

    print("Generating model predictions on test dataset...")
    y_pred = model.predict(x_test)

    print("Running evaluation tests...")

    tests = [
        mae_score,
        mse_score,
        r2_score,
    ]
    evaluation_metrics_results = []

    with tqdm(total=len(tests) + 1) as pbar:
        for test in tests:
            evaluation_metric_result = test(y_test, y_pred)
            evaluation_metrics_results.append(evaluation_metric_result)
            pbar.update(1)

        evaluation_metrics_results.append(permutation_importance(model, x_test, y_test))
        pbar.update(1)

        shap_results = shap_global_importance(model, x_test, linear=True)
        figures = shap_results.pop("plots")
        evaluation_metrics_results.append(shap_results)
        pbar.update(1)

    print("\nModel evaluation tests have completed.")
    if send:
        print(
            f"Sending {len(evaluation_metrics_results)} metrics results to ValidMind..."
        )
        log_evaluation_metrics(evaluation_metrics_results, run_cuid=run_cuid)

        print(f"Sending {len(figures)} figures to ValidMind...")
        for figure in figures:
            log_figure(figure["figure"], key=figure["key"], metadata=figure["metadata"])

    print("\nSummary of results:\n")
    table = summarize_evaluation_results(evaluation_metrics_results)
    print(table)

    print("\nPlotting model evaluation results...")
    # _get_roc_curve_plot(evaluation_metrics_results)
    return evaluation_metrics_results
