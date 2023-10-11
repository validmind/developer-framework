# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from validmind.vm_models import Figure, Metric


@dataclass
class PiTCreditScoresHistogram(Metric):
    """
    Generates a histogram visualization for observed and predicted credit default scores.

    **Purpose**:
    The PiT (Point in Time) Credit Scores Histogram metric is used to evaluate the predictive performance of a credit
    risk assessment model. This metric provides a visual representation of observed versus predicted default scores and
    enables quick and intuitive comparison for model assessment.

    **Test Mechanism**:
    This metric generates histograms for both observed and predicted score distributions of defaults and non-defaults.
    The simultaneous representation of both the observed and predicted scores sheds light on the model's ability to
    accurately predict credit risk.

    **Signs of High Risk**:
    - Significant discrepancies between the observed and predicted histograms, suggesting that the model may not be
    adequately addressing certain risk factors.
    - Concentration of predicted defaults towards one end of the graph, or uneven distribution in comparison to
    observed scores, indicating potential issues in the model's interpretation of the data or outcome prediction.

    **Strengths**:
    - Provides an intuitive visual representation of model performance that's easy to comprehend, even for individuals
    without a technical background.
    - Useful for understanding the model's ability to distinguish between defaulting and non-defaulting entities.
    - Specifically tailored for assessing credit risk models. The Point in Time (PiT) factor considers the evolution of
    credit risk over time.

    **Limitations**:
    - As the information is visual, precise and quantitative results for detailed statistical analyses may not be
    obtained.
    - The method relies on manual inspection and comparison, introducing subjectivity and potential bias.
    - Subtle discrepancies might go unnoticed and it could be less reliable for identifying such cues.
    - Performance may degrade when score distributions overlap significantly or when too many scores are plotted,
    resulting in cluttered or hard-to-decipher graphs.
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
