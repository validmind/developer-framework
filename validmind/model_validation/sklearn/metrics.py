"""
Metrics functions models trained with sklearn or that provide
a sklearn-like API
"""
import warnings
from dataclasses import dataclass
from functools import partial

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn import metrics
from sklearn.inspection import permutation_importance

from ...vm_models import Figure, Metric, Model, ResultSummary, ResultTable
from ...utils import format_number


def _get_psi(score_initial, score_new, num_bins=10, mode="fixed", as_dict=False):
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
            min_val + (max_val - min_val) * (i) / num_bins for i in range(num_bins + 1)
        ]
    elif mode == "quantile":
        bins = pd.qcut(score_initial, q=num_bins, retbins=True)[
            1
        ]  # Create the quantiles based on the initial population
    else:
        raise ValueError(
            f"Mode '{mode}' not recognized. Your options are 'fixed' and 'quantile'"
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
    psi_df["percent_new"] = psi_df["percent_new"].apply(lambda x: eps if x == 0 else x)

    # Calculate the psi
    psi_df["psi"] = (psi_df["percent_initial"] - psi_df["percent_new"]) * np.log(
        psi_df["percent_initial"] / psi_df["percent_new"]
    )

    if as_dict:
        return psi_df.to_dict(orient="records")

    # Return the psi values dataframe
    return psi_df


@dataclass
class CharacteristicStabilityIndex(Metric):
    """
    Characteristic Stability Index between two datasets
    """

    name = "csi"
    required_context = ["model"]
    value_formatter = "key_values"

    def run(self):
        """
        Calculates PSI for each of the dataset features
        """
        model_library = Model.model_library(self.model.model)
        if model_library == "statsmodels" or model_library == "pytorch":
            print(f"Skiping CSI for {model_library} models")
            return

        x_train = self.model.train_ds.x
        x_test = self.model.test_ds.x

        csi_values = {}
        for col in x_train.columns:
            psi_df = _get_psi(x_train[col].values, x_test[col].values)
            csi_value = np.mean(psi_df["psi"])
            csi_values[col] = csi_value

        return self.cache_results(metric_value=csi_values)


@dataclass
class ConfusionMatrix(Metric):
    """
    Confusion Matrix
    """

    name = "confusion_matrix"
    required_context = ["model"]

    def summary(self, metric_value):
        return None

    def run(self):
        y_true = self.model.test_ds.y
        y_labels = list(map(lambda x: x.item(), y_true.unique()))
        y_labels.sort()

        class_pred = self.model.class_predictions(self.model.y_test_predict)

        cm = metrics.confusion_matrix(y_true, class_pred, labels=y_labels)
        tn, fp, fn, tp = cm.ravel()

        plot = metrics.ConfusionMatrixDisplay(
            confusion_matrix=cm, display_labels=y_labels
        ).plot()

        return self.cache_results(
            metric_value={
                "tn": tn,
                "fp": fp,
                "fn": fn,
                "tp": tp,
            },
            figures=[
                Figure(
                    key="confusion_matrix",
                    figure=plot.figure_,
                    metadata={},
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
                    key="pfi",
                    figure=fig,
                    metadata={},
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

    def run(self):
        y_true = self.model.test_ds.df[self.model.test_ds.target_column]
        precision, recall, pr_thresholds = metrics.precision_recall_curve(
            y_true, self.model.y_test_predict
        )
        plot = metrics.PrecisionRecallDisplay(
            precision=precision,
            recall=recall,
            average_precision=None,
        ).plot()

        return self.cache_results(
            metric_value={
                "precision": precision,
                "recall": recall,
                "thresholds": pr_thresholds,
            },
            figures=[Figure(key="pr_curve", figure=plot.figure_, metadata={})],
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

        metrics = self.params["metrics"]
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

    def run(self):
        y_true = self.model.test_ds.df[self.model.test_ds.target_column]
        class_pred = self.model.class_predictions(self.model.y_test_predict)
        fpr, tpr, roc_thresholds = metrics.roc_curve(
            y_true, self.model.y_test_predict, drop_intermediate=True
        )
        auc = metrics.roc_auc_score(y_true, class_pred)

        plot = metrics.RocCurveDisplay(
            fpr=fpr,
            tpr=tpr,
            roc_auc=auc,
        ).plot()

        return self.cache_results(
            metric_value={
                "auc": auc,
                "fpr": fpr,
                "tpr": tpr,
                "thresholds": roc_thresholds,
            },
            figures=[Figure(key="roc_auc_curve", figure=plot.figure_, metadata={})],
        )


@dataclass
class SHAPGlobalImportance(Metric):
    """
    SHAP Global Importance
    """

    required_context = ["model"]
    name = "shap"

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

        return Figure(figure=figure, key=f"shap:{type_}", metadata={"type": type_})

    def run(self):
        model_library = Model.model_library(self.model.model)
        if model_library == "statsmodels" or model_library == "pytorch":
            print(f"Skiping SHAP for {model_library} models")
            return

        trained_model = self.model.model
        model_class = Model.model_class(trained_model)

        # the shap library generates a bunch of annoying warnings that we don't care about
        warnings.filterwarnings("ignore", category=UserWarning)

        # RandomForestClassifier applies here too
        if model_class == "XGBClassifier" or model_class == "RandomForestClassifier":
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
    value_formatter = "records"

    def run(self):
        model_library = Model.model_library(self.model.model)
        if model_library == "statsmodels" or model_library == "pytorch":
            print(f"Skiping PSI for {model_library} models")
            return

        psi_df = _get_psi(self.model.y_train_predict, self.model.y_test_predict)

        return self.cache_results(metric_value=psi_df)
