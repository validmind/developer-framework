# Copyright © 2023 ValidMind Inc. All rights reserved.

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
    TestResult,
    ThresholdTest,
    Model,
)


@dataclass
class RobustnessDiagnosis(ThresholdTest):
    """
    Test robustness of model by perturbing the features column values by adding noise within scale
    stardard deviation.
    """

    category = "model_diagnosis"
    name = "robustness"
    required_context = ["model", "model.train_ds", "model.test_ds"]

    default_params = {
        "features_columns": None,
        "scaling_factor_std_dev_list": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
        "accuracy_decay_threshold": 4,
    }
    default_metrics = {
        "accuracy": metrics.accuracy_score,
    }

    def description(self):
        return """
        The robustness of a machine learning model refers to its ability to maintain performance
        in the face of perturbations or changes to the input data. One way to test the robustness
        of a model is by perturbing its input features and observing how the model's performance changes.

        To perturb the input features, one can add random noise or modify the values of the features
        within a certain range. By perturbing the input features, one can simulate different scenarios
        in which the input data may be corrupted or incomplete, and test whether the model is able to
        handle such scenarios.

        The performance of the model can be measured in terms of its accuracy, precision, recall,
        or any other relevant metric, both before and after perturbing the input features. A model
        that is robust to perturbations should maintain a high level of performance even after the
        input features have been perturbed.
        """

    def run(self):
        model_library = Model.model_library(self.model.model)
        if model_library == "statsmodels" or model_library == "pytorch":
            print(f"Skiping Robustness Diagnosis test for {model_library} models")
            return

        # Validate X std deviation parameter
        if "scaling_factor_std_dev_list" not in self.params:
            raise ValueError("scaling_factor_std_dev_list must be provided in params")
        x_std_dev_list = self.params["scaling_factor_std_dev_list"]

        if self.params["accuracy_decay_threshold"] is None:
            raise ValueError("accuracy_decay_threshold must be provided in params")
        accuracy_threshold = self.params["accuracy_decay_threshold"]

        if self.model is None:
            raise ValueError("model must of provided to run this test")

        # Validate list of features columns need to be perterubed
        if "features_columns" not in self.params:
            raise ValueError("features_columns must be provided in params")

        features_list = self.params["features_columns"]
        if features_list is None:
            features_list = self.model.train_ds.get_numeric_features_columns()

        # Check if all elements from features_list are present in the numerical feature columns
        all_present = all(
            elem in self.model.train_ds.get_numeric_features_columns()
            for elem in features_list
        )
        if not all_present:
            raise ValueError(
                "The list of feature columns provided do not match with training "
                + "dataset numerical feature columns"
            )

        # Remove target column if it exist in the list
        features_list = self.model.train_ds.get_features_columns()

        train_df = self.model.train_ds.x_df().copy()
        train_y_true = self.model.train_ds.y

        test_df = self.model.test_ds.x_df().copy()
        test_y_true = self.model.test_ds.y

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
            TestResult(
                test_name="accuracy",
                column=features_list,
                passed=True,
                values={"records": df.to_dict("records")},
            )
        )
        return self.cache_results(
            test_results, passed=df["Passed"].all(), figures=test_figures
        )

    def summary(self, results: List[TestResult], all_passed: bool):
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
        y_prediction = self.model.model.predict(df)
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
