"""
Metrics functions models trained with sklearn or that provide
a sklearn-like API
"""
import warnings
from dataclasses import dataclass
from functools import partial

import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import shap
from sklearn import metrics
from sklearn.inspection import permutation_importance

from ...vm_models import (
    Figure,
    Metric,
    Model,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)
from ...utils import format_number


@dataclass
class ConfusionMatrix(Metric):
    """
    Confusion Matrix
    """

    name = "confusion_matrix"
    required_context = ["model"]

    def description(self):
        return """
        A confusion matrix is a table that is used to describe the performance of a classification
        model. For metrics such as **True Positives (TP)** and **True Negatives (TN)**, the higher their
        values the better as the model is able to distinguish the correct class from the incorrect
        class more effectively. For **False Positives (FP)** and **False Negatives (FN)**, the lower
        their values the better.
        """

    def run(self):
        y_true = self.model.test_ds.y
        y_labels = list(map(lambda x: x.item(), y_true.unique()))
        y_labels.sort()

        class_pred = self.model.class_predictions(self.model.y_test_predict)

        cm = metrics.confusion_matrix(y_true, class_pred, labels=y_labels)
        tn, fp, fn, tp = cm.ravel()

        # Custom text to display on the heatmap cells
        text = [
            [
                f"<b>True Negatives (TN)</b><br />{tn}",
                f"<b>False Positives (FP)</b><br />{fp}",
            ],
            [
                f"<b>False Negatives (FN)</b><br />{fn}",
                f"<b>True Positives (TP)</b><br />{tp}",
            ],
        ]

        fig = ff.create_annotated_heatmap(
            [[tn, fp], [fn, tp]],
            x=[0, 1],
            y=[0, 1],
            colorscale="Blues",
            annotation_text=text,
        )
        # Reverse the xaxis so that 1 is on the left
        fig["layout"]["xaxis"]["autorange"] = "reversed"

        fig["data"][0][
            "hovertemplate"
        ] = "True Label:%{y}<br>Predicted Label:%{x}<br>Count:%{z}<extra></extra>"

        fig.update_layout(
            xaxis=dict(title="Predicted label", constrain="domain"),
            yaxis=dict(title="True label", scaleanchor="x", scaleratio=1),
            autosize=False,
            width=600,
            height=600,
        )

        return self.cache_results(
            metric_value={
                "tn": tn,
                "fp": fp,
                "fn": fn,
                "tp": tp,
            },
            figures=[
                Figure(
                    for_object=self,
                    key="confusion_matrix",
                    figure=fig,
                )
            ],
        )


@dataclass
class PermutationFeatureImportance(Metric):
    """
    Permutation Feature Importance
    """

    name = "pfi"
    required_context = ["model"]

    def description(self):
        return """
        The Feature Importance plot below calculates a score representing the
        importance of each feature in the model. A higher score indicates
        that the specific input feature will have a larger effect on the
        predictive power of the model.

        The importance score is calculated using Permutation Feature
        Importance. Permutation feature importance measures the decrease of
        model performance after the feature''s values have been permuted, which
        breaks the relationship between the feature and the true outcome. A
        feature is "important" if shuffling its values increases the model
        error, because in this case the model relied on the feature for the
        prediction. A feature is "unimportant" if shuffling its values leaves
        the model error unchanged, because in this case the model ignored the
        feature for the prediction.
        """

    def run(self):
        x = self.model.train_ds.x
        y = self.model.train_ds.y

        model_instance = self.model.model
        model_library = Model.model_library(model_instance)
        if model_library == "statsmodels" or model_library == "pytorch":
            print(f"Skiping PFI for {model_library} models")
            return

        # Check if the model has a fit method. This works for statsmodels
        # if not hasattr(model_instance, "fit"):
        #     model_instance.fit = lambda **kwargs: None

        pfi_values = permutation_importance(
            model_instance,
            x,
            y,
            random_state=0,
            n_jobs=-2,
            # scoring="neg_mean_squared_log_error",
        )
        pfi = {}
        for i, column in enumerate(x.columns):
            pfi[column] = [pfi_values["importances_mean"][i]], [
                pfi_values["importances_std"][i]
            ]

        sorted_idx = pfi_values.importances_mean.argsort()
        fig, ax = plt.subplots()
        ax.barh(
            x.columns[sorted_idx], pfi_values.importances[sorted_idx].mean(axis=1).T
        )
        ax.set_title("Permutation Importances (test set)")

        return self.cache_results(
            metric_value=pfi,
            figures=[
                Figure(
                    for_object=self,
                    key="pfi",
                    figure=fig,
                ),
            ],
        )


