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

from ...vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
)


@dataclass
class MinimumAccuracy(ThresholdTest):
    """
    Test that the model's prediction accuracy on a dataset meets or
    exceeds a predefined threshold.
    """

    category = "model_performance"
    name = "accuracy_score"
    required_context = ["model"]
    default_params = {"min_threshold": 0.7}

    def summary(self, results: List[TestResult], all_passed: bool):
        """
        The accuracy score test returns results like these:
        [{"values": {"score": 0.734375, "threshold": 0.7}, "passed": true}]
        """
        result = results[0]
        results_table = [
            {
                "Score": result.values["score"],
                "Threshold": result.values["threshold"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pd.DataFrame(results_table),
                    metadata=ResultTableMetadata(
                        title="Minimum Accuracy Test on Test Data"
                    ),
                )
            ]
        )

    def run(self):
        y_true = self.model.test_ds.y
        class_pred = self.model.class_predictions(self.model.y_test_predict)
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
    required_context = ["model"]
    default_params = {"min_threshold": 0.5}

    def summary(self, results: List[TestResult], all_passed: bool):
        """
        The f1 score test returns results like these:
        [{"values": {"score": 0.734375, "threshold": 0.7}, "passed": true}]
        """
        result = results[0]
        results_table = [
            {
                "Score": result.values["score"],
                "Threshold": result.values["threshold"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pd.DataFrame(results_table),
                    metadata=ResultTableMetadata(title="Minimum F1 Score Test"),
                )
            ]
        )

    def run(self):
        y_true = self.model.test_ds.y
        class_pred = self.model.class_predictions(self.model.y_test_predict)
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
    required_context = ["model"]
    default_params = {"min_threshold": 0.5}

    def summary(self, results: List[TestResult], all_passed: bool):
        """
        The roc auc score test returns results like these:
        [{"values": {"score": 0.734375, "threshold": 0.7}, "passed": true}]
        """
        result = results[0]
        results_table = [
            {
                "Score": result.values["score"],
                "Threshold": result.values["threshold"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pd.DataFrame(results_table),
                    metadata=ResultTableMetadata(title="Minimum ROC AUC Score Test"),
                )
            ]
        )

    def run(self):
        y_true = self.model.test_ds.y
        class_pred = self.model.class_predictions(self.model.y_test_predict)
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
    required_context = ["model"]

    default_params = {
        "metrics": ["accuracy", "precision", "recall", "f1"],
        "max_threshold": 0.10,  # Maximum 10% degradation
    }
    default_metrics = {
        "accuracy": metrics.accuracy_score,
        "precision": partial(metrics.precision_score, zero_division=0),
        "recall": partial(metrics.recall_score, zero_division=0),
        "f1": partial(metrics.f1_score, zero_division=0),
    }

    def summary(self, results: List[TestResult], all_passed: bool):
        """
        The training test degradation test returns results like these:
        [{"values":
            {"test_score": 0.7225, "train_score": 0.7316666666666667, "degradation": 0.012528473804100214}, "test_name": "accuracy", "passed": true}, ...]
        """
        results_table = [
            {
                "Metric": result.test_name.title(),
                "Train Score": result.values["train_score"],
                "Test Score": result.values["test_score"],
                "Degradation (%)": result.values["degradation"] * 100,
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pd.DataFrame(results_table),
                    metadata=ResultTableMetadata(
                        title="Training-Test Degradation Test"
                    ),
                )
            ]
        )

    def run(self):
        y_true = self.model.test_ds.y

        train_class_pred = self.model.class_predictions(self.model.y_train_predict)
        test_class_pred = self.model.class_predictions(self.model.y_test_predict)

        metrics_to_compare = self.params["metrics"]
        test_results = []
        for metric in metrics_to_compare:
            metric_fn = self.default_metrics[metric]

            train_score = metric_fn(self.model.train_ds.y, train_class_pred)
            test_score = metric_fn(y_true, test_class_pred)
            degradation = (train_score - test_score) / train_score

            passed = degradation < self.params["max_threshold"]
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
    required_context = ["model", "model.train_ds", "model.test_ds"]

    default_params = {"features_columns": None, "cut_off_percentage": 4}
    default_metrics = {
        "accuracy": metrics.accuracy_score,
    }

    def description(self):
        return """
        Test that identify overfitting regions based on the train-test performance gap,
        one can divide the feature space into regions and analyze the train-test performance
        gap for each region. Regions with a large train-test performance gap can be considered as
        overfitting regions, indicating that the model is overfitting in those regions.

        Once overfitting regions have been identified, one can use various techniques to address the overfitting.
        For example, one could use regularization techniques such as L1 or L2 regularization, dropout, or early
        stopping to prevent the model from overfitting. Alternatively, one could use data augmentation techniques
        to increase the size of the training data and reduce overfitting.

        Overall, analyzing the train-test performance gap can provide valuable insights into the performance of
        a machine learning model and help identify overfitting regions that need to be addressed to improve
        the model's generalization performance.
        """

    def run(self):
        if "cut_off_percentage" not in self.params:
            raise ValueError("cut_off_percentage must be provided in params")
        cut_off_percentage = self.params["cut_off_percentage"]

        if "features_columns" not in self.params:
            raise ValueError("features_columns must be provided in params")

        if self.model is None:
            raise ValueError("model must of provided to run this test")

        if self.params["features_columns"] is None:
            features_list = self.model.train_ds.get_features_columns()
        else:
            features_list = self.params["features_columns"]

        # Check if all elements from features_list are present in the feature columns
        all_present = all(
            elem in self.model.train_ds.get_features_columns() for elem in features_list
        )
        if not all_present:
            raise ValueError(
                "The list of feature columns provided do not match with training dataset feature columns"
            )

        if not isinstance(features_list, list):
            raise ValueError(
                "features_columns must be a list of features you would like to test"
            )

        target_column = self.model.train_ds.target_column
        prediction_column = f"{target_column}_pred"

        # Add prediction column in the training dataset
        train_df = self.model.train_ds.df.copy()
        train_class_pred = self.model.class_predictions(self.model.y_train_predict)
        train_df[prediction_column] = train_class_pred

        # Add prediction column in the test dataset
        test_df = self.model.test_ds.df.copy()
        test_class_pred = self.model.class_predictions(self.model.y_test_predict)
        test_df[prediction_column] = test_class_pred

        test_results = []
        test_figures = []
        results_headers = ["slice", "shape", "feature"]
        results_headers.extend(self.default_metrics.keys())

        for feature_column in features_list:
            bins = 10
            if feature_column in self.model.train_ds.get_categorical_features_columns():
                bins = len(train_df[feature_column].unique())
            train_df["bin"] = pd.cut(train_df[feature_column], bins=bins)

            results_train = {k: [] for k in results_headers}
            results_test = {k: [] for k in results_headers}

            for region, df_region in train_df.groupby("bin"):
                self._compute_metrics(
                    results_train,
                    region,
                    df_region,
                    target_column,
                    prediction_column,
                    feature_column,
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
                    feature_column,
                )

            results = self._prepare_results(results_train, results_test)

            fig = self._plot_overfit_regions(
                results, feature_column, "accuracy", threshold=cut_off_percentage
            )
            # We're currently plotting accuracy gap only
            test_figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.name}:accuracy:{feature_column}",
                    figure=fig,
                    metadata={
                        "metric": "accuracy",
                        "cut_off_percentage": cut_off_percentage,
                        "feature": feature_column,
                    },
                )
            )

            results = results[results["gap"] > cut_off_percentage]
            passed = results.empty
            results = results.to_dict(orient="records")
            test_results.append(
                TestResult(
                    test_name="accuracy",
                    column=feature_column,
                    passed=passed,
                    values={"records": results},
                )
            )
        return self.cache_results(
            test_results,
            passed=all([r.passed for r in test_results]),
            figures=test_figures,
        )

    def summary(self, results: List[TestResult], all_passed: bool):
        results_table = [
            record for result in results for record in result.values["records"]
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(title="Overfit Regions Data"),
                )
            ]
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
        results = results_train.copy()
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
        feature_column: str,
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
        results["feature"].append(feature_column)

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
    required_context = ["model", "model.train_ds", "model.test_ds"]

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

    def description(self):
        return """
        A weak spots test is a type of testing that is performed on a machine learning model
        to identify areas where the model may not perform well or may be vulnerable to errors.
        The purpose of this testing is to identify the limitations and weaknesses of the model
        so that appropriate measures can be taken to improve its performance.
        The weak spots test typically involves subjecting the model to different types of data
        that are different from the data used to train the model. For example, the test data may
        contain outliers, missing data, or noise that was not present in the training data. The model
        is then evaluated on this test data using appropriate metrics such as accuracy, precision,
        recall, F1 score, etc.
        """

    def run(self):
        thresholds = self.params["thresholds"]

        # Ensure there is a threshold for each metric
        for metric in self.default_metrics.keys():
            if metric not in thresholds:
                raise ValueError(f"Threshold for metric {metric} is missing")

        if self.model is None:
            raise ValueError("model must of provided to run this test")

        if self.params["features_columns"] is None:
            features_list = self.model.train_ds.get_features_columns()
        else:
            features_list = self.params["features_columns"]

        # Check if all elements from features_list are present in the feature columns
        all_present = all(
            elem in self.model.train_ds.get_features_columns() for elem in features_list
        )
        if not all_present:
            raise ValueError(
                "The list of feature columns provided do not match with "
                + "training dataset feature columns"
            )

        target_column = self.model.train_ds.target_column
        prediction_column = f"{target_column}_pred"

        train_df = self.model.train_ds.df.copy()
        train_class_pred = self.model.class_predictions(self.model.y_train_predict)
        train_df[prediction_column] = train_class_pred

        test_df = self.model.test_ds.df.copy()
        test_class_pred = self.model.class_predictions(self.model.y_test_predict)
        test_df[prediction_column] = test_class_pred

        test_results = []
        test_figures = []
        results_headers = ["slice", "shape", "feature"]
        results_headers.extend(self.default_metrics.keys())
        for feature in features_list:
            bins = 10
            if feature in self.model.train_ds.get_categorical_features_columns():
                bins = len(train_df[feature].unique())
            train_df["bin"] = pd.cut(train_df[feature], bins=bins)

            results_train = {k: [] for k in results_headers}
            results_test = {k: [] for k in results_headers}

            for region, df_region in train_df.groupby("bin"):
                self._compute_metrics(
                    results_train,
                    region,
                    df_region,
                    target_column,
                    prediction_column,
                    feature,
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
                    feature,
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
                        for_object=self,
                        key=f"{self.name}:{metric}:{feature}",
                        figure=fig,
                        metadata={
                            "metric": metric,
                            "threshold": thresholds[metric],
                            "feature": feature,
                        },
                    )
                )

            # For simplicity, test has failed if any of the metrics is below the threshold. We will
            # rely on visual assessment for this test for now.
            results_passed = df[df[list(thresholds.keys())].lt(thresholds).any(axis=1)]
            passed = results_passed.empty

            test_results.append(
                TestResult(
                    test_name="accuracy",
                    column=feature,
                    passed=passed,
                    values={"records": df.to_dict("records")},
                )
            )
        return self.cache_results(
            test_results,
            passed=all([r.passed for r in test_results]),
            figures=test_figures,
        )

    def summary(self, results: List[TestResult], all_passed: bool):
        results_table = [
            record for result in results for record in result.values["records"]
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(title="Weakspots Test"),
                )
            ]
        )

    def _compute_metrics(
        self,
        results: dict,
        region: str,
        df_region: pd.DataFrame,
        target_column: str,
        prediction_column: str,
        feature_column: str,
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
        results["feature"].append(feature_column)

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
        features_list = [
            col for col in features_list if col != self.model.train_ds.target_column
        ]

        train_df = self.model.train_ds.x.copy()
        train_y_true = self.model.train_ds.y

        test_df = self.model.test_ds.x.copy()
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
        y_prediction = self.model.predict(df)
        y_prediction = self.model.class_predictions(y_prediction)
        for metric, metric_fn in self.default_metrics.items():
            results[metric].append(metric_fn(y_true.values, y_prediction) * 100)

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
        ax.set_ylabel("Accuracy", weight="bold", fontsize=22)
        ax.legend(fontsize=22)
        ax.set_xlabel(
            "Perturbation Size (X * Standard Deviation)", weight="bold", fontsize=22
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
