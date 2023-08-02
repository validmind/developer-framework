# Copyright © 2023 ValidMind Inc. All rights reserved.

import pandas as pd
from dataclasses import dataclass
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from validmind.vm_models import Figure, Metric, Model


@dataclass
class LogisticRegPredictionHistogram(Metric):
    """
    Probability of Default (PD) Histogram
    """

    name = "logistic_reg_prediction_histogram"
    required_context = ["model"]
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
        pd = probabilities
        X["probabilities"] = pd
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
        if not Model.is_supported_model(self.model.model):
            raise ValueError(
                f"{Model.model_library(self.model.model)}.{Model.model_class(self.model.model)} \
                              is not supported by ValidMind framework yet"
            )

        target_column = self.model.train_ds.target_column
        title = self.params["title"]

        X_train = self.model.train_ds.x.copy()
        y_train = self.model.train_ds.y.copy()
        X_test = self.model.test_ds.x.copy()
        y_test = self.model.test_ds.y.copy()

        X_train = self.compute_probabilities(self.model, X_train)
        X_test = self.compute_probabilities(self.model, X_test)

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
