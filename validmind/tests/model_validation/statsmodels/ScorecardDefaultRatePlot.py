import numpy as np
import pandas as pd
from dataclasses import dataclass
import plotly.graph_objects as go
from validmind.vm_models import Figure, Metric, Model


@dataclass
class ScorecardDefaultRatePlot(Metric):
    """
    Scorecard Bucket Analysis
    """

    name = "scorecard_default_rate_plot"
    required_context = ["model"]
    default_parameters = {
        "title": "Default Rates by Rating Class",
        "target_score": 600,
        "target_odds": 50,
        "pdo": 20,
        "rating_classes": ["A", "B", "C", "D"],
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
    def plot_bucket_analysis(df, score_col, target_col, title, rating_classes):
        df["bucket"] = pd.cut(
            df[score_col], bins=len(rating_classes), labels=rating_classes, right=False
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
            yaxis_title="Default Rate",
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
        target_score = self.params["target_score"]
        target_odds = self.params["target_odds"]
        pdo = self.params["pdo"]
        rating_classes = self.params["rating_classes"]

        X_train = self.model.train_ds.x.copy()
        y_train = self.model.train_ds.y.copy()
        X_test = self.model.test_ds.x.copy()
        y_test = self.model.test_ds.y.copy()

        X_train_scores = self.compute_scores(
            self.model, X_train, target_score, target_odds, pdo
        )
        X_test_scores = self.compute_scores(
            self.model, X_test, target_score, target_odds, pdo
        )

        df_train = pd.concat([X_train_scores, y_train], axis=1)
        df_test = pd.concat([X_test_scores, y_test], axis=1)

        fig_train = self.plot_bucket_analysis(
            df_train, "score", target_column, title + " - Train Data", rating_classes
        )
        fig_test = self.plot_bucket_analysis(
            df_test, "score", target_column, title + " - Test Data", rating_classes
        )

        return self.cache_results(
            metric_value={
                "bucket_analysis": {
                    "train_scores": list(X_train_scores["score"]),
                    "test_scores": list(X_test_scores["score"]),
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