@dataclass
class PrecisionRecallCurve(Metric):
    """
    Precision Recall Curve
    """

    name = "pr_curve"
    required_context = ["model"]

    def description(self):
        return """
        The precision-recall curve shows the trade-off between precision and recall for different thresholds.
        A high area under the curve represents both high recall and high precision, where high precision
        relates to a low false positive rate, and high recall relates to a low false negative rate. High scores
        for both show that the classifier is returning accurate results (high precision), as well as returning
        a majority of all positive results (high recall).
        """

    def run(self):
        y_true = self.model.test_ds.df[self.model.test_ds.target_column]
        precision, recall, pr_thresholds = metrics.precision_recall_curve(
            y_true, self.model.y_test_predict
        )

        trace = go.Scatter(
            x=recall,
            y=precision,
            mode="lines",
            name="Precision-Recall Curve",
            line=dict(color="#DE257E"),
        )
        layout = go.Layout(
            title="Precision-Recall Curve",
            xaxis=dict(title="Recall"),
            yaxis=dict(title="Precision"),
        )

        fig = go.Figure(data=[trace], layout=layout)

        return self.cache_results(
            metric_value={
                "precision": precision,
                "recall": recall,
                "thresholds": pr_thresholds,
            },
            figures=[
                Figure(
                    for_object=self,
                    key="pr_curve",
                    figure=fig,
                )
            ],
        )


@dataclass
class ClassifierPerformance(Metric):
    """
    Test that outputs the performance of the model on the training or test data.
    """

    default_params = {"metrics": ["accuracy", "precision", "recall", "f1", "roc_auc"]}
    default_metrics = {
        "accuracy": metrics.accuracy_score,
        "precision": partial(metrics.precision_score, zero_division=0),
        "recall": partial(metrics.recall_score, zero_division=0),
        "f1": partial(metrics.f1_score, zero_division=0),
        "roc_auc": metrics.roc_auc_score,
    }

    # This will need to be moved to the backend
    metric_definitions = {
        "accuracy": "Overall, how often is the model correct?",
        "precision": 'When the model predicts "{target_column}", how often is it correct?',
        "recall": 'When it\'s actually "{target_column}", how often does the model predict "{target_column}"?',
        "f1": "Harmonic mean of precision and recall",
        "roc_auc": "Area under the Receiver Operating Characteristic curve",
    }

    metric_formulas = {
        "accuracy": "TP + TN / (TP + TN + FP + FN)",
        "precision": "TP / (TP + FP)",
        "recall": "TP / (TP + FN)",
        "f1": "2 x (Precision x Recall) / (Precision + Recall)",
        "roc_auc": "TPR / FPR",
    }

    def summary(self, metric_value: dict):
        # Turns the metric value into a table of [{metric_name: value}]
        summary_in_sample_performance = []
        for metric_name, metric_value in metric_value.items():
            summary_in_sample_performance.append(
                {
                    "Metric": metric_name.title(),
                    "Definition": self.metric_definitions[metric_name].format(
                        target_column=self.model.train_ds.target_column
                    ),
                    "Formula": self.metric_formulas[metric_name],
                    "Value": format_number(metric_value),
                }
            )

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_in_sample_performance,
                ),
            ]
        )

    def y_true(self):
        raise NotImplementedError

    def y_pred(self):
        raise NotImplementedError

    def run(self):
        y_true = self.y_true()
        class_pred = self.model.class_predictions(self.y_pred())

        results = {}

        metrics = self.params.get("metrics", self.default_params["metrics"])
        for metric_name in metrics:
            if metric_name not in self.default_metrics:
                raise ValueError(f"Metric {metric_name} not supported.")
            metric_func = self.default_metrics[metric_name]
            results[metric_name] = metric_func(y_true, class_pred)

        return self.cache_results(results)


