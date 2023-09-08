# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from validmind.vm_models import Figure, Metric


@dataclass
class LogisticRegPredictionHistogram(Metric):
    """
    Probability of Default (PD) Histogram
    """

    name = "logistic_reg_prediction_histogram"
    required_inputs = ["model"]
    default_parameters = {"title": "Histogram of Predictive Probabilities"}

    def description(self):
        return """
        This metric calculates the probability of default (PD) for each instance in the training and test datasets,
        and creates histograms to visualize the distributions of PD for the positive and negative classes.
        """

    @staticmethod
    def compute_probabilities(model, X):
        """
        Predict probabilities and add PD as a new column in X
        """
        probabilities = model.predict(X)
        pd_series = probabilities

        # If X is a numpy array, convert it to DataFrame
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)

        X["probabilities"] = pd_series
        return X

    @staticmethod
    def plot_prob_histogram(df_train, df_test, pd_col, target_col, title):
        train_0 = df_train[df_train[target_col] == 0][pd_col]
        train_1 = df_train[df_train[target_col] == 1][pd_col]
        test_0 = df_test[df_test[target_col] == 0][pd_col]
        test_1 = df_test[df_test[target_col] == 1][pd_col]

        fig = make_subplots(rows=1, cols=2, subplot_titles=("Train Data", "Test Data"))

        trace_train_0 = go.Histogram(
            x=train_0, opacity=0.75, name=f"Train {target_col} = 0"
        )
        trace_train_1 = go.Histogram(
            x=train_1, opacity=0.75, name=f"Train {target_col} = 1"
        )
        trace_test_0 = go.Histogram(
            x=test_0, opacity=0.75, name=f"Test {target_col} = 0"
        )
        trace_test_1 = go.Histogram(
            x=test_1, opacity=0.75, name=f"Test {target_col} = 1"
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

        fig = self.plot_prob_histogram(
            df_train, df_test, "probabilities", target_column, title
        )

        return self.cache_results(
            metric_value={
                "prob_histogram": {
                    "train_probs": list(X_train["probabilities"]),
                    "test_probs": list(X_test["probabilities"]),
                },
            },
            figures=[
                Figure(
                    for_object=self,
                    key="prob_histogram",
                    figure=fig,
                )
            ],
        )
