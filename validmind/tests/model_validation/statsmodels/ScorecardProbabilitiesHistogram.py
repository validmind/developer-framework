# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class ScorecardProbabilitiesHistogram(Metric):
    """
    Evaluates risk classification of a model by visualizing the distribution of default probability across score
    buckets.

    **Purpose**: The Scorecard Probabilities Histogram, a specific metric used within the credit risk domain, is
    designed to evaluate and visualize risk classification of a model. It aims at examining the distribution of the
    probability of default across varied score buckets, with the score buckets being categories that entities (e.g.,
    loan applicants) are classed under based on their predicted default risks. The key idea is to ensure that the model
    accurately classifies entities into appropriate risk categories (score buckets) and aptly represents their default
    probabilities.

    **Test Mechanism**: The mechanism behind the Scorecard Probabilities Histogram includes several steps. It starts
    with the calculation of default probabilities by the 'compute_probabilities' method, where the resulting
    probability is added as a fresh column to the input dataset. Following that, scores are computed using these
    probabilities, a target score, target odds, and a Points to Double the odds (pdo) factor by the 'compute_scores'
    method. These scores are then bucketed via the 'compute_buckets' method. A histogram is then plotted for each score
    bucket, with default probabilities as the x-axis and their frequency as the y-axis - implemented within the
    'plot_probabilities_histogram' method. This entire process is executed distinctly for both training and testing
    datasets.

    **Signs of High Risk**:
    - A significant overlap of different score buckets in the histogram indicates that the model is not efficiently
    distinguishing between various risk categories.
    - If very high or low probabilities are commonplace across all buckets, the model's predictions could be skewed.

    **Strengths**:
    - The Scorecard Probabilities Histogram allows for the visualization and analysis of the predicted default risk
    distribution across different risk classes, thereby facilitating a visual inspection of the model's performance and
    calibration for various risk categories.
    - It provides a means to visualize how these classifications are distributed on the training and testing datasets
    separately, contributing to a better comprehension of model generalization.

    **Limitations**:
    - The Scorecard Probabilities Histogram assumes linear and equally spaced risk categories, which might not always
    hold true.
    - If there are too few or too many score buckets, the visualization may not convey sufficient information.
    - While it effectively illustrates the distribution of probabilities, it does not provide adequate numerical
    metrics or threshold to definitively evaluate the model's performance. A more accurate evaluation necessitates its
    usage in conjunction with other metrics and tools including the confusion matrix, AUC-ROC, Precision, Recall, and
    so forth.
    """

    name = "scorecard_probabilities_histogram"
    required_inputs = ["model"]
    metadata = {
        "task_types": ["classification"],
        "tags": ["tabular_data", "visualization", "credit_risk"],
    }
    default_params = {
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
