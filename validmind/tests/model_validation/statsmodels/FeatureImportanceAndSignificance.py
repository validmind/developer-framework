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
    Evaluates and visualizes the statistical significance and feature importance using regression and decision tree
    models.

    **Purpose**: The 'FeatureImportanceAndSignificance' test evaluates the statistical significance and the importance
    of features in the context of the machine learning model. By comparing the p-values from a regression model and the
    feature importances from a decision tree model, this test aids in determining the most significant variables from a
    statistical and a machine learning perspective, assisting in feature selection during the model development process.

    **Test Mechanism**: The test first compares the p-values from a regression model and the feature importances from a
    decision tree model. These values are normalized to ensure a uniform comparison. The 'p_threshold' parameter is
    used to determine what p-value is considered statistically significant and if the 'significant_only' parameter is
    true, only features with p-values below this threshold are included in the final output. The output from this test
    includes an interactive visualization displaying normalized p-values and the associated feature importances. The
    test throws an error if it does not receive both a regression model and a decision tree model.

    **Signs of High Risk**:
    - Exceptionally high or low p-values, which suggest that a feature may not be significant or meaningful in the
    context of the model.
    - If many variables with small feature importance values have significant p-values, this could indicate that the
    model might be overfitting.

    **Strengths**:
    - Combines two perspectives statistical significance (p-values) and feature importance (decision tree model),
    making it a robust feature selection test.
    - Provides an interactive visualization making it easy to interpret and understand the results.

    **Limitations**:
    - The test only works with a regression model and a decision tree model which may limit its applicability.
    - The test does not take into account potential correlations or causative relationships between features which may
    lead to misinterpretations of significance and importance.
    - Over-reliance on the p-value as a cut-off for feature significance can be seen as arbitrary and may not truly
    reflect the real-world importance of the feature.
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
