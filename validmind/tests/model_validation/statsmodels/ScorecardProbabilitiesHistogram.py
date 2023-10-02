# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class ScorecardProbabilitiesHistogram(Metric):
    """
    **Purpose**: This metric, referred to as the Scorecard Probabilities Histogram, is used to visualise and evaluate
    the risk classification of a model especially designed for the credit risk domain. It does this by examining the
    distribution of the probability of default across different score buckets. The score buckets are categories in
    which entities (like loan applicants) are placed based on their predicted default risk. Specifically, this metric
    is used to ensure the model correctly classifies entities into the appropriate risk categories (score buckets) and
    also properly represents their default probabilities.

    **Test Mechanism**: The Scorecard Probabilities Histogram first calculates default probabilities using the
    'compute_probabilities' method where the output probability is added as a new column to the input dataset. Next,
    scores are computed using these probabilities, a target score, target odds and Points to Double the odds (pdo)
    factor in the 'compute_scores' method. These scores are further processed into buckets using the 'compute_buckets'
    method. Once data is bucketed, a histogram is plotted for each score bucket. This histogram takes the probabilities
    of default serious as the x-axis and their frequency as the y-axis using the 'plot_probabilities_histogram' method.
    The process is run separately for both training and testing data.

    **Signs of High Risk**: If there is a significant overlap of different score buckets in the histogram, this can
    indicate that the model is not effectively distinguishing between different risk categories. Additionally, if
    extremely high or low probabilities are common across all buckets, there may be a skew in the model's predictions.

    **Strengths**: The Scorecard Probabilities Histogram is an advantageous tool for observing and analysing the
    predicted default risk distribution across different risk categories. This metric allows us to visually inspect the
    model's performance and its calibration for different risk categories. Moreover, it also provides a mechanism to
    visualize how these classifications are distributed on the training and testing datasets separately which is
    beneficial for understanding model generalization.

    **Limitations**: The Scorecard Probabilities Histogram does have limitations. For one, it assumes that the risk
    categories are linear and equally spaced, which may not always be the case. Secondly, the visualization may not
    provide adequate information if there are too few or too many score buckets. Lastly, while this metric effectively
    visualizes the distribution of probabilities, it provides no concrete numerical metric or threshold to definitively
    gauge the model's performance. For a more precise evaluation, it should be used in combination with other metrics
    and tools such as confusion matrix, AUC-ROC, Precision, Recall etc.
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
