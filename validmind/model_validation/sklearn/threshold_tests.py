"""
Threshold based tests
"""
from dataclasses import dataclass
from functools import partial
from operator import add
from sklearn import metrics
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from ...vm_models import TestResult, Figure, ThresholdTest


@dataclass
class MinimumAccuracy(ThresholdTest):
    """
    Test that the model's prediction accuracy on a dataset meets or
    exceeds a predefined threshold.
    """

    category = "model_performance"
    name = "accuracy_score"
    default_params = {"min_threshold": 0.7}

    def run(self):
        y_true = self.test_ds.y
        class_pred = self.class_predictions(self.y_test_predict)
        accuracy_score = metrics.accuracy_score(y_true, class_pred)

        passed = accuracy_score > self.params["min_threshold"]
        results = [
            TestResult(
                passed=passed,
                values={
                    "score": accuracy_score,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))


@dataclass
class MinimumF1Score(ThresholdTest):
    """
    Test that the model's F1 score on the validation dataset meets or
    exceeds a predefined threshold.
    """

    category = "model_performance"
    name = "f1_score"
    default_params = {"min_threshold": 0.5}

    def run(self):
        y_true = self.test_ds.y
        class_pred = self.class_predictions(self.y_test_predict)
        f1_score = metrics.f1_score(y_true, class_pred)

        passed = f1_score > self.params["min_threshold"]
        results = [
            TestResult(
                passed=passed,
                values={
                    "score": f1_score,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))


@dataclass
class MinimumROCAUCScore(ThresholdTest):
    """
    Test that the model's ROC AUC score on the validation dataset meets or
    exceeds a predefined threshold.
    """

    category = "model_performance"
    name = "roc_auc_score"
    default_params = {"min_threshold": 0.5}

    def run(self):
        y_true = self.test_ds.y
        class_pred = self.class_predictions(self.y_test_predict)
        roc_auc = metrics.roc_auc_score(y_true, class_pred)

        passed = roc_auc > self.params["min_threshold"]
        results = [
            TestResult(
                passed=passed,
                values={
                    "score": roc_auc,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))


@dataclass
class TrainingTestDegradation(ThresholdTest):
    """
    Test that the degradation in performance between the training and test datasets
    does not exceed a predefined threshold.
    """

    category = "model_performance"
    name = "training_test_degradation"
    default_params = {"metrics": ["accuracy", "precision", "recall", "f1"]}
    default_metrics = {
        "accuracy": metrics.accuracy_score,
        "precision": partial(metrics.precision_score, zero_division=0),
        "recall": partial(metrics.recall_score, zero_division=0),
        "f1": partial(metrics.f1_score, zero_division=0),
    }

    def run(self):
        y_true = self.test_ds.y

        train_class_pred = self.class_predictions(self.y_train_predict)
        test_class_pred = self.class_predictions(self.y_test_predict)

        metrics_to_compare = self.params["metrics"]
        test_results = []
        for metric in metrics_to_compare:
            metric_fn = self.default_metrics[metric]

            train_score = metric_fn(self.train_ds.y, train_class_pred)
            test_score = metric_fn(y_true, test_class_pred)
            degradation = (train_score - test_score) / train_score

            passed = train_score > test_score
            test_results.append(
                TestResult(
                    test_name=metric,
                    passed=passed,
                    values={
                        "test_score": test_score,
                        "train_score": train_score,
                        "degradation": degradation,
                    },
                )
            )

        return self.cache_results(
            test_results, passed=all([r.passed for r in test_results])
        )


@dataclass
class OverfitDiagnosis(ThresholdTest):
    """
    Test that identify overfit regions with high residuals by histogram slicing techniques.
    """

    category = "model_diagnosis"
    name = "overfit_regions"

    default_params = {"features_columns": None, "cut_off_percentage": 4}
    default_metrics = {
        "accuracy": metrics.accuracy_score,
    }

    def run(self):
        if "cut_off_percentage" not in self.params:
            raise ValueError("cut_off_percentage must be provided in params")
        cut_off_percentage = self.params["cut_off_percentage"]

        if "features_columns" not in self.params:
            raise ValueError("features_columns must be provided in params")

        if self.params["features_columns"] is None:
            features_list = [field_dict["id"] for field_dict in self.train_ds.fields]
            features_list.remove(self.train_ds.target_column)
        else:
            features_list = self.params["features_columns"]

        if not isinstance(features_list, list):
            raise ValueError(
                "features_columns must be a list of features you would like to test"
            )

        target_column = self.train_ds.target_column
        prediction_column = f"{target_column}_pred"

        # Add prediction column in the training dataset
        train_df = self.train_ds.df.copy(deep=True)
        train_class_pred = self.class_predictions(self.y_train_predict)
        train_df[prediction_column] = train_class_pred

        # Add prediction column in the test dataset
        test_df = self.test_ds.df.copy(deep=True)
        test_class_pred = self.class_predictions(self.y_test_predict)
        test_df[prediction_column] = test_class_pred

        test_results = []
        test_figures = []
        results_headers = ["slice", "shape"]
        results_headers.extend(self.default_metrics.keys())

        for feature_column in features_list:
            train_df["bin"] = pd.cut(train_df[feature_column], bins=10)
            results_train = {k: [] for k in results_headers}
            results_test = {k: [] for k in results_headers}

            for region, df_region in train_df.groupby("bin"):
                self._compute_metrics(
                    results_train, region, df_region, target_column, prediction_column
                )
                df_test_region = test_df[
                    (test_df[feature_column] > region.left)
                    & (test_df[feature_column] <= region.right)
                ]
                self._compute_metrics(
                    results_test,
                    region,
                    df_test_region,
                    target_column,
                    prediction_column,
                )

            results = self._prepare_results(results_train, results_test)

            fig = self._plot_overfit_regions(
                results, feature_column, "accuracy", threshold=cut_off_percentage
            )
            # We're currently plotting accuracy gap only
            test_figures.append(
                Figure(
                    key=f"{self.name}:accuracy:{feature_column}",
                    figure=fig,
                    metadata={
                        "cut_off_percentage": cut_off_percentage,
                        "key": self.name,
                        "metric": "accuracy",
                        "feature": feature_column,
                    },
                )
            )

            results = results[results["gap"] > cut_off_percentage]
            passed = results.empty
            results = results.to_dict(orient="list")
            test_results.append(
                TestResult(
                    test_name="accuracy",
                    column=feature_column,
                    passed=passed,
                    values=results,
                )
            )
        return self.cache_results(
            test_results,
            passed=all([r.passed for r in test_results]),
            figures=test_figures,
        )

    def _prepare_results(self, results_train: dict, results_test: dict) -> pd.DataFrame:
        """
        Prepares and returns a DataFrame with training and testing results.

        Args:
            results_train (dict): A dictionary containing training results.
            results_test (dict): A dictionary containing testing results.

        Returns:
            pd.DataFrame: A DataFrame containing the following columns:
                - 'shape': The number of training records used.
                - 'slice': The name of the region being evaluated.
                - 'training accuracy': The accuracy achieved on the training data (in percentage).
                - 'test accuracy': The accuracy achieved on the testing data (in percentage).
                - 'gap': The difference between the training and testing accuracies (in percentage).
        """

        results_train = pd.DataFrame(results_train)
        results_test = pd.DataFrame(results_test)
        results = results_train.copy(deep=True)
        results.rename(
            columns={"shape": "training records", "accuracy": "training accuracy"},
            inplace=True,
        )
        results["training accuracy"] = results["training accuracy"] * 100
        results["test accuracy"] = results_test["accuracy"] * 100
        results["gap"] = results["training accuracy"] - results["test accuracy"]

        return results

    def _compute_metrics(
        self,
        results: dict,
        region: str,
        df_region: pd.DataFrame,
        target_column: str,
        prediction_column: str,
    ) -> None:
        """
        Computes and appends the evaluation metrics for a given region.

        Args:
            results (dict): A dictionary containing the evaluation results for all regions.
            region (str): The name of the region being evaluated.
            df_region (pd.DataFrame): The DataFrame containing the region-specific data.
            target_column (str): The name of the target column in the DataFrame.
            prediction_column (str): The name of the column containing the model's predictions.

        Returns:
            None
        """

        results["slice"].append(str(region))
        results["shape"].append(df_region.shape[0])

        # Check if df_region is an empty dataframe and if so, append 0 to all metrics
        if df_region.empty:
            for metric in self.default_metrics.keys():
                results[metric].append(0)
            return

        y_true = df_region[target_column].values
        y_prediction = (
            df_region[prediction_column].astype(df_region[target_column].dtypes).values
        )

        for metric, metric_fn in self.default_metrics.items():
            results[metric].append(metric_fn(y_true, y_prediction))

    def _plot_overfit_regions(
        self, df: pd.DataFrame, feature_column: str, metric: str, threshold: float
    ) -> plt.Figure:
        """
        Plots the overfit regions of a given DataFrame.

        Args:
            df (pd.DataFrame): A DataFrame containing the data to plot.
            feature_column (str): The name of the feature column to plot.
            threshold (float): The threshold value for the gap, above which a region is considered to be overfit.

        Returns:
            plt.Figure: A matplotlib Figure object containing the plot.
        """

        # Create a bar plot using seaborn library
        fig, ax = plt.subplots()
        barplot = sns.barplot(data=df, x="slice", y="gap", ax=ax)
        ax.tick_params(axis="x", rotation=90)
        # Draw threshold line
        axhline = ax.axhline(
            y=threshold,
            color="red",
            linestyle="--",
            linewidth=1,
            label=f"Cut-Off Percentage: {threshold}%",
        )
        ax.tick_params(axis="x", labelsize=20)
        ax.tick_params(axis="y", labelsize=20)

        ax.set_ylabel(f"{metric.capitalize()} Gap (%)", weight="bold", fontsize=22)
        ax.set_xlabel("Slice/Segments", weight="bold", fontsize=22)
        ax.set_title(
            f"Overfit regions in feature column: {feature_column}",
            weight="bold",
            fontsize=24,
        )

        # Get the legend handles and labels from the barplot
        handles, labels = barplot.get_legend_handles_labels()

        # Append the axhline handle and label
        handles.append(axhline)
        labels.append(axhline.get_label())

        # Create a legend with both hue and axhline labels, the threshold line
        # will show up twice so remove the first element
        # barplot.legend(handles=handles[:-1], labels=labels, loc="upper right")
        barplot.legend(
            handles=handles[:-1],
            labels=labels,
            loc="upper center",
            bbox_to_anchor=(0.5, 0.1),
            ncol=len(handles),
        )

        # Do this if you want to prevent the figure from being displayed
        plt.close("all")

        return fig


@dataclass
class WeakspotsDiagnosis(ThresholdTest):
    """
    Test that identify weak regions with high residuals by histogram slicing techniques.
    """

    category = "model_diagnosis"
    name = "weak_spots"

    default_params = {
        "features_columns": None,
        # Some default values that the user should override
        "thresholds": {
            "accuracy": 0.75,
            "precision": 0.5,
            "recall": 0.5,
            "f1": 0.7,
        },
    }
    # TODO: allow configuring
    default_metrics = {
        "accuracy": metrics.accuracy_score,
        "precision": partial(metrics.precision_score, zero_division=0),
        "recall": partial(metrics.recall_score, zero_division=0),
        "f1": partial(metrics.f1_score, zero_division=0),
    }

    def run(self):
        thresholds = self.params["thresholds"]

        # Ensure there is a threshold for each metric
        for metric in self.default_metrics.keys():
            if metric not in thresholds:
                raise ValueError(f"Threshold for metric {metric} is missing")

        if "features_columns" not in self.params:
            raise ValueError("features_columns must be provided in params")

        if self.params["features_columns"] is None:
            features_list = [field_dict["id"] for field_dict in self.train_ds.fields]
            features_list.remove(self.train_ds.target_column)
        else:
            features_list = self.params["features_columns"]

        target_column = self.train_ds.target_column
        prediction_column = f"{target_column}_pred"

        train_df = self.train_ds.df.copy(deep=True)
        train_class_pred = self.class_predictions(self.y_train_predict)
        train_df[prediction_column] = train_class_pred

        test_df = self.test_ds.df.copy(deep=True)
        test_class_pred = self.class_predictions(self.y_test_predict)
        test_df[prediction_column] = test_class_pred

        test_results = []
        test_figures = []
        results_headers = ["slice", "shape"]
        results_headers.extend(self.default_metrics.keys())
        for feature in features_list:
            train_df["bin"] = pd.cut(train_df[feature], bins=10)
            results_train = {k: [] for k in results_headers}
            results_test = {k: [] for k in results_headers}

            for region, df_region in train_df.groupby("bin"):
                self._compute_metrics(
                    results_train, region, df_region, target_column, prediction_column
                )
                df_test_region = test_df[
                    (test_df[feature] > region.left)
                    & (test_df[feature] <= region.right)
                ]
                self._compute_metrics(
                    results_test,
                    region,
                    df_test_region,
                    target_column,
                    prediction_column,
                )

            # Make one plot per metric
            for metric in self.default_metrics.keys():
                fig, df = self._plot_weak_spots(
                    results_train,
                    results_test,
                    feature,
                    metric=metric,
                    threshold=thresholds[metric],
                )

                test_figures.append(
                    Figure(
                        key=f"{self.name}:{metric}:{feature}",
                        figure=fig,
                        metadata={
                            "threshold": thresholds[metric],
                            "key": self.name,
                            "metric": metric,
                            "feature": feature,
                        },
                    )
                )

            # For simplicity, test has failed if any of the metrics is below the threshold. We will
            # rely on visual assessment for this test for now.
            results_passed = df[df[list(thresholds.keys())].lt(thresholds).any(axis=1)]

            passed = results_passed.empty
            results = pd.concat(
                [pd.DataFrame(results_train), pd.DataFrame(results_test)]
            ).to_dict(orient="list")

            test_results.append(
                TestResult(
                    test_name="accuracy",
                    column=feature,
                    passed=passed,
                    values=results,
                )
            )
        return self.cache_results(
            test_results,
            passed=all([r.passed for r in test_results]),
            figures=test_figures,
        )

    def _compute_metrics(
        self,
        results: dict,
        region: str,
        df_region: pd.DataFrame,
        target_column: str,
        prediction_column: str,
    ) -> None:
        """
        Computes and appends the default metrics for a given DataFrame slice to the results dictionary.

        Args:
            results (dict): A dictionary to which the computed metrics will be appended.
            region (str): A string identifier for the DataFrame slice being evaluated.
            df_region (pd.DataFrame): A pandas DataFrame slice containing the data to evaluate.
            target_column (str): The name of the target column to use for computing the metrics.
            prediction_column (str): The name of the prediction column to use for computing the metrics.

        Returns:
            None: The computed metrics are appended to the `results` dictionary in-place.
        """
        results["slice"].append(str(region))
        results["shape"].append(df_region.shape[0])

        # Check if df_region is an empty dataframe and if so, append 0 to all metrics
        if df_region.empty:
            for metric in self.default_metrics.keys():
                results[metric].append(0)
            return

        y_true = df_region[target_column].values
        y_prediction = (
            df_region[prediction_column].astype(df_region[target_column].dtypes).values
        )

        for metric, metric_fn in self.default_metrics.items():
            results[metric].append(metric_fn(y_true, y_prediction))

    def _plot_weak_spots(
        self, results_train, results_test, feature_column, metric, threshold
    ):
        """
        Plots the metric of the training and test datasets for each region in a given feature column,
        and highlights regions where the score is below a specified threshold.

        Args:
            results_train (list of dict): The results of the model on the training dataset, as a list of dictionaries.
            results_test (list of dict): The results of the model on the test dataset, as a list of dictionaries.
            feature_column (str): The name of the feature column being analyzed.
            metric (str): The name of the metric to plot.
            threshold (float): The minimum accuracy threshold to be highlighted on the plot.

        Returns:
            fig (matplotlib.figure.Figure): The figure object containing the plot.
            df (pandas.DataFrame): The concatenated dataframe containing the training and test results.
        """
        # Concat training and test datasets
        results_train = pd.DataFrame(results_train)
        results_test = pd.DataFrame(results_test)
        dataset_type_column = "Dataset Type"
        results_train[dataset_type_column] = "Training"
        results_test[dataset_type_column] = "Test"
        df = pd.concat([results_train, results_test])

        # Create a bar plot using seaborn library
        fig, ax = plt.subplots()
        barplot = sns.barplot(
            data=df,
            x="slice",
            y=metric,
            hue=dataset_type_column,
            edgecolor="black",
            ax=ax,
        )
        ax.tick_params(axis="x", rotation=90)
        for p in ax.patches:
            t = ax.annotate(
                str("{:.2f}%".format(p.get_height())),
                xy=(p.get_x() + 0.03, p.get_height() + 1),
            )
            t.set(color="black", size=14)

        axhline = ax.axhline(
            y=threshold,
            color="red",
            linestyle="--",
            linewidth=3,
            label=f"Threshold: {threshold}",
        )
        ax.set_ylabel(metric.capitalize(), weight="bold", fontsize=22)
        ax.set_xlabel("Slice/Segments", weight="bold", fontsize=22)
        ax.set_title(
            f"Weak regions in feature column: {feature_column}",
            weight="bold",
            fontsize=24,
        )

        # Get the legend handles and labels from the barplot
        handles, labels = barplot.get_legend_handles_labels()

        # Append the axhline handle and label
        handles.append(axhline)
        labels.append(axhline.get_label())

        # Create a legend with both hue and axhline labels, the threshold line
        # will show up twice so remove the first element
        # barplot.legend(handles=handles[:-1], labels=labels, loc="upper right")
        barplot.legend(
            handles=handles[:-1],
            labels=labels,
            loc="upper center",
            bbox_to_anchor=(0.5, 0.1),
            ncol=len(handles),
        )

        # Do this if you want to prevent the figure from being displayed
        plt.close("all")

        return fig, df


@dataclass
class RobustnessDiagnosis(ThresholdTest):
    """
    Test robustness of model by perturbing the features column values
    """

    category = "model_diagnosis"
    name = "robustness"

    default_params = {
        "features_columns": None,
        "scaling_factor_std_dev_list": [0.01, 0.02],
    }
    default_metrics = {
        "accuracy": metrics.accuracy_score,
    }

    def run(self):
        # Validate X std deviation parameter
        if "scaling_factor_std_dev_list" not in self.params:
            raise ValueError("scaling_factor_std_dev_list must be provided in params")
        x_std_dev_list = self.params["scaling_factor_std_dev_list"]

        # Validate list of features columns need to be perterubed
        if "features_columns" not in self.params:
            raise ValueError("features_columns must be provided in params")

        # Identify numeric features
        numeric_features_columns = [
            field_dic["id"]
            for field_dic in self.train_ds.fields
            if field_dic["type"] == "Numeric"
        ]
        if self.params["features_columns"] is None:
            features_list = numeric_features_columns
        else:
            features_list = self.params["features_columns"]

        # Remove target column if it exist in the list
        if self.train_ds.target_column in features_list:
            features_list.remove(self.train_ds.target_column)

        train_df = self.train_ds.x.copy(deep=True)
        train_y_true = self.train_ds.y

        test_df = self.test_ds.x.copy(deep=True)
        test_y_true = self.test_ds.y

        test_results = []
        test_figures = []

        results_headers = ["Perturbation Size", "Dataset Type", "Records"]
        results_headers.extend(self.default_metrics.keys())
        results = {k: [] for k in results_headers}

        # Iterate scaling factor for the standard deviation list
        for x_std_dev in x_std_dev_list:
            temp_train_df = train_df.copy(deep=True)
            temp_test_df = test_df.copy(deep=True)

            # Add noise to numeric features columns provided by user
            for feature in features_list:
                temp_train_df[feature] = self.add_noise_std_dev(
                    temp_train_df[feature].to_list(), x_std_dev
                )
                temp_test_df[feature] = self.add_noise_std_dev(
                    temp_test_df[feature].to_list(), x_std_dev
                )

            self._compute_metrics(
                results, temp_train_df, train_y_true, x_std_dev, "Traning"
            )
            self._compute_metrics(results, temp_test_df, test_y_true, x_std_dev, "Test")

        fig, df = self._plot_robustness(results, features_list)

        test_figures.append(
            Figure(
                key=f"{self.name}:accuracy",
                figure=fig,
                metadata={
                    "key": self.name,
                    "metric": "accuracy",
                    "features_list": features_list,
                },
            )
        )

        test_results.append(
            TestResult(
                test_name="accuracy",
                column=features_list[0],
                passed=True,
                values=df.to_dict(orient="list"),
            )
        )
        return self.cache_results(test_results, passed=True, figures=test_figures)

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
        y_prediction = self.model.predict(df)
        y_prediction = [round(value) for value in y_prediction]
        for metric, metric_fn in self.default_metrics.items():
            results[metric].append(metric_fn(y_true.values, y_prediction) * 100)

    def add_noise_std_dev(
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
        ax.set_ylabel("Accuracy", weight="bold", fontsize=22)
        ax.legend(fontsize=22)
        ax.set_xlabel(
            "Perturbation Size ( X * Standard Deviation)", weight="bold", fontsize=22
        )
        ax.set_title(
            f"Perturbed Features: {', '.join(features_columns)}",
            weight="bold",
            fontsize=24,
        )

        # Do this if you want to prevent the figure from being displayed
        plt.close("all")

        # fig, ax = plt.subplots()
        return fig, df