@dataclass
class ClassifierInSamplePerformance(ClassifierPerformance):
    """
    Test that outputs the performance of the model on the training data.
    """

    name = "classifier_in_sample_performance"
    required_context = ["model", "model.train_ds"]

    def description(self):
        return """
        This section shows the performance of the model on the training data. Popular
        metrics such as the accuracy, precision, recall, F1 score, etc. are
        used to evaluate the model.
        """

    def y_true(self):
        return self.model.train_ds.y

    def y_pred(self):
        return self.model.y_train_predict


@dataclass
class ClassifierOutOfSamplePerformance(ClassifierPerformance):
    """
    Test that outputs the performance of the model on the test data.
    """

    name = "classifier_out_of_sample_performance"
    required_context = ["model", "model.test_ds"]

    def description(self):
        return """
        This section shows the performance of the model on the test data. Popular
        metrics such as the accuracy, precision, recall, F1 score, etc. are
        used to evaluate the model.
        """

    def y_true(self):
        return self.model.test_ds.y

    def y_pred(self):
        return self.model.y_test_predict


@dataclass
class ROCCurve(Metric):
    """
    ROC Curve
    """

    name = "roc_curve"
    required_context = ["model"]

    def description(self):
        return """
        The ROC curve shows the trade-off between the true positive rate (TPR) and false positive rate (FPR)
        for different thresholds. The area under the curve (AUC) is a measure of how well a model can
        distinguish between two groups (e.g. default/non-default). The higher the AUC, the better the model is
        at distinguishing between positive and negative classes.
        """

    def run(self):
        y_true = self.model.test_ds.df[self.model.test_ds.target_column]
        class_pred = self.model.class_predictions(self.model.y_test_predict)
        fpr, tpr, roc_thresholds = metrics.roc_curve(
            y_true, self.model.y_test_predict, drop_intermediate=True
        )
        auc = metrics.roc_auc_score(y_true, class_pred)

        trace0 = go.Scatter(
            x=fpr,
            y=tpr,
            mode="lines",
            name=f"ROC curve (AUC = {auc:.2f})",
            line=dict(color="#DE257E"),
        )
        trace1 = go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Random (AUC = 0.5)",
            line=dict(color="grey", dash="dash"),
        )

        layout = go.Layout(
            title="ROC Curve",
            xaxis=dict(title="False Positive Rate"),
            yaxis=dict(title="True Positive Rate"),
        )

        fig = go.Figure(data=[trace0, trace1], layout=layout)

        return self.cache_results(
            metric_value={
                "auc": auc,
                "fpr": fpr,
                "tpr": tpr,
                "thresholds": roc_thresholds,
            },
            figures=[
                Figure(
                    for_object=self,
                    key="roc_auc_curve",
                    figure=fig,
                )
            ],
        )


