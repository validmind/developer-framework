# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go
from sklearn.inspection import permutation_importance

from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric

logger = get_logger(__name__)


@dataclass
class FeatureImportanceAndSignificance(Metric):
    """
    **Purpose**: The 'FeatureImportanceAndSignificance' test in the given script aims to calculate the importance and
    statistical significance of features within the model's context. It achieves this by comparing the p-values from a
    regression model and the feature importances from a decision tree model. This test aids in feature selection during
    the model development process by identifying the most significant variables.

    **Test Mechanism**: During this test, an initial comparison is made between the p-values from a regression model
    and the importance of features from a decision tree model. Both the p-values and feature importances are then
    normalized to ensure uniform comparison. The 'p_threshold' parameter is used to determine what p-value is
    considered statistically significant. If 'significant_only' parameter is true, features with p-values below the
    threshold will be included in the final output. The output includes interactive plots displaying Normalized
    p-values and the corresponding Normalized Feature Importance. Errors are thrown if two models aren't provided (one
    regression and one decision tree).

    **Signs of High Risk**: High risk or warning signs in the context of this test might include very high or very low
    p-values that stand out, suggesting a feature might not be meaningful. The risk may also exist if many unimportant
    variables (with low feature importance) have significant p-values, which might indicate that the model is possibly
    overfitted.

    **Strengths**: It is an excellent test for feature selection mechanisms as it combines two perspectives:
    statistical significance through p-values and feature importance using a machine learning model (decision tree).
    Additionally, it includes an interactive visualization, facilitating comprehension of the results easily.

    **Limitations**: This test only accepts two models - a regression model and a decision tree. Therefore, its
    application may be limited if other model types are used. Furthermore, the test might not account for potential
    correlative or causative relationships between the input features, which potentially can lead to inaccurate
    importance and significance readings. Lastly, it heavily relies on the p-value as a cut-off for feature
    significance, which critics argue can be arbitrary and might not reflect the true significance of the feature.
    """

    name = "feature_importance_and_significance"
    default_params = {
        "fontsize": 10,
        "p_threshold": 0.05,
        "significant_only": False,
        "figure_height": 800,
        "bar_width": 0.3,
    }
    metadata = {
        "task_types": ["regression"],
        "tags": [
            "statsmodels",
            "feature_importance",
            "statistical_test",
            "visualization",
        ],
    }

    def compute_p_values_and_feature_importances(
        self, regression_model, decision_tree_model
    ):
        p_values = regression_model.model.pvalues
        feature_importances = permutation_importance(
            decision_tree_model.model,
            decision_tree_model.train_ds.x,
            decision_tree_model.train_ds.y,
            random_state=0,
            n_jobs=-2,
        ).importances_mean

        p_values = p_values / max(p_values)
        feature_importances = feature_importances / max(feature_importances)

        return p_values, feature_importances

    def create_dataframe(
        self,
        p_values,
        feature_importances,
        regression_model,
        significant_only,
        p_threshold,
    ):
        df = pd.DataFrame(
            {
                "Normalized p-value": p_values,
                "Normalized Feature Importance": feature_importances,
            },
            index=regression_model.train_ds.x.columns,
        )

        if significant_only:
            df = df[df["Normalized p-value"] <= p_threshold]

        df = df.sort_values(by="Normalized Feature Importance", ascending=True)

        return df

    def create_figure(self, df, fontsize, figure_height, bar_width):
        fig = go.Figure()

        title_text = (
            "Significant Features (p-value <= {0})".format(self.params["p_threshold"])
            if self.params["significant_only"]
            else "All Features"
        )

        fig.update_layout(
            title=title_text,
            barmode="group",
            height=figure_height,
            yaxis=dict(tickfont=dict(size=fontsize)),
            xaxis=dict(title="Normalized Value", titlefont=dict(size=fontsize)),
        )

        fig.add_trace(
            go.Bar(
                y=df.index,
                x=df["Normalized p-value"],
                name="Normalized p-value",
                orientation="h",
                marker=dict(color="skyblue"),
                width=bar_width,
            )
        )

        fig.add_trace(
            go.Bar(
                y=df.index,
                x=df["Normalized Feature Importance"],
                name="Normalized Feature Importance",
                orientation="h",
                marker=dict(color="orange"),
                width=bar_width,
            )
        )

        return fig

    def run(self):
        fontsize = self.params["fontsize"]
        significant_only = self.params["significant_only"]
        p_threshold = self.params["p_threshold"]
        figure_height = self.params["figure_height"]
        bar_width = self.params["bar_width"]

        all_models = []

        if self.models is not None:
            all_models.extend(self.models)

        if len(self.models) != 2:
            raise ValueError("Two models must be provided")

        regression_model = self.models[0]
        decision_tree_model = self.models[1]

        p_values, feature_importances = self.compute_p_values_and_feature_importances(
            regression_model, decision_tree_model
        )

        df = self.create_dataframe(
            p_values,
            feature_importances,
            regression_model,
            significant_only,
            p_threshold,
        )

        fig = self.create_figure(df, fontsize, figure_height, bar_width)

        return self.cache_results(
            figures=[
                Figure(
                    for_object=self,
                    key=self.key,
                    figure=fig,
                    metadata={
                        "model_regression": str(regression_model.model),
                        "model_decision_tree": str(decision_tree_model.model),
                    },
                )
            ]
        )
