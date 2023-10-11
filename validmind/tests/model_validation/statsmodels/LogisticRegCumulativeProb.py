# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from validmind.vm_models import Figure, Metric


@dataclass
class LogisticRegCumulativeProb(Metric):
    """
    Visualizes cumulative probabilities of positive and negative classes for both training and testing in logistic
    regression models.

    **Purpose**: This metric is utilized to evaluate the distribution of predicted probabilities for positive and
    negative classes in a logistic regression model. It's not solely intended to measure the model's performance but
    also provides a visual assessment of the model's behavior by plotting the cumulative probabilities for positive and
    negative classes across both the training and test datasets.

    **Test Mechanism**: The logistic regression model is evaluated by first computing the predicted probabilities for
    each instance in both the training and test datasets, which are then added as a new column in these sets. The
    cumulative probabilities for positive and negative classes are subsequently calculated and sorted in ascending
    order. Cumulative distributions of these probabilities are created for both positive and negative classes across
    both training and test datasets. These cumulative probabilities are represented visually in a plot, containing two
    subplots - one for the training data and the other for the test data, with lines representing cumulative
    distributions of positive and negative classes.

    **Signs of High Risk**:
    - Imbalanced distribution of probabilities for either positive or negative classes.
    - Notable discrepancies or significant differences between the cumulative probability distributions for the
    training data versus the test data.
    - Marked discrepancies or large differences between the cumulative probability distributions for positive and
    negative classes.

    **Strengths**:
    - It offers not only numerical probabilities but also provides a visual illustration of data, which enhances the
    ease of understanding and interpreting the model's behavior.
    - Allows for the comparison of model's behavior across training and testing datasets, providing insights about how
    well the model is generalized.
    - It differentiates between positive and negative classes and their respective distribution patterns, which can aid
    in problem diagnosis.

    **Limitations**:
    - Exclusive to classification tasks and specifically to logistic regression models.
    - Graphical results necessitate human interpretation and may not be directly applicable for automated risk
    detection.
    - The method does not give a solitary quantifiable measure of model risk, rather it offers a visual representation
    and broad distributional information.
    - If the training and test datasets are not representative of the overall data distribution, the metric could
    provide misleading results.
    """

    name = "logistic_reg_cumulative_prob"
    required_inputs = ["model"]
    metadata = {
        "task_types": ["classification"],
        "tags": ["logistic_regression", "visualization"],
    }
    default_params = {"title": "Cumulative Probabilities"}

    @staticmethod
    def compute_probabilities(model, X):
        """
        Predict probabilities and add them as a new column in X
        """
        probabilities = model.predict(X)
        X["probabilities"] = probabilities
        return X

    @staticmethod
    def plot_cumulative_prob(df_train, df_test, prob_col, target_col, title):
        # Separate probabilities based on target column
        train_0 = np.sort(df_train[df_train[target_col] == 0][prob_col])
        train_1 = np.sort(df_train[df_train[target_col] == 1][prob_col])
        test_0 = np.sort(df_test[df_test[target_col] == 0][prob_col])
        test_1 = np.sort(df_test[df_test[target_col] == 1][prob_col])

        # Calculate cumulative distributions
        cumulative_train_0 = np.cumsum(train_0) / np.sum(train_0)
        cumulative_train_1 = np.cumsum(train_1) / np.sum(train_1)
        cumulative_test_0 = np.cumsum(test_0) / np.sum(test_0)
        cumulative_test_1 = np.cumsum(test_1) / np.sum(test_1)

        # Create subplot
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Train Data", "Test Data"))

        # Create line plots for training data
        trace_train_0 = go.Scatter(
            x=train_0,
            y=cumulative_train_0,
            mode="lines",
            name=f"Train {target_col} = 0",
        )
        trace_train_1 = go.Scatter(
            x=train_1,
            y=cumulative_train_1,
            mode="lines",
            name=f"Train {target_col} = 1",
        )

        # Create line plots for testing data
        trace_test_0 = go.Scatter(
            x=test_0, y=cumulative_test_0, mode="lines", name=f"Test {target_col} = 0"
        )
        trace_test_1 = go.Scatter(
            x=test_1, y=cumulative_test_1, mode="lines", name=f"Test {target_col} = 1"
        )

        # Add traces to the subplots
        fig.add_trace(trace_train_0, row=1, col=1)
        fig.add_trace(trace_train_1, row=1, col=1)
        fig.add_trace(trace_test_0, row=1, col=2)
        fig.add_trace(trace_test_1, row=1, col=2)

        # Update layout
        fig.update_layout(title_text=title)

        return fig

    def run(self):
        model = self.model[0] if isinstance(self.model, list) else self.model

        target_column = model.train_ds.target_column
        title = self.params["title"]

        # Create a copy of training and testing dataframes
        df_train = model.train_ds._df.copy()
        df_test = model.test_ds._df.copy()

        # Drop target_column to create feature dataframes
        X_train = df_train.drop(columns=[target_column])
        X_test = df_test.drop(columns=[target_column])

        # Subset only target_column to create target dataframes
        y_train = df_train[[target_column]]
        y_test = df_test[[target_column]]

        X_train = self.compute_probabilities(model, X_train)
        X_test = self.compute_probabilities(model, X_test)

        df_train = pd.concat([X_train, y_train], axis=1)
        df_test = pd.concat([X_test, y_test], axis=1)

        fig = self.plot_cumulative_prob(
            df_train, df_test, "probabilities", target_column, title
        )

        return self.cache_results(
            metric_value={
                "cum_prob": {
                    "train_probs": list(X_train["probabilities"]),
                    "test_probs": list(X_test["probabilities"]),
                },
            },
            figures=[
                Figure(
                    for_object=self,
                    key="cum_prob",
                    figure=fig,
                )
            ],
        )
