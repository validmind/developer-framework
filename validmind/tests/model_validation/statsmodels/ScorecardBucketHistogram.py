# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class ScorecardBucketHistogram(Metric):
    """
    Evaluates and visualizes distribution of risk categories in a classification model's scores, useful in credit risk
    assessment.

    **Purpose**: The 'Scorecard Bucket Histogram' is employed as a metric to evaluate the performance of a
    classification model, specifically in credit risk assessment. It categorizes model scores into different rating
    classes, and visualizes the distribution of scores or probabilities within each class. It essentially measures how
    different risk categories (classes) are distributed in the model scores and provides insight into the model's
    classification ability. This makes it particularly useful in credit scoring and risk modeling where understanding
    the probability of default is critical.

    **Test Mechanism**: The test works by computing the probabilities for each record in the test and train dataset
    using the model's predict function. Subsequently, it calculates the scores using a formula incorporating target
    score, target odds, and points to double odds (PDO). The scores are then bucketed into predefined rating classes
    (such as 'A', 'B', 'C', 'D') and plotted in a histogram for both the train and test datasets. The target score,
    target odds, points to double the odds (PDO), and rating classes are customizable parameters, providing flexibility
    in test metrics based on differing model or industry norms.

    **Signs of High Risk**:

    - Disproportionate scores within rating classes
    - Excessive overlap between classes
    - Inconsistent distribution of scores between the training and testing datasets

    If the model is accurately classifying and risk is being evenly distributed, we would anticipate smooth and
    relatively balanced histograms within classes.

    **Strengths**:

    - Provides a quick visual snapshot of score distribution
    - Breaks down complex predictions into simple, understandable classes, making it easily interpretable for both
    technical and non-technical audiences
    - Caters to customization of parameters
    - Gives ownership of the class definitions to the user
    - Useful in the field of credit risk, providing a clear understanding of which class or 'bucket' a potential
    borrower belongs to

    **Limitations**:

    - Relies on manual setting of classes and other parameters (like target score, target odds, and PDO), potentially
    leading to arbitrary classifications and potential bias if not judiciously performed
    - Effectiveness can be limited with non-tabular data
    - Doesn't provide a numerical value easily compared across different models or runs as the output is primarily
    visual
    - Might not present a complete view of model performance and should be used in conjunction with other metrics
    """

    name = "scorecard_bucket_histogram"
    required_inputs = ["model"]
    metadata = {
        "task_types": ["classification"],
        "tags": ["tabular_data", "visualization", "credit_risk"],
    }
    default_params = {
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
