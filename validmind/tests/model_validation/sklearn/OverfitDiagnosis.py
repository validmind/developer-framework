# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import metrics

from validmind.logging import get_logger
from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
    VMDataset,
    VMModel,
)

logger = get_logger(__name__)

# TODO: A couple of improvements here could be to:
# 1. Allow the test to use multiple metrics at once
# 2. Allow custom functions for computing performance

DEFAULT_THRESHOLD = 0.04
DEFAULT_CLASSIFICATION_METRIC = "auc"
DEFAULT_REGRESSION_METRIC = "mse"
PERFORMANCE_METRICS = {
    "accuracy": {
        "function": metrics.accuracy_score,
        "is_lower_better": False,
    },
    "auc": {
        "function": metrics.roc_auc_score,
        "is_lower_better": False,
    },
    "f1": {
        "function": metrics.f1_score,
        "is_lower_better": False,
    },
    "precision": {
        "function": metrics.precision_score,
        "is_lower_better": False,
    },
    "recall": {
        "function": metrics.recall_score,
        "is_lower_better": False,
    },
    "mse": {
        "function": metrics.mean_squared_error,
        "is_lower_better": True,
    },
    "mae": {
        "function": metrics.mean_absolute_error,
        "is_lower_better": True,
    },
    "r2": {
        "function": metrics.r2_score,
        "is_lower_better": False,
    },
    "mape": {
        "function": metrics.mean_absolute_percentage_error,
        "is_lower_better": True,
    },
}


def _prepare_results(
    results_train: dict, results_test: dict, metric: str
) -> pd.DataFrame:
    results_train = pd.DataFrame(results_train)
    results_test = pd.DataFrame(results_test)
    results = results_train.copy()
    results.rename(
        columns={"shape": "training records", f"{metric}": f"training {metric}"},
        inplace=True,
    )
    results[f"test {metric}"] = results_test[metric]

    # Adjust gap calculation based on metric directionality
    if PERFORMANCE_METRICS[metric]["is_lower_better"]:
        results["gap"] = results[f"test {metric}"] - results[f"training {metric}"]
    else:
        results["gap"] = results[f"training {metric}"] - results[f"test {metric}"]

    return results


def _compute_metrics(
    results: dict,
    region: str,
    df_region: pd.DataFrame,
    target_column: str,
    prob_column: str,
    pred_column: str,
    feature_column: str,
    metric: str,
    is_classification: bool,
) -> None:
    results["slice"].append(str(region))
    results["shape"].append(df_region.shape[0])
    results["feature"].append(feature_column)

    # Check if any records
    if df_region.empty:
        results[metric].append(0)
        return

    metric_func = PERFORMANCE_METRICS[metric]["function"]
    y_true = df_region[target_column].values

    # AUC requires probability scores
    if is_classification and metric == "auc":
        # if only one class is present in the data, return 0
        if len(np.unique(y_true)) == 1:
            return results[metric].append(0)

        return results[metric].append(
            metric_func(y_true, df_region[prob_column].values)
        )

    return results[metric].append(metric_func(y_true, df_region[pred_column].values))


def _plot_overfit_regions(
    df: pd.DataFrame, feature_column: str, threshold: float, metric: str
) -> plt.Figure:
    fig, ax = plt.subplots()
    barplot = sns.barplot(data=df, x="slice", y="gap", ax=ax)
    ax.tick_params(axis="x", rotation=90)

    # Draw threshold line
    axhline = ax.axhline(
        y=threshold,
        color="red",
        linestyle="--",
        linewidth=1,
        label=f"Cut-Off Threshold: {threshold}",
    )
    ax.tick_params(axis="x", labelsize=20)
    ax.tick_params(axis="y", labelsize=20)

    ax.set_ylabel(f"{metric.upper()} Gap", weight="bold", fontsize=18)
    ax.set_xlabel("Slice/Segments", weight="bold", fontsize=18)
    ax.set_title(
        f"Overfit regions in feature column: {feature_column}",
        weight="bold",
        fontsize=20,
        wrap=True,
    )

    handles, labels = barplot.get_legend_handles_labels()
    handles.append(axhline)
    labels.append(axhline.get_label())

    barplot.legend(
        handles=handles[:-1],
        labels=labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.1),
        ncol=len(handles),
    )

    plt.close("all")

    return fig


