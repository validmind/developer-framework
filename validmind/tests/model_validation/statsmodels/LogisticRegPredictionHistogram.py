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
    Generates and visualizes histograms of the Probability of Default predictions for both positive and negative
    classes in training and testing datasets.

    **Purpose**: This code is designed to generate histograms that display the Probability of Default (PD) predictions
    for positive and negative classes in both the training and testing datasets. By doing so, it evaluates the
    performance of a logistic regression model, particularly in the context of credit risk prediction.

    **Test Mechanism**: The metric executes these steps to run the test:
    - Firstly, it extracts the target column from both the train and test datasets.
    - The model's predict function is then used to calculate probabilities.
    - These probabilities are added as a new column to the training and testing dataframes.
    - Histograms are generated for each class (0 or 1 in binary classification scenarios) within the training and
    testing datasets.
    - To enhance visualization, the histograms are set to have different opacities.
    - The four histograms (two for training data and two for testing) are overlaid on two different subplot frames (one
    for training and one for testing data).
    - The test returns a plotly graph object displaying the visualization.

    **Signs of High Risk**: Several indicators could suggest a high risk or failure in the model's performance. These
    include:
    - Significant discrepancies observed between the histograms of training and testing data.
    - Large disparities between the histograms for the positive and negative classes.
    - These issues could signal potential overfitting or bias in the model.
    - Unevenly distributed probabilities may also indicate that the model does not accurately predict outcomes.

    **Strengths**: This metric and test offer several benefits, including:
    - The visual representation of the PD predictions made by the model, which aids in understanding the model's
    behaviour.
    - The ability to assess both the training and testing datasets, adding depth to the validation of the model.
    - Highlighting disparities between multiple classes, providing potential insights into class imbalance or data
    skewness issues.
    - Particularly beneficial for credit risk prediction, it effectively visualizes the spread of risk across different
    classes.

    **Limitations**: Despite its strengths, the test has several limitations:
    - It is specifically tailored for binary classification scenarios, where the target variable only has two classes;
    as such, it isn't suited for multi-class classification tasks.
    - This metric is mainly applicable for logistic regression models. It might not be effective or accurate when used
    on other model types.
    - While the test provides a robust visual representation of the model's PD predictions, it does not provide a
    quantifiable measure or score to assess model performance.
    """

    name = "logistic_reg_prediction_histogram"
    required_inputs = ["model"]
    metadata = {
        "task_types": ["classification"],
        "tags": ["tabular_data", "visualization", "credit_risk", "logistic_regression"],
    }

    default_params = {"title": "Histogram of Predictive Probabilities"}

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
