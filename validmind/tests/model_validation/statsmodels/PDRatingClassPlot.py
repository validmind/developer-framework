# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class PDRatingClassPlot(Metric):
    """
    Assesses and visualizes credit risk distribution across different rating classes within a dataset via default
    probabilities.

    **Purpose**: The purpose of the Probability of Default (PD) Rating Class Plot test is to measure and evaluate the
    distribution of calculated default probabilities across different rating classes. This is critical for
    understanding and inferring credit risk and can provide insights into how effectively the model is differentiating
    between different risk levels in a credit dataset.

    **Test Mechanism**: This metric is implemented via a visualization mechanism. It sorts the predicted probabilities
    of defaults into user-defined rating classes defined in "rating_classes" in default parameters. When it has
    classified the probabilities, it then calculates the average default rates within each rating class. Subsequently,
    it produces bar plots for each of these rating classes, illustrating the average likelihood of a default within
    each class. This process is executed separately for both the training and testing data sets. The classification of
    predicted probabilities utilizes the pandas "cut" function, sorting and sectioning the data values into bins.

    **Signs of High Risk**:

    - If lower rating classes present higher average likelihoods of default than higher rating classes
    - If there is poor differentiation between the averages across the different rating classes
    - If the model generates a significant contrast between the likelihoods for the training set and the testing set,
    suggestive of model overfitting

    **Strengths**:

    - Presents a clear visual representation of how efficient the model is at predicting credit risk across different
    risk levels
    - Allows for rapid identification and understanding of model performance per rating class
    - Highlights potential overfitting issues by including both training and testing datasets in the analysis

    **Limitations**:

    - Making an incorrect choice for the number of rating classes, either oversimplifying or overcomplicating the
    distribution of default rates
    - Relying on the assumption that the rating classes are effective at differentiating risk levels and that the
    boundaries between classes truly represent the risk distribution
    - Not accounting for data set class imbalance, which could cause skewed average probabilities
    - Inability to gauge the overall performance of the model only based on this metric, emphasizing the requirement of
    combining it with other evaluation metrics
    """

    name = "pd_rating_class_plot"
    required_inputs = ["model"]

    metadata = {
        "task_types": ["classification"],
        "tags": ["visualization", "credit_risk"],
    }

    default_params = {
        "title": "PD by Rating Class",
        "rating_classes": ["A", "B", "C", "D"],
    }

    @staticmethod
    def plot_bucket_analysis(df, prob_col, target_col, title, rating_classes):
        df["bucket"] = pd.cut(
            df[prob_col], bins=len(rating_classes), labels=rating_classes, right=False
        )
        default_rate = df.groupby("bucket")[target_col].mean()

        # Sort the data based on the order of rating_classes
        sorted_data = sorted(
            zip(rating_classes, default_rate),
            key=lambda x: rating_classes.index(x[0]),
        )
        rating_classes_sorted, default_rate_sorted = zip(*sorted_data)

        fig = go.Figure()

        # Iterate through the sorted data and create a bar for each score bucket
        for i, (bucket, rate) in enumerate(
            zip(rating_classes_sorted, default_rate_sorted)
        ):
            fig.add_trace(go.Bar(x=[bucket], y=[rate], name=bucket))

        fig.update_layout(
            title_text=title,
            xaxis_title="Rating Class",
            yaxis_title="Probability of Default",
            barmode="group",
        )

        return fig

    def run(self):
        target_column = self.model.train_ds.target_column
        title = self.params["title"]
        rating_classes = self.params["rating_classes"]

        X_train = self.model.train_ds.x.copy()
        y_train = self.model.train_ds.y.copy()
        X_test = self.model.test_ds.x.copy()
        y_test = self.model.test_ds.y.copy()

        # Compute probabilities
        X_train["probability"] = self.model.predict(X_train)
        X_test["probability"] = self.model.predict(X_test)

        df_train = pd.concat([X_train, y_train], axis=1)
        df_test = pd.concat([X_test, y_test], axis=1)

        fig_train = self.plot_bucket_analysis(
            df_train,
            "probability",
            target_column,
            title + " - Train Data",
            rating_classes,
        )
        fig_test = self.plot_bucket_analysis(
            df_test,
            "probability",
            target_column,
            title + " - Test Data",
            rating_classes,
        )

        return self.cache_results(
            metric_value={
                "bucket_analysis": {
                    "train_probs": list(X_train["probability"]),
                    "test_probs": list(X_test["probability"]),
                },
            },
            figures=[
                Figure(
                    for_object=self,
                    key="bucket_analysis_train",
                    figure=fig_train,
                ),
                Figure(
                    for_object=self,
                    key="bucket_analysis_test",
                    figure=fig_test,
                ),
            ],
        )
