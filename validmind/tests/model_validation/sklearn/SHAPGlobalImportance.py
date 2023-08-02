# Copyright © 2023 ValidMind Inc. All rights reserved.

import warnings
from dataclasses import dataclass

import matplotlib.pyplot as plt
import shap

from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric, Model

logger = get_logger(__name__)


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
        if (
            model_library == "statsmodels"
            or model_library == "pytorch"
            or model_library == "catboost"
        ):
            logger.info(f"Skiping SHAP for {model_library} models")
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
