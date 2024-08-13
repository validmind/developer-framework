# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from collections import defaultdict
from dataclasses import dataclass
from operator import add
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import metrics

from validmind.errors import MissingOrInvalidModelPredictFnError
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

DEFAULT_DECAY_THRESHOLD = 0.05
DEFAULT_STD_DEV_LIST = [0.1, 0.2, 0.3, 0.4, 0.5]
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


def _add_noise_std_dev(
    values: List[float], x_std_dev: float
) -> Tuple[List[float], float]:
    """
    Adds Gaussian noise to a list of values.
    Args:
        values (list[float]): A list of numerical values to which noise is added.
        x_std_dev (float): A scaling factor for the standard deviation of the noise.
    Returns:
        tuple[list[float], float]: A tuple containing:
            - A list of noisy values, where each value is the sum of the corresponding value
            in the input list and a randomly generated value sampled from a Gaussian distribution
            with mean 0 and standard deviation x_std_dev times the standard deviation of the input list.
            - The standard deviation of the input list of values.
    """
    std_dev = np.std(values)
    noise_list = np.random.normal(0, x_std_dev * std_dev, size=len(values))
    noisy_values = list(map(add, noise_list, values))

    return noisy_values


def _compute_metric(
    dataset: VMDataset, model: VMModel, X: pd.DataFrame, metric: str
) -> float:
    if metric not in PERFORMANCE_METRICS:
        raise ValueError(
            f"Invalid metric: {metric}, expected one of {PERFORMANCE_METRICS.keys()}"
        )

    if metric == "auc":
        try:
            y_proba = model.predict_proba(X)
        except MissingOrInvalidModelPredictFnError:
            y_proba = model.predict(X)
        return metrics.roc_auc_score(dataset.y, y_proba)

    return PERFORMANCE_METRICS[metric]["function"](dataset.y, model.predict(X))


def _compute_gap(result: dict, metric: str) -> float:
    if PERFORMANCE_METRICS[metric]["is_lower_better"]:
        return result[metric.upper()][-1] - result[metric.upper()][0]

    return result[metric.upper()][0] - result[metric.upper()][-1]


def _combine_results(results: List[dict]):
    final_results = defaultdict(list)

    # Interleave rows from each dictionary
    for i in range(len(results[0]["Perturbation Size"])):
        for result in results:
            for key in result.keys():
                final_results[key].append(result[key][i])

    return pd.DataFrame(final_results)


def _plot_robustness(
    results: pd.DataFrame, metric: str, threshold: float, columns: List[str]
):
    fig, ax = plt.subplots()

    pallete = sns.color_palette("muted", len(results["Dataset"].unique()))
    sns.lineplot(
        data=results,
        x="Perturbation Size",
        y=metric.upper(),
        hue="Dataset",
        style="Dataset",
        linewidth=3,
        markers=True,
        markersize=10,
        dashes=False,
        palette=pallete,
        ax=ax,
    )

    if PERFORMANCE_METRICS[metric]["is_lower_better"]:
        y_label = f"{metric.upper()} (lower is better)"
    else:
        threshold = -threshold
        y_label = f"{metric.upper()} (higher is better)"

    # add dotted threshold line
    for i in range(len(results["Dataset"].unique())):
        baseline = results[results["Dataset"] == results["Dataset"].unique()[i]][
            metric.upper()
        ].iloc[0]
        ax.axhline(
            y=baseline + threshold,
            color=pallete[i],
            linestyle="dotted",
        )

    ax.tick_params(axis="x")
    ax.set_ylabel(y_label, weight="bold", fontsize=18)
    ax.legend(fontsize=18)
    ax.set_xlabel(
        "Perturbation Size (X * Standard Deviation)", weight="bold", fontsize=18
    )
    ax.set_title(
        f"Perturbed Features: {', '.join(columns)}",
        weight="bold",
        fontsize=20,
        wrap=True,
    )

    # prevent the figure from being displayed
    plt.close("all")

    return fig


