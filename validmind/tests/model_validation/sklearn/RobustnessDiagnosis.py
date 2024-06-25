# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from operator import add
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import metrics

from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class RobustnessDiagnosis(ThresholdTest):
    """
    Evaluates the robustness of a machine learning model by injecting Gaussian noise to input data and measuring
    performance.

    **Purpose**:

    The purpose of this test code is to evaluate the robustness of a machine learning model. Robustness refers to a
    model's ability to maintain a high level of performance in the face of perturbations or changes—particularly
    noise—added to its input data. This test is designed to help gauge how well the model can handle potential
    real-world scenarios where the input data might be incomplete or corrupted.

    **Test Mechanism**:

    This test is conducted by adding Gaussian noise, proportional to a particular standard deviation scale, to numeric
    input features of both the training and testing datasets. The model performance in the face of these perturbed
    features is then evaluated using metrics (default: 'accuracy'). This process is iterated over a range of scale
    factors. The resulting accuracy trend against the amount of noise introduced is illustrated with a line chart. A
    predetermined threshold determines what level of accuracy decay due to perturbation is considered acceptable.

    **Signs of High Risk**:
    - Substantial decreases in accuracy when noise is introduced to feature inputs.
    - The decay in accuracy surpasses the configured threshold, indicating that the model is not robust against input
    noise.
    - Instances where one or more elements provided in the features list don't match with the training dataset's
    numerical feature columns.

    **Strengths**:
    - Provides an empirical measure of the model's performance in tackling noise or data perturbations, revealing
    insights into the model's stability.
    - Offers flexibility with the ability to choose specific features to perturb and control the level of noise applied.
    - Detailed results visualization helps in interpreting the outcome of robustness testing.

    **Limitations**:
    - Only numerical features are perturbed, leaving out non-numerical features, which can lead to an incomplete
    analysis of robustness.
    - The default metric used is accuracy, which might not always give the best measure of a model's success,
    particularly for imbalanced datasets.
    - The test is contingent on the assumption that the added Gaussian noise sufficiently represents potential data
    corruption or incompleteness in real-world scenarios.
    - There might be a requirement to fine-tune the set decay threshold for accuracy with the help of domain knowledge
    or specific project requisites.
    - The robustness test might not deliver the expected results for datasets with a text column.
    """

    name = "robustness"
    required_inputs = ["model", "datasets"]
    default_params = {
        "features_columns": None,
        "scaling_factor_std_dev_list": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
        "accuracy_decay_threshold": 4,
    }
    tasks = ["classification", "text_classification"]
    tags = [
        "sklearn",
        "binary_classification",
        "multiclass_classification",
        "model_diagnosis",
        "visualization",
    ]

    default_metrics = {"accuracy": metrics.accuracy_score}

    def run(self):
        # Validate X std deviation parameter
        if "scaling_factor_std_dev_list" not in self.params:
            raise ValueError("scaling_factor_std_dev_list must be provided in params")
        x_std_dev_list = self.params["scaling_factor_std_dev_list"]

        if self.params["accuracy_decay_threshold"] is None:
            raise ValueError("accuracy_decay_threshold must be provided in params")
        accuracy_threshold = self.params["accuracy_decay_threshold"]

        if self.inputs.model is None:
            raise ValueError("model must of provided to run this test")

        # Validate list of features columns need to be perterubed
        if "features_columns" not in self.params:
            raise ValueError("features_columns must be provided in params")

        features_list = self.params["features_columns"]
        if features_list is None:
            features_list = self.inputs.datasets[0].feature_columns

        # Check if all elements from features_list are present in the numerical feature columns
        all_present = all(
            elem in self.inputs.datasets[0].feature_columns for elem in features_list
        )
        if not all_present:
            raise ValueError(
                "The list of feature columns provided do not match with training "
                + "dataset numerical feature columns"
            )

        if self.inputs.datasets[0].text_column in features_list:
            raise ValueError(
                "Skiping Robustness Diagnosis test for the dataset with text column"
            )

        train_df = self.inputs.datasets[0].x_df().copy()
        train_y_true = self.inputs.datasets[0].y

        test_df = self.inputs.datasets[1].x_df().copy()
        test_y_true = self.inputs.datasets[1].y

        test_results = []
        test_figures = []

        results_headers = ["Perturbation Size", "Dataset Type", "Records"] + list(
            self.default_metrics.keys()
        )
        results = {k: [] for k in results_headers}
        # Iterate scaling factor for the standard deviation list
        for x_std_dev in x_std_dev_list:
            temp_train_df = train_df.copy()
            temp_test_df = test_df.copy()

            # Add noise to numeric features columns provided by user
            for feature in features_list:
                temp_train_df[feature] = self._add_noise_std_dev(
                    temp_train_df[feature].to_list(), x_std_dev
                )
                temp_test_df[feature] = self._add_noise_std_dev(
                    temp_test_df[feature].to_list(), x_std_dev
                )

            self._compute_metrics(
                results, temp_train_df, train_y_true, x_std_dev, "Training"
            )
            self._compute_metrics(results, temp_test_df, test_y_true, x_std_dev, "Test")

        fig, df = self._plot_robustness(results, features_list)

        test_figures.append(
            Figure(
                for_object=self,
                key=f"{self.name}:accuracy",
                figure=fig,
                metadata={
                    "metric": "accuracy",
                    "features_list": features_list,
                },
            )
        )

        train_acc = df.loc[(df["Dataset Type"] == "Training"), "accuracy"].values[0]
        test_acc = df.loc[(df["Dataset Type"] == "Test"), "accuracy"].values[0]

        df["Passed"] = np.where(
            (df["Dataset Type"] == "Training")
            & (df["accuracy"] >= (train_acc - accuracy_threshold)),
            True,
            np.where(
                (df["Dataset Type"] == "Test")
                & (df["accuracy"] >= (test_acc - accuracy_threshold)),
                True,
                False,
            ),
        )
        test_results.append(
            ThresholdTestResult(
                test_name="accuracy",
                column=features_list,
                passed=True,
                values={"records": df.to_dict("records")},
            )
        )
        return self.cache_results(
            test_results, passed=df["Passed"].all(), figures=test_figures
        )

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
        results_table = [
            record for result in results for record in result.values["records"]
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(title="Robustness test"),
                )
            ]
        )

    def _compute_metrics(
        self,
        results: dict,
        df: pd.DataFrame,
        y_true: str,
        x_std_dev: float,
        dataset_type: str,
    ):
        """
        Compute evaluation metrics for a given perturbed dataset.
        Args:
        results (dict): A dictionary to store the results of the computation.
        df (pd.DataFrame): A Pandas dataframe containing the dataset to evaluate.
        y_true (str): A string representing the name of the column containing the true target values.
        x_std_dev (float): A float representing the standard deviation of the perturbation applied to the dataset.
        dataset_type (str): A string representing the type of dataset (e.g. "training", "validation", "test").
        Returns:
        None
        """
        results["Dataset Type"].append(dataset_type)
        results["Perturbation Size"].append(x_std_dev)
        results["Records"].append(df.shape[0])
        y_prediction = self.inputs.model.predict(df)
        for metric, metric_fn in self.default_metrics.items():
            results[metric].append(metric_fn(y_true, y_prediction) * 100)

    def _add_noise_std_dev(
        self, values: List[float], x_std_dev: float
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

    def _plot_robustness(self, results: dict, features_columns: List[str]):
        """
        Plots the model's accuracy under feature perturbations.
        Args:
            results (dict): A dictionary containing the results of the evaluation.
                It has the following keys:
                    - 'Dataset Type': the type of dataset evaluated, e.g. 'Training' or 'Test'.
                    - 'Perturbation Size': the size of the perturbation applied to the features.
                    - 'Records': the number of records evaluated.
                    - Any other metric used for evaluation as keys, e.g. 'accuracy', 'precision', 'recall'.
                The values of each key are lists containing the results for each evaluation.
            features_columns (list[str]): A list containing the names of the features perturbed.
        Returns:
            tuple[matplotlib.figure.Figure, pd.DataFrame]: A tuple containing the matplotlib Figure object
            and a DataFrame containing the results used to generate the plot.
        """
        df = pd.DataFrame(results)

        # Create a bar plot using seaborn library
        fig, ax = plt.subplots()
        sns.lineplot(
            data=df,
            x="Perturbation Size",
            y="accuracy",
            hue="Dataset Type",
            style="Dataset Type",
            linewidth=3,
            markers=True,
            markersize=10,
            dashes=False,
            palette=["red", "blue"],
            ax=ax,
        )
        ax.tick_params(axis="x")
        ax.set_ylabel("Accuracy", weight="bold", fontsize=18)
        ax.legend(fontsize=18)
        ax.set_xlabel(
            "Perturbation Size (X * Standard Deviation)", weight="bold", fontsize=18
        )
        ax.set_title(
            f"Perturbed Features: {', '.join(features_columns)}",
            weight="bold",
            fontsize=20,
            wrap=True,
        )

        # Do this if you want to prevent the figure from being displayed
        plt.close("all")

        # fig, ax = plt.subplots()
        return fig, df

    def test(self):
        """Unit Test for Robustness Diagnosis Threshold Test"""
        # Verify the result object is present
        assert self.result is not None

        # Verify test results and their type
        assert isinstance(self.result.test_results.results, list)

        # Check for presence and validity of 'values' dict and 'passed' flag in each result
        for test_result in self.result.test_results.results:
            assert "values" in test_result.__dict__
            assert "passed" in test_result.__dict__
            assert isinstance(test_result.values, dict)
            assert "records" in test_result.values

            # For unperturbed training dataset, accuracy should be present
            if (
                test_result.column == self.params["features_columns"]
                and 0.0 in test_result.values["records"][0]["Perturbation Size"]
            ):
                assert "accuracy" in test_result.values["records"][0]
