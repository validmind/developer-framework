# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt
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
        model_library = Model.model_library(self.model.model)
        if model_library == "statsmodels" or model_library == "pytorch":
            print(f"Skiping Overfit Diagnosis test for {model_library} models")
            return

        if "cut_off_percentage" not in self.params:
            raise ValueError("cut_off_percentage must be provided in params")
        cut_off_percentage = self.params["cut_off_percentage"]

        if "features_columns" not in self.params:
            raise ValueError("features_columns must be provided in params")

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

        ax.set_ylabel(f"{metric.capitalize()} Gap (%)", weight="bold", fontsize=18)
        ax.set_xlabel("Slice/Segments", weight="bold", fontsize=18)
        ax.set_title(
            f"Overfit regions in feature column: {feature_column}",
            weight="bold",
            fontsize=20,
            wrap=True,
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