# TODO: make this a functional test instead of class-based when appropriate
# simply have to remove the class and rename this func to OverfitDiagnosis
def overfit_diagnosis(  # noqa: C901
    model: VMModel,
    datasets: List[VMDataset],
    metric: str = None,
    cut_off_threshold: float = DEFAULT_THRESHOLD,
):
    """Identify overfit regions in a model's predictions.

    This test compares the model's performance on training versus test data, grouped by
    feature columns. It calculates the difference between the training and test performance
    for each group and identifies regions where the difference exceeds a specified threshold.

    ## Test Methodology

    This test works for both classification and regression models and with a variety of
    performance metrics. By default, it uses the AUC metric for classification models and
    the MSE metric for regression models. The threshold for identifying overfit regions
    defaults to 0.04 but should be adjusted based on the specific use case.

    ## Inputs
    - `model` (VMModel): The ValidMind model object to evaluate.
    - `datasets` (List[VMDataset]): A list of two VMDataset objects where the first dataset
        is the training data and the second dataset is the test data.

    ## Parameters
    - `metric` (str, optional): The performance metric to use for evaluation. Choose from:
        'accuracy', 'auc', 'f1', 'precision', 'recall', 'mse', 'mae', 'r2', 'mape'.
        Defaults to 'auc' for classification models and 'mse' for regression models.
    - `cut_off_threshold` (float, optional): The threshold for identifying overfit regions.
        Defaults to 0.04.
    """

    # Determine if it's a classification or regression model
    is_classification = bool(datasets[0].probability_column(model))

    # Set default metric if not provided
    if not metric:
        metric = (
            DEFAULT_CLASSIFICATION_METRIC
            if is_classification
            else DEFAULT_REGRESSION_METRIC
        )
        logger.info(
            f"Using default {'classification' if is_classification else 'regression'} metric: {metric}"
        )

    if id(cut_off_threshold) == id(DEFAULT_THRESHOLD):
        logger.info("Using default cut-off threshold of 0.04")

    train_df = datasets[0].df
    test_df = datasets[1].df

    pred_column = f"{datasets[0].target_column}_pred"
    prob_column = f"{datasets[0].target_column}_prob"

    train_df[pred_column] = datasets[0].y_pred(model)
    test_df[pred_column] = datasets[1].y_pred(model)

    if is_classification:
        train_df[prob_column] = datasets[0].y_prob(model)
        test_df[prob_column] = datasets[1].y_prob(model)

    test_results = []
    test_figures = []
    results_headers = ["slice", "shape", "feature", metric]

    for feature_column in datasets[0].feature_columns:
        bins = 10
        if feature_column in datasets[0].feature_columns_categorical:
            bins = len(train_df[feature_column].unique())
        train_df["bin"] = pd.cut(train_df[feature_column], bins=bins)

        results_train = {k: [] for k in results_headers}
        results_test = {k: [] for k in results_headers}

        for region, df_region in train_df.groupby("bin"):
            _compute_metrics(
                results=results_train,
                region=region,
                df_region=df_region,
                feature_column=feature_column,
                target_column=datasets[0].target_column,
                prob_column=prob_column,
                pred_column=pred_column,
                metric=metric,
                is_classification=is_classification,
            )
            df_test_region = test_df[
                (test_df[feature_column] > region.left)
                & (test_df[feature_column] <= region.right)
            ]
            _compute_metrics(
                results=results_test,
                region=region,
                df_region=df_test_region,
                feature_column=feature_column,
                target_column=datasets[1].target_column,
                prob_column=prob_column,
                pred_column=pred_column,
                metric=metric,
                is_classification=is_classification,
            )

        results = _prepare_results(results_train, results_test, metric)

        fig = _plot_overfit_regions(results, feature_column, cut_off_threshold, metric)
        test_figures.append(
            Figure(
                key=f"overfit_diagnosis:{metric}:{feature_column}",
                figure=fig,
                metadata={
                    "metric": metric,
                    "cut_off_threshold": cut_off_threshold,
                    "feature": feature_column,
                },
            )
        )

        for _, row in results[results["gap"] > cut_off_threshold].iterrows():
            test_results.append(
                {
                    "Feature": feature_column,
                    "Slice": row["slice"],
                    "Number of Records": row["training records"],
                    f"Training {metric.upper()}": row[f"training {metric}"],
                    f"Test {metric.upper()}": row[f"test {metric}"],
                    "Gap": row["gap"],
                }
            )

    return {"Overfit Diagnosis": test_results}, *test_figures


@dataclass
class OverfitDiagnosis(ThresholdTest):
    """
    Assesses potential overfitting in a model's predictions, identifying regions where performance between training and
    testing sets deviates significantly.

    ### Purpose

    The Overfit Diagnosis test aims to identify areas in a model's predictions where there is a significant difference
    in performance between the training and testing sets. This test helps to pinpoint specific regions or feature
    segments where the model may be overfitting.

    ### Test Mechanism

    This test compares the model's performance on training versus test data, grouped by feature columns. It calculates
    the difference between the training and test performance for each group and identifies regions where this
    difference exceeds a specified threshold:

    - The test works for both classification and regression models.
    - It defaults to using the AUC metric for classification models and the MSE metric for regression models.
    - The threshold for identifying overfitting regions is set to 0.04 by default.
    - The test calculates the performance metrics for each feature segment and plots regions where the performance gap
    exceeds the threshold.

    ### Signs of High Risk

    - Significant gaps between training and test performance metrics for specific feature segments.
    - Multiple regions with performance gaps exceeding the defined threshold.
    - Higher than expected differences in predicted versus actual values in the test set compared to the training set.

    ### Strengths

    - Identifies specific areas where overfitting occurs.
    - Supports multiple performance metrics, providing flexibility.
    - Applicable to both classification and regression models.
    - Visualization of overfitting segments aids in better understanding and debugging.

    ### Limitations

    - The default threshold may not be suitable for all use cases and requires tuning.
    - May not capture more subtle forms of overfitting that do not exceed the threshold.
    - Assumes that the binning of features adequately represents the data segments.
    """

    required_inputs = ["model", "datasets"]
    default_params = {"metric": None, "cut_off_threshold": DEFAULT_THRESHOLD}
    tasks = ["classification", "regression"]
    tags = [
        "sklearn",
        "binary_classification",
        "multiclass_classification",
        "linear_regression",
        "model_diagnosis",
    ]

    def run(self):
        func_result = overfit_diagnosis(
            self.inputs.model,
            self.inputs.datasets,
            metric=self.params["metric"],
            cut_off_threshold=self.params["cut_off_threshold"],
        )

        return self.cache_results(
            test_results_list=[
                ThresholdTestResult(
                    test_name=self.params["metric"],
                    column=row["Feature"],
                    passed=False,
                    values={k: v for k, v in row.items()},
                )
                for row in func_result[0]["Overfit Diagnosis"]
            ],
            passed=(not func_result[0]["Overfit Diagnosis"]),
            figures=func_result[1:],
        )

    def summary(self, results, _):
        return ResultSummary(
            results=[
                ResultTable(
                    data=[result.values for result in results],
                    metadata=ResultTableMetadata(title="Overfit Diagnosis"),
                )
            ],
        )
