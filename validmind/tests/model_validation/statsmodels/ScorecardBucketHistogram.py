# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

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
    required_inputs = ["datasets"]
    metadata = {
        "task_types": ["classification"],
        "tags": ["tabular_data", "visualization", "credit_risk"],
    }
    default_params = {
        "title": "Histogram of Scores",
        "score_column": "score",
        "bucket_column": "bucket",
    }

    @staticmethod
    def plot_score_bucket_histogram(df, score_col, bucket_col, title):
        fig = go.Figure()

        rating_classes = df[bucket_col].unique()

        for bucket in rating_classes:
            df_bucket = df[df[bucket_col] == bucket]
            bucket_values = df_bucket[score_col]
            fig.add_trace(
                go.Histogram(
                    x=bucket_values,
                    name=str(bucket),  # Ensure bucket names are string for the plot
                    opacity=0.6,
                )
            )

        fig.update_layout(
            title_text=title,
            xaxis_title="Score",
            yaxis_title="Frequency",
            barmode="overlay",
        )

        return fig

    def run(self):
        title = self.params["title"]
        score_column = self.params["score_column"]
        bucket_column = self.params["bucket_column"]

        # Directly retrieve the score and bucket column data
        df_train = self.inputs.datasets[0].df.copy()
        df_test = self.inputs.datasets[1].df.copy()

        # The plot function now dynamically determines rating classes from the unique bucket values
        fig_train = self.plot_score_bucket_histogram(
            df_train,
            score_column,
            bucket_column,
            title + " - Train Data",
        )
        fig_test = self.plot_score_bucket_histogram(
            df_test,
            score_column,
            bucket_column,
            title + " - Test Data",
        )

        # Return the results
        return self.cache_results(
            metric_value={
                "score_distribution": {
                    "train_scores": list(df_train[score_column]),
                    "test_scores": list(df_test[score_column]),
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
