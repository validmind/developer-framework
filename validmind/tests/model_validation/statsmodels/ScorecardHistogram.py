# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from validmind.vm_models import Figure, Metric


@dataclass
class ScorecardHistogram(Metric):
    """
    **Purpose**: The **Scorecard Histogram** test provides a visual representation of the distribution of credit scores
    produced by an ML model for classification tasks involving credit risk. The metric is primarily designed to analyze
    how the model's scoring decision aligns with actual outcomes of credit loan applications. In addition, it helps
    identify potential discrepancies between model predictions and real-world risk levels.

    **Test Mechanism**: This model-specific metric uses the provided training and test datasets to generate a histogram
    of credit scores for both default (negative class) and non-default (positive class) instances. It works by
    calculating the credit score for each instance in the dataset using a logistic regression model's scorecard method
    which takes into account the contributions of different features to the odds of being a default. It uses a default
    point to odds (PDO) scaling factor and predefined target score and odds settings. The score distribution is
    calculated and plotted separately for the training and test sets to facilitate insights into how well the model
    generalizes to unseen data.

    **Signs of High Risk**: Indications of potential risk or performance issues in relation to this metric include
    significant discrepancies between the distributions of training and testing data, skewed distributions favoring a
    particular score or class, or an abnormal distribution of scores that does not align with expected real-world
    patterns. If positive and negative classes tend to have similar scores or their distributions overlap
    significantly, it might suggest the model is not effective at differentiating between the classes.

    **Strengths**: The Scorecard Histogram metric is useful for visually interpreting the credit scoring system of a
    machine learning model and can provide a greater understanding of model behavior. It allows for direct comparison
    of actual and predicted scores for both training and testing data, and provides a way to intuitively visualize
    model's ability to differentiate between positive and negative classes. It also aids in uncovering patterns or
    anomalies that might not be evident from numerical metrics alone.

    **Limitations**: Although valuable for visual interpretation, this method doesn't quantify model's performance, and
    hence might lack precision when it comes to complete model evaluation. It is also susceptible to the quality of the
    input data—undue bias or noise in the data will impact both the score calculation and resultant histogram.
    Additionally, the test is specific to credit scoring models, which limits its usefulness across a broader range of
    machine learning tasks and models. Finally, the efficacy of the metric is somewhat tied to subjective
    interpretation, as it relies on the analyst's assessment of the plot's characteristics and implications.
    """

    name = "scorecard_histogram"
    required_inputs = ["model"]
    metadata = {
        "task_types": ["classification"],
        "tags": ["tabular_data", "visualization", "credit_risk"],
    }
    default_params = {
        "title": "Histogram of Scores",
        "target_score": 600,
        "target_odds": 50,
        "pdo": 20,
    }

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
        model = self.model[0] if isinstance(self.model, list) else self.model

        target_column = model.train_ds.target_column
        title = self.params["title"]
        target_score = self.params["target_score"]
        target_odds = self.params["target_odds"]
        pdo = self.params["pdo"]

        # Create a copy of training and testing dataframes
        df_train = model.train_ds._df.copy()
        df_test = model.test_ds._df.copy()

        # Drop target_column to create feature dataframes
        X_train = df_train.drop(columns=[target_column])
        X_test = df_test.drop(columns=[target_column])

        # Subset only target_column to create target dataframes
        y_train = df_train[[target_column]]
        y_test = df_test[[target_column]]

        X_train_scores = self.compute_scores(
            model, X_train, target_score, target_odds, pdo
        )
        X_test_scores = self.compute_scores(
            model, X_test, target_score, target_odds, pdo
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
