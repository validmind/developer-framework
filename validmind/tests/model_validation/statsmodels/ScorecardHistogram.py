# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import pandas as pd
from dataclasses import dataclass
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from validmind.vm_models import Figure, Metric, Model


@dataclass
class ScorecardHistogram(Metric):
    """
    Score Histogram
    """

    name = "scorecard_histogram"
    required_context = ["model"]
    default_parameters = {
        "title": "Histogram of Scores",
        "target_score": 600,
        "target_odds": 50,
        "pdo": 20,
    }

    def description(self):
        return """
        This metric calculates the credit score for each instance in the training and test datasets,
        and creates histograms to visualize the distributions of scores for the positive and negative classes.
        """

    @staticmethod
    def compute_scores(model, X, target_score, target_odds, pdo):
        X_copy = X.copy()
        beta = model.model.params.values
        alpha = model.model.params[0]
        factor = pdo / np.log(2)
        offset = target_score - (factor * np.log(target_odds))

        for _, row in X_copy.iterrows():
            score_i = 0
            for i in range(1, len(beta)):
                WoE_i = row[i]
                score_i += (beta[i] * WoE_i) * factor

            score_i += alpha * factor
            score_i += offset
            X_copy.loc[row.name, "score"] = score_i

        return X_copy

    @staticmethod
    def plot_score_histogram(df_train, df_test, score_col, target_col, title):
        scores_train_0 = df_train[df_train[target_col] == 0][score_col]
        scores_train_1 = df_train[df_train[target_col] == 1][score_col]
        scores_test_0 = df_test[df_test[target_col] == 0][score_col]
        scores_test_1 = df_test[df_test[target_col] == 1][score_col]

        fig = make_subplots(rows=1, cols=2, subplot_titles=("Train Data", "Test Data"))

        trace_train_0 = go.Histogram(
            x=scores_train_0, opacity=0.75, name=f"Train {target_col} = 0"
        )
        trace_train_1 = go.Histogram(
            x=scores_train_1, opacity=0.75, name=f"Train {target_col} = 1"
        )
        trace_test_0 = go.Histogram(
            x=scores_test_0, opacity=0.75, name=f"Test {target_col} = 0"
        )
        trace_test_1 = go.Histogram(
            x=scores_test_1, opacity=0.75, name=f"Test {target_col} = 1"
        )

        fig.add_trace(trace_train_0, row=1, col=1)
        fig.add_trace(trace_train_1, row=1, col=1)
        fig.add_trace(trace_test_0, row=1, col=2)
        fig.add_trace(trace_test_1, row=1, col=2)

        fig.update_layout(barmode="overlay", title_text=title)

        return fig

    def run(self):
        if not Model.is_supported_model(self.model.model):
            raise ValueError(
                f"{Model.model_library(self.model.model)}.{Model.model_class(self.model.model)} \
                is not supported by ValidMind framework yet"
            )

        target_column = self.model.train_ds.target_column
        title = self.params["title"]
        target_score = self.params["target_score"]
        target_odds = self.params["target_odds"]
        pdo = self.params["pdo"]

        X_train = self.model.train_ds.x.copy()
        y_train = self.model.train_ds.y.copy()
        X_test = self.model.test_ds.x.copy()
        y_test = self.model.test_ds.y.copy()

        X_train_scores = self.compute_scores(
            self.model, X_train, target_score, target_odds, pdo
        )
        X_test_scores = self.compute_scores(
            self.model, X_test, target_score, target_odds, pdo
        )

        df_train = pd.concat([X_train_scores, y_train], axis=1)
        df_test = pd.concat([X_test_scores, y_test], axis=1)

        fig = self.plot_score_histogram(
            df_train, df_test, "score", target_column, title
        )

        return self.cache_results(
            metric_value={
                "score_histogram": {
                    "train_scores": list(X_train_scores["score"]),
                    "test_scores": list(X_test_scores["score"]),
                },
            },
            figures=[
                Figure(
                    for_object=self,
                    key="score_histogram",
                    figure=fig,
                )
            ],
        )