@dataclass
class SHAPGlobalImportance(Metric):
    """
    SHAP Global Importance
    """

    required_context = ["model"]
    name = "shap"

    def description(self):
        return """
        The Mean Importance plot below shows the significance of each feature
        based on its absolute Shapley values. As we are measuring global importance,
        the process involves computing the average of these absolute Shapley values
        for each feature throughout the data.

        The Summary Plot displayed further combines the importance of each feature
        with their respective effects. Every dot in this plot represents a Shapley value
        for a certain feature in a particular instance. The y-axis positioning is
        determined by the feature, while the x-axis positioning is decided by the
        Shapley value. The color gradation represents the feature's value, transitioning
        from low to high. Points that overlap are scattered slightly in the y-axis
        direction, giving us an idea of the Shapley values distribution for each feature.
        The features are then arranged based on their importance levels.
        """

    def _generate_shap_plot(self, type_, shap_values, x_test):
        """
        Plots two types of SHAP global importance (SHAP).
        :params type: mean, summary
        :params shap_values: a matrix
        :params x_test:
        """
        plt.close("all")

        # preserve styles
        # mpl.rcParams["grid.color"] = "#CCC"
        ax = plt.axes()
        ax.set_facecolor("white")

        summary_plot_extra_args = {}
        if type_ == "mean":
            summary_plot_extra_args = {"plot_type": "bar"}

        shap.summary_plot(shap_values, x_test, show=False, **summary_plot_extra_args)
        figure = plt.gcf()
        # avoid displaying on notebooks and clears the canvas for the next plot
        plt.close()

        return Figure(
            for_object=self,
            figure=figure,
            key=f"shap:{type_}",
            metadata={"type": type_},
        )

    def run(self):
        model_library = Model.model_library(self.model.model)
        if model_library == "statsmodels" or model_library == "pytorch":
            print(f"Skiping SHAP for {model_library} models")
            return

        trained_model = self.model.model
        model_class = Model.model_class(trained_model)

        # the shap library generates a bunch of annoying warnings that we don't care about
        warnings.filterwarnings("ignore", category=UserWarning)

        # Any tree based model can go here
        if (
            model_class == "XGBClassifier"
            or model_class == "RandomForestClassifier"
            or model_class == "CatBoostClassifier"
        ):
            explainer = shap.TreeExplainer(trained_model)
        elif (
            model_class == "LogisticRegression"
            or model_class == "XGBRegressor"
            or model_class == "LinearRegression"
        ):
            explainer = shap.LinearExplainer(trained_model, self.model.test_ds.x)
        else:
            raise ValueError(f"Model {model_class} not supported for SHAP importance.")

        shap_values = explainer.shap_values(self.model.test_ds.x)

        figures = [
            self._generate_shap_plot("mean", shap_values, self.model.test_ds.x),
            self._generate_shap_plot("summary", shap_values, self.model.test_ds.x),
        ]

        # restore warnings
        warnings.filterwarnings("default", category=UserWarning)

        return self.cache_results(figures=figures)