# TODO: make this a functional test instead of class-based when appropriate
# simply have to remove the class and rename this func to OverfitDiagnosis
def robustness_diagnosis(
    model: VMModel,
    datasets: List[VMDataset],
    metric: str = None,
    scaling_factor_std_dev_list: List[float] = DEFAULT_STD_DEV_LIST,
    performance_decay_threshold: float = DEFAULT_DECAY_THRESHOLD,
):
    if not metric:
        metric = (
            DEFAULT_CLASSIFICATION_METRIC
            if datasets[0].probability_column(model)
            else DEFAULT_REGRESSION_METRIC
        )
        logger.info(f"Using default metric ({metric.upper()}) for robustness diagnosis")

    if id(scaling_factor_std_dev_list) == id(DEFAULT_STD_DEV_LIST):
        logger.info(
            f"Using default scaling factors for the standard deviation of the noise: {DEFAULT_STD_DEV_LIST}"
        )

    if id(performance_decay_threshold) == id(DEFAULT_DECAY_THRESHOLD):
        logger.info(
            f"Using default performance decay threshold of {DEFAULT_DECAY_THRESHOLD}"
        )

    results = [{} for _ in range(len(datasets))]

    # add baseline results (no perturbation)
    for dataset, result in zip(datasets, results):
        result["Perturbation Size"] = [0.0]
        result["Dataset"] = [f"{dataset.input_id}"]
        result["Row Count"] = [dataset._df.shape[0]]

        result[metric.upper()] = [
            _compute_metric(
                dataset=dataset,
                model=model,
                X=dataset.x_df(),
                metric=metric,
            )
        ]
        result["Performance Decay"] = [0.0]
        result["Passed"] = [True]

    # Iterate scaling factor for the standard deviation list
    for x_std_dev in scaling_factor_std_dev_list:
        for dataset, result in zip(datasets, results):

            result["Perturbation Size"].append(x_std_dev)
            result["Dataset"].append(result["Dataset"][0])
            result["Row Count"].append(result["Row Count"][0])

            temp_df = dataset.x_df().copy()
            for feature in dataset.feature_columns_numeric:
                temp_df[feature] = _add_noise_std_dev(
                    values=temp_df[feature].to_list(),
                    x_std_dev=x_std_dev,
                )

            result[metric.upper()].append(
                _compute_metric(
                    dataset=dataset,
                    model=model,
                    X=temp_df,
                    metric=metric,
                )
            )
            result["Performance Decay"].append(_compute_gap(result, metric))
            result["Passed"].append(
                result["Performance Decay"][-1] < performance_decay_threshold
            )

    results_df = _combine_results(results)
    fig = _plot_robustness(
        results=results_df,
        metric=metric,
        threshold=performance_decay_threshold,
        columns=datasets[0].feature_columns_numeric,
    )

    # rename perturbation size for baseline
    results_df["Perturbation Size"][
        results_df["Perturbation Size"] == 0.0
    ] = "Baseline (0.0)"

    return results_df, fig


@dataclass
class RobustnessDiagnosis(ThresholdTest):
    """Evaluate the robustness of a machine learning model to noise

    Robustness refers to a model's ability to maintain a high level of performance in
    the face of perturbations or changes (particularly noise) added to its input data.
    This test is designed to help gauge how well the model can handle potential real-
    world scenarios where the input data might be incomplete or corrupted.

    ## Test Methodology
    This test is conducted by adding Gaussian noise, proportional to a particular standard
    deviation scale, to numeric input features of the input datasets. The model's
    performance on the perturbed data is then evaluated using a user-defined metric or the
    default metric of AUC for classification tasks and MSE for regression tasks. The results
    are then plotted to visualize the model's performance decay as the perturbation size
    increases.

    When using this test, it is highly recommended to tailor the performance metric, list
    of scaling factors for the standard deviation of the noise, and the performance decay
    threshold to the specific use case of the model being evaluated.

    **Inputs**:
    - model (VMModel): The trained model to be evaluated.
    - datasets (List[VMDataset]): A list of datasets to evaluate the model against.

    ## Parameters
    - metric (str, optional): The performance metric to be used for evaluation. If not
        provided, the default metric is used based on the task of the model. Default values
        are "auc" for classification tasks and "mse" for regression tasks.
    - scaling_factor_std_dev_list (List[float], optional): A list of scaling factors for
        the standard deviation of the noise to be added to the input features. The default
        values are [0.1, 0.2, 0.3, 0.4, 0.5].
    - performance_decay_threshold (float, optional): The threshold for the performance
        decay of the model. The default value is 0.05.
    """

    name = "robustness"
    required_inputs = ["model", "datasets"]
    default_params = {
        "metric": None,
        "scaling_factor_std_dev_list": DEFAULT_STD_DEV_LIST,
        "performance_decay_threshold": DEFAULT_DECAY_THRESHOLD,
    }
    tasks = ["classification", "regression"]
    tags = [
        "sklearn",
        "model_diagnosis",
        "visualization",
    ]

    def run(self):
        results, fig = robustness_diagnosis(
            model=self.inputs.model,
            datasets=self.inputs.datasets,
            metric=self.params["metric"],
            scaling_factor_std_dev_list=self.params["scaling_factor_std_dev_list"],
            performance_decay_threshold=self.params["performance_decay_threshold"],
        )

        return self.cache_results(
            passed=results["Passed"].all(),
            test_results_list=[
                ThresholdTestResult(
                    test_name=self.params["metric"],
                    passed=results["Passed"].all(),
                    values=results,
                )
            ],
            figures=[
                Figure(
                    for_object=self,
                    key=f"{self.name}:{self.params['metric']}",
                    figure=fig,
                )
            ],
        )

    def summary(self, results: List[ThresholdTestResult], _):
        return ResultSummary(
            results=[
                ResultTable(
                    data=results[0].values,
                    metadata=ResultTableMetadata(title="Robustness Diagnosis Results"),
                )
            ]
        )

    def test(self):
        """Unit Test for Robustness Diagnosis Threshold Test"""
        # Verify the result object is present
        assert self.result is not None

        # Verify test results and their type
        assert isinstance(self.result.test_results.results, list)

        # Check for presence and validity of 'values' and 'passed' flag in each result
        for test_result in self.result.test_results.results:
            assert "values" in test_result.__dict__
            assert "passed" in test_result.__dict__
            assert isinstance(test_result.values, pd.DataFrame)
