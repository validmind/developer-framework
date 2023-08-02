# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import pandas as pd
from dataclasses import dataclass
import plotly.graph_objects as go
from validmind.vm_models import Figure, Metric, Model


@dataclass
class ScorecardBucketHistogram(Metric):
    """
    Scorecard Bucket Probability of Default
    """

    name = "scorecard_bucket_histogram"
    required_context = ["model"]
    default_parameters = {
        "title": "Distribution of Scores by Rating Classes",
        "target_score": 600,
        "target_odds": 50,
        "pdo": 20,
        "rating_classes": ["A", "B", "C", "D"],
    }

    @staticmethod
    def compute_probabilities(model, X):
        """
        Predict probabilities and add them as a new column in X
        """
        probabilities = model.predict(X)
        X["probabilities"] = probabilities
        return X

    @staticmethod
    def compute_scores(X, target_score, target_odds, pdo):
        X_copy = X.copy()
        factor = pdo / np.log(2)
        offset = target_score - (factor * np.log(target_odds))

        X_copy["score"] = offset + factor * np.log(
            X_copy["probabilities"] / (1 - X_copy["probabilities"])
        )

        return X_copy

    @staticmethod
    def plot_score_bucket_histogram(df, score_col, title, rating_classes):
        df["bucket"] = pd.cut(
            df[score_col], bins=len(rating_classes), labels=rating_classes, right=False
        )

        fig = go.Figure()

        color_scale = [[0.0, "rgba(178, 24, 43, 1)"], [1.0, "rgba(33, 102, 172, 1)"]]

        for bucket in rating_classes:
            df_bucket = df[df["bucket"] == bucket]
            bucket_values = df_bucket[score_col]
            fig.add_trace(
                go.Histogram(
                    x=bucket_values,
                    name=bucket,
                    opacity=0.6,
                )
            )

        fig.update_layout(
            title_text=title,
            xaxis_title="",
            yaxis_title="Frequency",
            barmode="overlay",
            coloraxis=dict(colorscale=color_scale, colorbar=dict(title="")),
        )

        return fig

    def run(self):
        if not Model.is_supported_model(self.model.model):
            raise ValueError(
                f"{Model.model_library(self.model.model)}.{Model.model_class(self.model.model)} \
                is not supported by ValidMind framework yet"
            )

        title = self.params["title"]
        target_score = self.params["target_score"]
        target_odds = self.params["target_odds"]
        pdo = self.params["pdo"]
        rating_classes = self.params["rating_classes"]

        X_train = self.model.train_ds.x.copy()
        X_test = self.model.test_ds.x.copy()

        X_train_probs = self.compute_probabilities(self.model, X_train)
        X_test_probs = self.compute_probabilities(self.model, X_test)

        df_train_scores = self.compute_scores(
            X_train_probs, target_score, target_odds, pdo
        )
        df_test_scores = self.compute_scores(
            X_test_probs, target_score, target_odds, pdo
        )

        fig_train = self.plot_score_bucket_histogram(
            df_train_scores,
            "score",
            title + " - Train Data",
            rating_classes,
        )
        fig_test = self.plot_score_bucket_histogram(
            df_test_scores,
            "score",
            title + " - Test Data",
            rating_classes,
        )

        return self.cache_results(
            metric_value={
                "score_distribution": {
                    "train_scores": list(df_train_scores["score"]),
                    "test_scores": list(df_test_scores["score"]),
                },
            },
            figures=[
                Figure(
                    for_object=self,
                    key="score_distribution_train",
                    figure=fig_train,
                ),
                Figure(
                    for_object=self,
                    key="score_distribution_test",
                    figure=fig_test,
                ),
            ],
        )