@dataclass
class PopulationStabilityIndex(Metric):
    """
    Population Stability Index between two datasets
    """

    name = "psi"
    required_context = ["model"]

    def description(self):
        return """
        PSI is a widely-used metric to assess the stability of a predictive model's score distribution when comparing
        two separate samples (usually a development and a validation dataset or two separate time periods). It helps
        determine if a model's performance has changed significantly over time or if there is a major shift in the
        population characteristics.

        In this section, we compare the PSI between the training and test datasets.
        """

    def summary(self, metric_value):
        # Add a table with the PSI values for each feature
        # The data looks like this: [{"initial": 2652, "percent_initial": 0.5525, "new": 830, "percent_new": 0.5188, "psi": 0.0021},...
        psi_table = [
            {
                "Bin": i,
                "Count Initial": values["initial"],
                "Percent Initial (%)": values["percent_initial"] * 100,
                "Count New": values["new"],
                "Percent New (%)": values["percent_new"] * 100,
                "PSI": values["psi"],
            }
            for i, values in enumerate(metric_value)
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=psi_table,
                    metadata=ResultTableMetadata(
                        title="Population Stability Index for Training and Test Datasets"
                    ),
                ),
            ]
        )

    def _get_psi(
        self, score_initial, score_new, num_bins=10, mode="fixed", as_dict=False
    ):
        """
        Taken from:
        https://towardsdatascience.com/checking-model-stability-and-population-shift-with-psi-and-csi-6d12af008783
        """
        eps = 1e-4

        # Sort the data
        score_initial.sort()
        score_new.sort()

        # Prepare the bins
        min_val = min(min(score_initial), min(score_new))
        max_val = max(max(score_initial), max(score_new))
        if mode == "fixed":
            bins = [
                min_val + (max_val - min_val) * (i) / num_bins
                for i in range(num_bins + 1)
            ]
        elif mode == "quantile":
            bins = pd.qcut(score_initial, q=num_bins, retbins=True)[
                1
            ]  # Create the quantiles based on the initial population
        else:
            raise ValueError(
                f"Mode '{mode}' not recognized. Allowed options are 'fixed' and 'quantile'"
            )
        bins[0] = min_val - eps  # Correct the lower boundary
        bins[-1] = max_val + eps  # Correct the higher boundary

        # Bucketize the initial population and count the sample inside each bucket
        bins_initial = pd.cut(score_initial, bins=bins, labels=range(1, num_bins + 1))
        df_initial = pd.DataFrame({"initial": score_initial, "bin": bins_initial})
        grp_initial = df_initial.groupby("bin").count()
        grp_initial["percent_initial"] = grp_initial["initial"] / sum(
            grp_initial["initial"]
        )

        # Bucketize the new population and count the sample inside each bucket
        bins_new = pd.cut(score_new, bins=bins, labels=range(1, num_bins + 1))
        df_new = pd.DataFrame({"new": score_new, "bin": bins_new})
        grp_new = df_new.groupby("bin").count()
        grp_new["percent_new"] = grp_new["new"] / sum(grp_new["new"])

        # Compare the bins to calculate PSI
        psi_df = grp_initial.join(grp_new, on="bin", how="inner")

        # Add a small value for when the percent is zero
        psi_df["percent_initial"] = psi_df["percent_initial"].apply(
            lambda x: eps if x == 0 else x
        )
        psi_df["percent_new"] = psi_df["percent_new"].apply(
            lambda x: eps if x == 0 else x
        )

        # Calculate the psi
        psi_df["psi"] = (psi_df["percent_initial"] - psi_df["percent_new"]) * np.log(
            psi_df["percent_initial"] / psi_df["percent_new"]
        )

        return psi_df.to_dict(orient="records")

    def run(self):
        model_library = Model.model_library(self.model.model)
        if model_library == "statsmodels" or model_library == "pytorch":
            print(f"Skiping PSI for {model_library} models")
            return

        psi_results = self._get_psi(
            self.model.y_train_predict.copy(), self.model.y_test_predict.copy()
        )

        trace1 = go.Bar(
            x=list(range(len(psi_results))),
            y=[d["percent_initial"] for d in psi_results],
            name="Initial",
            marker=dict(color="#DE257E"),
        )
        trace2 = go.Bar(
            x=list(range(len(psi_results))),
            y=[d["percent_new"] for d in psi_results],
            name="New",
            marker=dict(color="#E8B1F8"),
        )

        trace3 = go.Scatter(
            x=list(range(len(psi_results))),
            y=[d["psi"] for d in psi_results],
            name="PSI",
            yaxis="y2",
            line=dict(color="#257EDE"),
        )

        layout = go.Layout(
            title="Population Stability Index (PSI) Plot",
            xaxis=dict(title="Bin"),
            yaxis=dict(title="Population Ratio"),
            yaxis2=dict(
                title="PSI",
                overlaying="y",
                side="right",
                range=[
                    0,
                    max(d["psi"] for d in psi_results) + 0.005,
                ],  # Adjust as needed
            ),
            barmode="group",
        )

        fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
        figure = Figure(
            for_object=self,
            key=self.key,
            figure=fig,
        )

        return self.cache_results(metric_value=psi_results, figures=[figure])
