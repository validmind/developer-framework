# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from validmind.vm_models import Figure, Metric


@dataclass
class PiTCreditScoresHistogram(Metric):
    """
    **Purpose**: The PiT (Point in Time) Credit Scores Histogram metric is used to assess the performance of a
    classification model with a focus on credit risk evaluation. It visualizes the distributions of observed and
    predicted default scores and provides an intuitive comparison allowing for quick model assessment.

    **Test Mechanism**: This metric leverages histograms to illustrate the differences in score distributions for both
    observed and predicted results. It separates the scores into defaulted (1) and not defaulted (0) and makes a
    histogram for each of these categories. The model compares the distributions of observed and predicted
    classifications simultaneously, furnishing a clear idea about how well the model can predict the credit risk.

    **Signs of High Risk**: If the observed and predicted histograms are significantly different, there may be risk
    factors that the model is not adequately addressing. Additionally, if the predicted defaults are concentrated
    towards one end of the graph or are less evenly distributed than the observed scores, this could indicate potential
    issues with how the model is understanding the data or predicting outcomes.

    **Strengths**: This metric provides an intuitive visual representation of model performance which can be easily
    understood and interpreted even without extensive technical background. By comparing the distributions of observed
    and predicted scores, it gives a clear picture about the model's ability in distinguishing between defaulting and
    non-defaulting entities. It's especially tailored for credit risk assessment models and the PiT element takes into
    consideration time evolution of credit risk.

    **Limitations**: This visual method may not provide accurate enough information for detailed statistical analysis
    and doesn't give precise, quantifiable measures of model performance. It relies on manual inspection and
    comparison, making it subjective to human bias and potentially less reliable for catching subtle discrepancies.
    Furthermore, this method doesn't work well when the score distributions overlap significantly or when there are too
    many scores to be plotted, resulting in cluttered or hard-to-read graphs.
    """

    name = "pit_credit_scores_histogram"
    required_context = ["dataset"]
    default_params = {"title": "Histogram of Scores"}
    metadata = {
        "task_types": ["classification"],
        "tags": ["tabular_data", "visualization", "credit_risk"],
    }

    @staticmethod
    def plot_score_histogram(
        df,
        default_column,
        predicted_default_column,
        scores_column,
        title,
        point_in_time_date,
    ):
        fig = make_subplots(
            rows=1, cols=2, subplot_titles=("Observed Default", "Predicted Default")
        )

        observed_data_0 = df[df[default_column] == 0][scores_column]
        observed_data_1 = df[df[default_column] == 1][scores_column]

        predicted_data_0 = df[df[predicted_default_column] == 0][scores_column]
        predicted_data_1 = df[df[predicted_default_column] == 1][scores_column]

        fig.add_trace(
            go.Histogram(x=observed_data_0, opacity=0.75, name="Observed Default = 0"),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Histogram(x=observed_data_1, opacity=0.75, name="Observed Default = 1"),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Histogram(
                x=predicted_data_0, opacity=0.75, name="Predicted Default = 0"
            ),
            row=1,
            col=2,
        )
        fig.add_trace(
            go.Histogram(
                x=predicted_data_1, opacity=0.75, name="Predicted Default = 1"
            ),
            row=1,
            col=2,
        )

        title += f" (PiT: {point_in_time_date.strftime('%d %b %Y')})"
        fig.update_layout(barmode="overlay", title_text=title)

        return fig

    def run(self):
        df = self.dataset
        default_column = self.params["default_column"]
        predicted_default_column = self.params["predicted_default_column"]
        scores_column = self.params["scores_column"]
        point_in_time_column = self.params["point_in_time_column"]

        title = self.params["title"]

        point_in_time_date = pd.to_datetime(df[point_in_time_column].iloc[0])

        fig = self.plot_score_histogram(
            df,
            default_column,
            predicted_default_column,
            scores_column,
            title,
            point_in_time_date,
        )

        return self.cache_results(
            metric_value={
                "score_histogram": {
                    "observed_scores": list(df[df[default_column] == 1][scores_column]),
                    "predicted_scores": list(
                        df[df[predicted_default_column] == 1][scores_column]
                    ),
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
