# Copyright © 2023 ValidMind Inc. All rights reserved.

import pandas as pd
from dataclasses import dataclass
import plotly.graph_objects as go
from validmind.vm_models import Figure, Metric, Model


@dataclass
class PDRatingClassPlot(Metric):
    """
    Probability of Default (PD) Rating Class Plot
    """

    name = "pd_rating_class_plot"
    required_context = ["model"]
    default_parameters = {
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
        if not Model.is_supported_model(self.model.model):
            raise ValueError(
                f"{Model.model_library(self.model.model)}.{Model.model_class(self.model.model)} \
                is not supported by ValidMind framework yet"
            )

        target_column = self.model.train_ds.target_column
        title = self.params["title"]
        rating_classes = self.params["rating_classes"]

        X_train = self.model.train_ds.x.copy()
        y_train = self.model.train_ds.y.copy()
        X_test = self.model.test_ds.x.copy()
        y_test = self.model.test_ds.y.copy()

        # Compute probabilities
        X_train["probability"] = self.model.model.predict(X_train)
        X_test["probability"] = self.model.model.predict(X_test)

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
