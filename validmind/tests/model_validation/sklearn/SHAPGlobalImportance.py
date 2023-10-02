# Copyright © 2023 ValidMind Inc. All rights reserved.

import warnings
from dataclasses import dataclass

import matplotlib.pyplot as plt
import shap

from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric

logger = get_logger(__name__)


@dataclass
class SHAPGlobalImportance(Metric):
    """
    **Purpose:**
    The SHAP (SHapley Additive exPlanations) Global Importance metric illuminates the outcomes of machine learning
    models by attributing them to the contributing features. It assigns a quantifiable global importance to features
    via their absolute Shapley values, making it applicable for tasks such as classification (both binary and
    multiclass). This metric is pivotal in the model risk management strategy.

    **Test Mechanism:**
    The first step involves choosing an appropriate explainer that matches the model type: TreeExplainer for tree-based
    models (like XGBClassifier, RandomForestClassifier, CatBoostClassifier) and LinearExplainer for linear ones (such
    as LogisticRegression, XGBRegressor, LinearRegression). Once the explainer calculates the Shapley values, they are
    visualized through two specific plots:

    1. **Mean Importance Plot**: This graph denotes the significance of each feature grounded in its absolute Shapley
    values. By computing the average of these absolute Shapley values across the entire dataset, the global importance
    of features is elucidated.

    2. **Summary Plot**: This visual representation amalgamates the importance of each feature with their effects. Each
    dot on this plot symbolizes a Shapley value for a distinct feature in a specific instance. The vertical axis
    represents the feature, while the horizontal axis corresponds to the Shapley value. A color gradient, shifting from
    low to high, marks the feature's value. Overlapping points experience a slight vertical dispersion, offering a
    snapshot of the Shapley values' distribution for each attribute. Features are methodically aligned in accordance
    with their prominence. The function `_generate_shap_plot()` renders these plots with the aforementioned types.

    **Signs of High Risk:**
    Overly dominant features in SHAP importance plots hint at potential model overfitting. Anomalies, like unexpected
    or speculative features flaunting high importance, could suggest that the model's decisions are rooted in incorrect
    or undesirable reasoning. Moreover, a SHAP summary plot teeming with high variability or scattered data points is a
    cause for concern.

    **Strengths:**
    Beyond delineating global feature significance, SHAP offers a granular perspective on how individual attributes
    shape the model's decision logic for each instance. This advanced method unravels model behavior with clarity. Its
    flexibility is evident in its support for a diverse array of model types, ensuring uniform interpretations across
    different models.

    **Limitations:**
    For large datasets or intricate models, SHAP's computations might demand substantial time and resources. Moreover,
    its compatibility does not extend to every model class, especially models from libraries like "statsmodels",
    "pytorch", "catboost", "transformers", "FoundationModel", and "R". High-dimensional data can muddle
    interpretations, and linking importance to tangible real-world impact retains a degree of subjectivity.
    """

    name = "shap"
    required_inputs = ["model"]
    metadata = {
        "task_types": ["classification", "text_classification"],
        "tags": [
            "sklearn",
            "binary_classification",
            "multiclass_classification",
            "feature_importance",
            "visualization",
        ],
    }

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
        model_library = self.model.model_library()
        if model_library in [
            "statsmodels",
            "pytorch",
            "catboost",
            "transformers",
            "FoundationModel",
            "R",
        ]:
            logger.info(f"Skiping SHAP for {model_library} models")
            return

        trained_model = self.model.model
        model_class = self.model.model_class()

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
