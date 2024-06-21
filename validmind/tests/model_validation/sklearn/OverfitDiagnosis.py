# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

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
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class OverfitDiagnosis(ThresholdTest):
    """
    Detects and visualizes overfit regions in an ML model by comparing performance on training and test datasets.

    **Purpose**: The OverfitDiagnosis test is devised to detect areas within a Machine Learning model that might be
    prone to overfitting. It achieves this by comparing the model's performance on both the training and testing
    datasets. These datasets are broken down into distinct sections defined by a Feature Space. Areas, where the model
    underperforms by displaying high residual values or a significant amount of overfitting, are highlighted, prompting
    actions for mitigation using regularization techniques such as L1 or L2 regularization, Dropout, Early Stopping or
    data augmentation.

    **Test Mechanism**: The metric conducts the test by executing the method 'run' on the default parameters and
    metrics with 'accuracy' as the specified metric. It segments the feature space by binning crucial feature columns
    from both the training and testing datasets. Then, the method computes the prediction results for each defined
    region. Subsequently, the prediction's efficacy is evaluated, i.e., the model's performance gap (defined as the
    discrepancy between the actual and the model's predictions) for both datasets is calculated and compared with a
    preset cut-off value for the overfitting condition. A test failure presents an overfit model, whereas a pass
    signifies a fit model. Meanwhile, the function also prepares figures further illustrating the regions with
    overfitting.

    **Signs of High Risk**: Indicators of a high-risk model are:
    - A high 'gap' value indicating discrepancies in the training and testing data accuracy signals an overfit model.
    - Multiple or vast overfitting zones within the feature space suggest overcomplication of the model.

    **Strengths**:
    - Presents a visual perspective by plotting regions with overfit issues, simplifying understanding of the model
    structure.
    - Permits a feature-focused assessment, which promotes specific, targeted modifications to the model.
    - Caters to modifications of the testing parameters such as 'cut_off_percentage' and 'features_column' enabling a
    personalized analysis.
    - Handles both numerical and categorical features.

    **Limitations**:
    - Does not currently support regression tasks and is limited to classification tasks only.
    - Ineffectual for text-based features, which in turn restricts its usage for Natural Language Processing models.
    - Primarily depends on the bins setting, responsible for segmenting the feature space. Different bin configurations
    might yield varying results.
    - Utilization of a fixed cut-off percentage for making overfitting decisions, set arbitrarily, leading to a
    possible risk of inaccuracy.
    - Limitation of performance metrics to accuracy alone might prove inadequate for detailed examination, especially
    for imbalanced datasets.
    """

    name = "overfit_regions"
    required_inputs = ["model", "datasets"]
    default_params = {"features_columns": None, "cut_off_percentage": 4}
    tasks = ["classification", "text_classification"]
    tags = [
        "sklearn",
        "binary_classification",
        "multiclass_classification",
        "model_diagnosis",
    ]

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
            features_list = self.inputs.datasets[0].feature_columns
        else:
            features_list = self.params["features_columns"]

        if self.inputs.datasets[0].text_column in features_list:
            raise ValueError(
                "Skiping Overfit Diagnosis test for the dataset with text column"
            )

        # Check if all elements from features_list are present in the feature columns
        all_present = all(
            elem in self.inputs.datasets[0].feature_columns for elem in features_list
        )
        if not all_present:
            raise ValueError(
                "The list of feature columns provided do not match with training dataset feature columns"
            )

        if not isinstance(features_list, list):
            raise ValueError(
                "features_columns must be a list of features you would like to test"
            )

        target_column = self.inputs.datasets[0].target_column
        prediction_column = f"{target_column}_pred"

        # Add prediction column in the training dataset
        train_df = self.inputs.datasets[0].df.copy()
        train_class_pred = self.inputs.datasets[0].y_pred(self.inputs.model)
        train_df[prediction_column] = train_class_pred

        # Add prediction column in the test dataset
        test_df = self.inputs.datasets[1].df.copy()
        test_class_pred = self.inputs.datasets[1].y_pred(self.inputs.model)
        test_df[prediction_column] = test_class_pred

        test_results = []
        test_figures = []
        results_headers = ["slice", "shape", "feature"]
        results_headers.extend(self.default_metrics.keys())

        for feature_column in features_list:
            bins = 10
            if feature_column in self.inputs.datasets[0].feature_columns_categorical:
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
                ThresholdTestResult(
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

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
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
