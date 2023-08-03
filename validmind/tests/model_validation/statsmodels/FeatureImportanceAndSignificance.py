# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from sklearn.inspection import permutation_importance
import pandas as pd
import plotly.graph_objects as go
from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric, Model

logger = get_logger(__name__)


@dataclass
class FeatureImportanceAndSignificance(Metric):
    """
    This metric class computes and visualizes the feature importance and statistical significance
    within a model's context. It compares the p-values from a regression model with the feature importances
    from a decision tree model. The significance filter can be turned on or off, allowing for flexibility
    in feature selection. The p-values and feature importances are normalized for comparison and visualization.
    """

    name = "feature_importance_and_significance"
    default_params = {
        "fontsize": 10,
        "p_threshold": 0.05,
        "significant_only": False,
        "figure_height": 800,
        "bar_width": 0.3,
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

        for m in all_models:
            if not Model.is_supported_model(m.model):
                raise ValueError(
                    f"{Model.model_library(m.model)}.{Model.model_class(m.model)}"
                    " is not supported by the ValidMind framework yet"
                )

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
