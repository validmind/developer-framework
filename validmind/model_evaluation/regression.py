"""
Evaluation Functions for Regression Models
"""
import matplotlib.pyplot as plt

from IPython.display import display
from tqdm import tqdm

from .utils import summarize_evaluation_metrics
from ..client import log_metrics, log_figure
from ..metrics.generic import (
    permutation_importance,
    shap_global_importance,
)
from ..metrics.regression import (
    adjusted_r2_score,
    mae_score,
    mse_score,
    r2_score,
)
from ..tests.config import Settings

config = Settings()


# TODO: same function as classification and regression, refactor
# TODO: shap requires an extra arg
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
        adjusted_r2_score,
        mae_score,
        mse_score,
        permutation_importance,
        r2_score,
        shap_global_importance,
    ]
    evaluation_metrics = []
    evaluation_figures = []
    report_figures = []

    plt.ioff()

    with tqdm(total=len(metrics)) as pbar:
        for metric_fn in metrics:
            if metric_fn.__name__ == "shap_global_importance":
                evaluation_metric_result = metric_fn(
                    model, test_set, test_preds, linear=True
                )
            else:
                evaluation_metric_result = metric_fn(
                    model, test_set, test_preds, train_set, train_preds
                )

            # TBD: make sure the test functions always return a list
            evaluation_metric_result = (
                [evaluation_metric_result]
                if not isinstance(evaluation_metric_result, list)
                else evaluation_metric_result
            )

            for result in evaluation_metric_result:
                if result.api_metric:
                    evaluation_metrics.append(result.api_metric)

                if result.api_figures:
                    evaluation_figures.extend(result.api_figures)
                    # extract plots from "figure" key on each api_figure so
                    # we can also display the figures that are going to be
                    # sent to the ValidMind API
                    for api_figure in result.api_figures:
                        report_figures.append(api_figure.figure)

                if result.plots:
                    report_figures.extend(result.plots)

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

    if len(report_figures):
        print("\nPlotting model evaluation metrics...")

    for figure in report_figures:
        if hasattr(figure, "canvas"):
            display(figure)
        elif hasattr(figure, "plot"):
            figure.plot()
            plt.show()

    return evaluation_metrics


def evaluate_regression_model(
    model, test_set, train_set=None, eval_opts=None, send=True, run_cuid=None
):
    """
    Run a suite of model evaluation tests and log their results to the API
    """
    x_test, _ = test_set

    print("Generating model predictions on test dataset...")
    y_pred = model.predict(x_test)

    if train_set is not None:
        x_train, _ = train_set
        print("Generating model predictions on training dataset...")
        y_train_pred = model.predict(x_train)

    results = []
    results.extend(
        get_model_metrics(
            model,
            test_set,
            test_preds=(y_pred, None),
            train_set=train_set,
            train_preds=(y_train_pred, None),
            send=send,
            run_cuid=run_cuid,
        )
    )

    return results
