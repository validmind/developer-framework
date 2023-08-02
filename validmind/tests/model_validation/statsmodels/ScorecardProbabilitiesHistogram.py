# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import pandas as pd
from dataclasses import dataclass
import plotly.graph_objects as go
from validmind.vm_models import Figure, Metric, Model


@dataclass
class ScorecardProbabilitiesHistogram(Metric):
    """
    Scorecard Bucket Probability of Default Histogram
    """

    name = "scorecard_probabilities_histogram"
    required_context = ["model"]
    default_parameters = {
        "title": "Probability of Default by Score Bucket",
        "target_score": 600,
        "target_odds": 50,
        "pdo": 20,
        "score_buckets": ["A", "B", "C", "D"],
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
    def compute_buckets(X, score_buckets):
        X["bucket"] = pd.qcut(X["score"], q=len(score_buckets), labels=score_buckets)
        return X

    @staticmethod
    def plot_probabilities_histogram(df, title, score_buckets):
        fig = go.Figure()

        for bucket in score_buckets:
            df_bucket = df[df["bucket"] == bucket]
            bucket_values = df_bucket["probabilities"]
            fig.add_trace(
                go.Histogram(
                    x=bucket_values,
                    name=bucket,
                    opacity=0.6,
                )
            )

        fig.update_layout(
            title_text=title,
            xaxis_title="Probability",
            yaxis_title="Frequency",
            barmode="overlay",
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
        score_buckets = self.params["score_buckets"]

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

        df_train_buckets = self.compute_buckets(df_train_scores, score_buckets)
        df_test_buckets = self.compute_buckets(df_test_scores, score_buckets)

        fig_train = self.plot_probabilities_histogram(
            df_train_buckets,
            title + " - Train Data",
            score_buckets,
        )
        fig_test = self.plot_probabilities_histogram(
            df_test_buckets,
            title + " - Test Data",
            score_buckets,
        )

        return self.cache_results(
            metric_value={
                "probability_distribution": {
                    "train_probs": list(df_train_buckets["probabilities"]),
                    "test_probs": list(df_test_buckets["probabilities"]),
                },
            },
            figures=[
                Figure(
                    for_object=self,
                    key="probability_distribution_train",
                    figure=fig_train,
                ),
                Figure(
                    for_object=self,
                    key="probability_distribution_test",
                    figure=fig_test,
                ),
            ],
        )
