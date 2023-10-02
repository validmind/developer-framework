# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class PDRatingClassPlot(Metric):
    """
    **Purpose**: The Probability of Default (PD) Rating Class Plot is used to understand the distribution of default
    probabilities across different rating classes. This test is critical in inferring credit risk, as it shows the
    likelihood of default for different rating classes based on the predictions made by the model. The test is designed
    to visualize how effectively the model is able to differentiate between different risk levels in the credit data
    set.

    **Test Mechanism**: This visualization metric classifies predicted probabilities of defaults into user-defined
    rating classes (defined in "rating_classes" in default parameters), performs a calculation of average default rate
    within each rating class, and then generates bar plots for each rating class. The generated bar plots aim to
    illustrate the average probability of default within each class, for both the training and testing data sets. The
    classification of predicted probabilities is performed using the pandas "cut" function, which segments and sorts
    the data values into bins.

    **Signs of High Risk**: If the bar plots show that lower rating classes have higher average probabilities of
    default than higher rating classes, or there is little differentiation between the averages across rating classes,
    this indicates high risk in the model's ability to accurately predict default levels. Also, a model that produces a
    vast difference between probabilities for the training and testing set may indicate overfitting, which is also a
    sign of high risk.

    **Strengths**: The strength of this metric lies in its ability to visually represent the effectiveness of the model
    in predicting credit default risk across different risk levels, allowing for easy interpretation. By visualizing
    the model's effectiveness for each rating class separately, it allows the analyst to quickly identify where the
    model is struggling. The inclusion of both training and testing data sets helps to quickly highlight issues of
    overfitting.

    **Limitations**: The main limitation of this metric comes from predetermining the number of rating classes.
    Incorrect choices could either oversimplify or overcomplicate the picture of default rates. The metric relies
    heavily on the assumptions that the rating classes effectively separate different risk levels and that the defined
    boundaries between rating classes accurately represent the true risk distribution. Furthermore, the tests don't
    account for class imbalance in the data set that could skew the average probabilities. This metric alone cannot be
    used for determining the overall performance of the model, and should be used in combination with other evaluation
    metrics.
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
